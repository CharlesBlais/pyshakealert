"""
..  codeauthor:: Charles Blais
"""
import pyshakealert.message.system_status as system_status


def test_system_status():
    """
    Test reading event read from file
    """
    message = system_status.from_file(
        'tests/message/examples/system_status.xml')
    assert message.alg_name == 'ha'
    assert message.alg_version == '2.2.1_2020-07-28'
    assert message.count == 15
    assert message.instance == 'ha_sa.eew-cn-int1'
    assert message.missing == 4
    assert message.required == 15
    assert message.status == 'WARNING'
    assert message.timestamp == '2022-06-01T12:23:10UTC'
    assert message.unexpected == 2
    assert len(message.component) == message.count
    assert message.component[0].count == 1
    assert message.component[0].missing == 0
    assert message.component[0].name == 'sa'
    assert message.component[0].required == 1
    assert message.component[0].status == 'ON'
    assert len(message.component[0].subcomponent) == message.component[0].count
    assert message.component[0].subcomponent[0].name == 'sa.eew-cn-int1'
    assert message.component[0].subcomponent[0].status == 'ON'
    assert message.component[0].subcomponent[0].timestamp \
        == '2022-06-01T12:23:07UTC'
