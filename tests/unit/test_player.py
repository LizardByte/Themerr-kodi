# kodi imports
import xbmc

# lib imports
import pytest

# local imports
from src.themerr import player


@pytest.fixture(scope='function')
def player_obj(mock_xbmc_player):
    """Return a Player object"""
    return player.Player()


def test_player_init(player_obj):
    """Test Player object initialization"""
    assert not player_obj.theme_is_playing
    assert not player_obj.theme_is_playing_for
    assert not player_obj.theme_playing_kodi_id
    assert not player_obj.theme_playing_url


@pytest.mark.parametrize('url', [
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'https://www.youtube.com/watch?v=Wb8j8Ojd4YQ&list=PLMYr5_xSeuXAbhxYHz86hA1eCDugoxXY0&pp=iAQB',  # playlist test
])
def test_ytdl_extract_url(player_obj, url):
    """Test ytdl_extract_url"""
    audio_url = player_obj.ytdl_extract_url(url=url)
    assert audio_url is not None
    assert audio_url.startswith('https://')


@pytest.mark.parametrize('url', [
    'https://www.youtube.com/watch?v=notavideoid',
    'https://blahblahblah',
])
def test_ytdl_extract_url_invalid(player_obj, url):
    """Test ytdl_extract_url with invalid url"""
    audio_url = player_obj.ytdl_extract_url(url=url)
    assert audio_url is None


def test_play_url(player_obj):
    """Test play_url"""
    url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    kodi_id = 1
    player_obj.play_url(
        url=url,
        kodi_id=kodi_id,
        windowed=False,
    )
    assert player_obj.theme_is_playing
    assert player_obj.theme_playing_kodi_id == kodi_id
    assert player_obj.theme_playing_url

    # noinspection PyUnresolvedReferences
    assert xbmc.Player.play.called_once_with(
        url=url,
        kodi_id=kodi_id,
        windowed=False,
    )


def test_stop(player_obj):
    """Test stop"""
    player_obj.stop()
    assert not player_obj.theme_is_playing
    assert not player_obj.theme_is_playing_for
    assert not player_obj.theme_playing_kodi_id
    assert not player_obj.theme_playing_url

    # noinspection PyUnresolvedReferences
    assert xbmc.Player.stop.called_once_with()


def test_reset(player_obj):
    """Test reset"""
    player_obj.theme_is_playing = True
    player_obj.theme_is_playing_for = 1000
    player_obj.theme_playing_kodi_id = 1000
    player_obj.theme_playing_url = 'https://...'

    player_obj.reset()
    assert not player_obj.theme_is_playing
    assert not player_obj.theme_is_playing_for
    assert not player_obj.theme_playing_kodi_id
    assert not player_obj.theme_playing_url
