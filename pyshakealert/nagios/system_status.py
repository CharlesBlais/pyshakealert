'''
Nagios System Status
====================

Process system status information to a nagios results

..  codeauthor:: Charles Blais
'''
import datetime

from dateutil.parser import parse

from pyshakealert.message.system_status import to_string

from pyshakealert.message.system_status.system_status import SystemStatus

from pyshakealert.message.system_status.component import Component

from pyshakealert.message.system_status.subcomponent import SubComponent

from typing import List, Optional

from .models import NagiosRange, NagiosResult, NagiosOutputCode, \
    NagiosPerformance


def _status_to_code(status: str) -> NagiosOutputCode:
    '''
    Convert string status to output code
    '''
    if status == 'WARNING':
        return NagiosOutputCode.warning
    elif status == 'OFFLINE':
        return NagiosOutputCode.critical
    elif status == 'ON':
        return NagiosOutputCode.ok
    return NagiosOutputCode.unknown


def system_status_to_nagios(
    system_status: SystemStatus
) -> NagiosResult:
    '''
    Convert system status to Nagios
    '''
    value = system_status.count
    total = system_status.count + system_status.missing
    perf = NagiosPerformance(
        label='count',
        value=value,
        critical=system_status.required,
        minimum=0,
        maximum=total,
    )

    return NagiosResult(
        summary=f'{system_status.status} - {system_status.alg_name}, \
{value}/{total}, required: {system_status.required}, \
unexpected: {system_status.unexpected}, {system_status.timestamp}',
        status=_status_to_code(system_status.status),
        performances=[perf],
        details=to_string(system_status)
    )


def component_to_nagios(
    component: Component
) -> NagiosResult:
    '''
    Convert component to Nagios
    '''
    value = component.count
    total = component.count + component.missing
    perf = NagiosPerformance(
        label='count',
        value=value,
        critical=component.required,
        minimum=0,
        maximum=total,
    )

    return NagiosResult(
        summary=f'{component.status} - {component.name}, \
{value}/{total}, \
required: {component.required}',
        status=_status_to_code(component.status),
        performances=[perf],
        details=to_string(component)
    )


def subcomponent_to_nagios(
    subcomponent: SubComponent
) -> NagiosResult:
    '''
    Convert subcomponent to Nagios
    '''
    return NagiosResult(
        summary=f'{subcomponent.status} - {subcomponent.name}, \
{subcomponent.timestamp}',
        status=_status_to_code(subcomponent.status),
        details=to_string(subcomponent)
    )


def to_nagios(
    system_status: SystemStatus,
    namepath: List[str] = []
) -> NagiosResult:
    '''
    Convert system status information to a Nagios result
    '''
    if len(namepath) == 0:
        return system_status_to_nagios(system_status)
    elif len(namepath) == 1:
        for comp in system_status.component:
            if comp.name != namepath[0]:
                continue
            return component_to_nagios(comp)
    elif len(namepath) == 2:
        for comp in system_status.component:
            if comp.name != namepath[0]:
                continue
            for scomp in comp.subcomponent:
                if scomp.name != namepath[1]:
                    continue
                return subcomponent_to_nagios(scomp)
    raise ValueError(f'Invalid namepath {namepath}')


def to_nagios_time_check(
    system_status: SystemStatus,
    warning: Optional[NagiosRange] = None,
    critical: Optional[NagiosRange] = None,
) -> NagiosResult:
    '''
    Convert system_status time check to range
    '''
    ts = parse(system_status.timestamp).replace(tzinfo=None)
    offset = (
        datetime.datetime.utcnow() - ts
    ).total_seconds()
    perf = NagiosPerformance(label='offset', value=offset)

    if critical is not None and critical.in_range(offset):
        return NagiosResult(
            summary=f'CRITICAL - {system_status.alg_name} \
{system_status.timestamp}',
            status=NagiosOutputCode.critical,
            performances=[perf],
            details=to_string(system_status)
        )
    if warning is not None and warning.in_range(offset):
        return NagiosResult(
            summary=f'WARNING - {system_status.alg_name} \
{system_status.timestamp}',
            status=NagiosOutputCode.warning,
            performances=[perf],
            details=to_string(system_status)
        )
    return NagiosResult(
        summary=f'OK - {system_status.alg_name} \
{system_status.timestamp}',
        status=NagiosOutputCode.ok,
        performances=[perf],
        details=to_string(system_status)
    )
