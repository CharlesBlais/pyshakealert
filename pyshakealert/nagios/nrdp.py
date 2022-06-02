'''
..  codeauthor:: Charles Blais
'''
import logging

from dataclasses import asdict

from typing import List, Optional

import json

from .models import NagiosRange, NagiosResultExtended, NagiosVerbose, \
    NRDP, NRDPCheckResults, NRDPCheckResult

from pyshakealert.message.system_status.system_status import SystemStatus

import requests

from .system_status import to_nagios, to_nagios_time_check


def nagios_to_nrdp(
    results: List[NagiosResultExtended]
) -> NRDP:
    '''
    Convert the Nagios plugin format result to NRDP
    format which is used for passive checks.
    '''
    nrdp = NRDP(checkresults=[])
    for result in results:
        # force the result to full verbose
        result.check.verbose = NagiosVerbose.multiline
        nrdp.checkresults.append(
            NRDPCheckResults(
                checkresult=NRDPCheckResult(type='service'),
                hostname=result.hostname,
                servicename=result.servicename,
                state=str(result.check.status.value),
                output=str(result.check),
            )
        )
    return nrdp


def to_nrdp(
    hostname: str,
    system_status: SystemStatus,
    warning: Optional[NagiosRange] = None,
    critical: Optional[NagiosRange] = None,
    prefix: str = 'Heartbeat -',
) -> NRDP:
    '''
    Generic method of converting a system status to complete list for
    Nagios reporting.  The idea is each component is reported individually
    as their own service. The following are assumptions:

    1. the system_status if for 1 hostname
    2. the servicename format: '{prefix} {instance}/{component.name}'
    3. global servicename format: '{prefix} {instance}

    Note, there is a global servicename is heartbeat update time.  The alerting
    thresholds are used for this.  The service name is '{prefix} last update'

    "instance" is the name without the host (pre .)
    '''
    instance = system_status.instance.split('.')[0]

    results = [
        NagiosResultExtended(
            hostname=hostname,
            servicename=f'{prefix} {instance} last update',
            check=to_nagios_time_check(
                system_status, warning, critical)
        ),
        NagiosResultExtended(
            hostname=hostname,
            servicename=f'{prefix} {instance}',
            check=to_nagios(system_status)
        )
    ]
    for comp in system_status.component:
        results.append(
            NagiosResultExtended(
                hostname=hostname,
                servicename=f'{prefix} {instance}/{comp.name}',
                check=to_nagios(system_status, namepath=[comp.name])
            )
        )
    return nagios_to_nrdp(results)


def submit(
    nrdp: NRDP,
    nagios_url: str,
    nagios_token: str,
):
    '''
    Submit the system_status result to Nagios API
    '''
    jsondata = json.dumps(asdict(nrdp))
    logging.info(f'Sending check:\n{jsondata}')
    data = {
        'token': nagios_token,
        'cmd': 'submitcheck',
        'json': jsondata
    }
    r = requests.post(nagios_url, data=data)
    r.raise_for_status()
    content = r.json()
    logging.debug(f'Response: {content}')
    if not isinstance(content, dict):
        raise requests.exceptions.HTTPError(
            f'Weird response from nagios: {content}')
    if content.get('result', {}).get('status') != 0:
        raise requests.exceptions.HTTPError(content)
