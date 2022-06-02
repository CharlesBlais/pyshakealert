'''
..  codeauthor:: Charles Blais
'''
import pytest

from pyshakealert.nagios import models

from pyshakealert.nagios.system_status import to_nagios

from pyshakealert.nagios.nrdp import to_nrdp

from pyshakealert.message.system_status import from_file

from pyshakealert.message.system_status.system_status import SystemStatus


@pytest.fixture
def system_status() -> SystemStatus:
    return from_file('tests/message/examples/system_status.xml')


def test_nagios_performance():
    '''
    Test generation of performance stats
    '''
    perf = models.NagiosPerformance(
        label='value',
        value=1,
        uom='%',
        warning=2,
        critical=3,
        minimum=0.9,
        maximum=1.1,
    )
    assert str(perf) == "'value'=1%;2.00000;3.00000;0.90000;1.10000"


def test_nagios_result():
    ng = models.NagiosResult(
        summary='test',
        status=models.NagiosOutputCode.ok,
        details='testing'
    )

    ng.verbose = models.NagiosVerbose.minimal
    assert str(ng) == 'test'
    ng.verbose = models.NagiosVerbose.singleline
    assert str(ng) == 'test |'
    ng.verbose = models.NagiosVerbose.multiline
    assert str(ng) == 'test |\ntesting'


def test_nagios_conv(system_status: SystemStatus):
    ng = to_nagios(system_status)
    print(ng)
    assert ng.status == models.NagiosOutputCode.warning


def test_nagios_conv_component(system_status: SystemStatus):
    ng = to_nagios(system_status, namepath=['epic'])
    print(ng)
    assert ng.status == models.NagiosOutputCode.ok


def test_nagios_conv_subcomponent_ok(system_status: SystemStatus):
    ng = to_nagios(system_status, namepath=['epic', 'epic.eew-cn-int1'])
    print(ng)
    assert ng.status == models.NagiosOutputCode.ok


def test_nagios_conv_subcomponent_nok(system_status: SystemStatus):
    ng = to_nagios(system_status, namepath=['epic', 'epic.eew-cn-int2'])
    print(ng)
    assert ng.status == models.NagiosOutputCode.critical


def test_nagios_conv_component_epic(system_status: SystemStatus):
    ng = to_nagios(system_status, namepath=['epic.wp.cn'])
    print(ng)


def test_nagios_nrdp(system_status: SystemStatus):
    nrdp = to_nrdp('eew-cn-int1', system_status)
    print(nrdp)
