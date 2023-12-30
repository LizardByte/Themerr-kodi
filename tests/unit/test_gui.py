# standard imports
import os

# kodi imports
import xbmc

# lib imports
import pytest

# local imports
from src.themerr import gui


@pytest.fixture(
    scope='function',
    params=[
        'tmdb_10378',
    ],
)
def kodi_id(request):
    return request.param


@pytest.fixture(scope='function')
def window_obj(mock_xbmc_player):
    """Return the Window object with a mocked player"""
    return gui.Window(player_instance=mock_xbmc_player)


def test_window_init(window_obj):
    """Test the Window object is initialized correctly"""
    assert isinstance(window_obj.monitor, xbmc.Monitor)

    isinstance(window_obj.player, xbmc.Player)
    assert type(window_obj.player).__name__ == 'Player'

    assert window_obj.item_selected_for == 0
    assert window_obj.playing_item_not_selected_for == 0
    assert window_obj.current_selected_item_id is None
    assert window_obj.last_selected_item_id is None
    assert window_obj.uuid_mapping == {}


def test_pre_checks_no_item_playing(window_obj):
    # Scenario 1: No item playing
    assert window_obj.pre_checks() is True


def test_pre_checks_video_is_playing(window_obj):
    # Scenario 2: Video is playing
    os.environ['_KODI_GET_PLAYING_FILE'] = 'https://www.youtube.com/watch?v=123'
    os.environ['_KODI_IS_PLAYING_VIDEO'] = '1'
    assert window_obj.pre_checks() is False

    del os.environ['_KODI_GET_PLAYING_FILE']
    del os.environ['_KODI_IS_PLAYING_VIDEO']


def test_pre_checks_mismatched_item_playing(window_obj):
    # Scenario 3: Item playing does not match player.theme_playing_url
    # i.e., The user starting playing something else
    os.environ['_KODI_GET_PLAYING_FILE'] = 'https://www.youtube.com/watch?v=123'
    window_obj.player.theme_playing_url = 'https://www.youtube.com/watch?v=456'
    assert window_obj.pre_checks() is False
    assert window_obj.player.theme_is_playing is False
    assert window_obj.player.theme_playing_kodi_id is None
    assert window_obj.player.theme_playing_url is None
    assert window_obj.item_selected_for == 0

    del os.environ['_KODI_GET_PLAYING_FILE']


def test_pre_checks_all_passing(window_obj):
    # Scenario 4: Everything is fine
    os.environ['_KODI_GET_PLAYING_FILE'] = 'https://www.youtube.com/watch?v=123'
    window_obj.player.theme_playing_url = 'https://www.youtube.com/watch?v=123'
    assert window_obj.pre_checks() is True


def test_process_kodi_id_movies(kodi_id, mock_xbmc_get_cond_visibility, window_obj):
    condition = 'Container.Content(movies)'
    env_var = f'_KODI_GET_COND_VISIBILITY_{condition}'
    os.environ[env_var] = '1'

    youtube_url = window_obj.process_kodi_id(kodi_id=kodi_id)
    assert youtube_url

    del os.environ[env_var]


def test_process_kodi_id_movie_collection(mock_xbmc_get_cond_visibility, window_obj):
    _kodi_id = 'tmdb_645'
    condition = 'ListItem.IsCollection'
    env_var = f'_KODI_GET_COND_VISIBILITY_{condition}'
    os.environ[env_var] = '1'

    youtube_url = window_obj.process_kodi_id(kodi_id=_kodi_id)
    assert youtube_url

    del os.environ[env_var]


def test_find_youtube_url(kodi_id, window_obj):
    youtube_url = window_obj.find_youtube_url(
        kodi_id=kodi_id,
        db_type='movies',
    )

    assert youtube_url
    assert youtube_url.startswith('https://')


@pytest.mark.parametrize('kodi_id_invalid', [
    'tmdb_0',
])
def test_find_youtube_url_exception(window_obj, kodi_id_invalid):
    youtube_url = window_obj.find_youtube_url(
        kodi_id=kodi_id_invalid,
        db_type='bar',
    )

    assert not youtube_url


@pytest.mark.parametrize('checks', [
    True,
    False,
    (True, True, True),
    (True, True, False),
    (True, False, True),
    (True, False, False),
    (False, True, True),
    (False, True, False),
    (False, False, True),
    (False, False, False),
])
def test_any_true(window_obj, checks):
    if isinstance(checks, bool):
        assert window_obj.any_true(check=checks) is checks
    elif True in checks:
        assert window_obj.any_true(checks=checks) is True
    else:
        assert window_obj.any_true(checks=checks) is False


@pytest.mark.parametrize('expected', [
    False,
    True,
])
def test_is_home(mock_xbmc_get_cond_visibility, window_obj, expected):
    condition = 'Window.IsVisible(home)'
    env_var = f'_KODI_GET_COND_VISIBILITY_{condition}'

    if expected:
        os.environ[env_var] = '1'

    assert window_obj.is_home() is expected

    if expected:
        del os.environ[env_var]


@pytest.mark.parametrize('expected', [
    False,
    True,
])
def test_is_movies(mock_xbmc_get_cond_visibility, window_obj, expected):
    condition = 'Container.Content(movies)'
    env_var = f'_KODI_GET_COND_VISIBILITY_{condition}'

    if expected:
        os.environ[env_var] = '1'

    assert window_obj.is_movies() is expected

    if expected:
        del os.environ[env_var]


@pytest.mark.parametrize('expected', [
    False,
    True,
])
def test_is_movie_set(mock_xbmc_get_cond_visibility, window_obj, expected):
    condition = 'ListItem.IsCollection'
    env_var = f'_KODI_GET_COND_VISIBILITY_{condition}'

    if expected:
        os.environ[env_var] = '1'

    assert window_obj.is_movie_set() is expected

    if expected:
        del os.environ[env_var]


@pytest.mark.parametrize('expected', [
    False,
    True,
])
def test_is_tv_shows(mock_xbmc_get_cond_visibility, window_obj, expected):
    condition = 'Container.Content(tvshows)'
    env_var = f'_KODI_GET_COND_VISIBILITY_{condition}'

    if expected:
        os.environ[env_var] = '1'

    assert window_obj.is_tv_shows() is expected

    if expected:
        del os.environ[env_var]


@pytest.mark.parametrize('expected', [
    False,
    True,
])
def test_is_seasons(mock_xbmc_get_cond_visibility, window_obj, expected):
    condition = 'Container.Content(Seasons)'
    env_var = f'_KODI_GET_COND_VISIBILITY_{condition}'

    if expected:
        os.environ[env_var] = '1'

    assert window_obj.is_seasons() is expected

    if expected:
        del os.environ[env_var]


@pytest.mark.parametrize('expected', [
    False,
    True,
])
def test_is_episodes(mock_xbmc_get_cond_visibility, window_obj, expected):
    condition = 'Container.Content(Episodes)'
    env_var = f'_KODI_GET_COND_VISIBILITY_{condition}'

    if expected:
        os.environ[env_var] = '1'

    assert window_obj.is_episodes() is expected

    if expected:
        del os.environ[env_var]
