'''
Test player for timelines
'''

from pyshakealert.player import CSVPlayer


def test_csv_player_parser():
    '''
    CSV player
    '''
    csv = CSVPlayer('tests/player/play.csv')
    assert len(csv.playlist) == 2
