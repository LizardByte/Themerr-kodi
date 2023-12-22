# standard imports
import os
from unittest.mock import MagicMock, patch

# kodi imports
import xbmc

# lib imports
import pytest

# script imports
from scripts.bootstrap_kodi import bootstrap_modules

# bootstrap kodi modules
bootstrap_modules()

from src.themerr.player import Player  # noqa: E402


@pytest.fixture(scope='function')
def mock_xbmc_log():
    with patch('xbmc.log', spec=True) as mock_log:
        yield mock_log


@pytest.fixture(scope='function')
def mock_xbmcgui_dialog():
    with patch('xbmcgui.Dialog', spec=True) as mock_dialog:
        mock_instance = mock_dialog.return_value
        yield mock_instance


@pytest.fixture(scope='function')
def mock_xbmc_player():
    with patch.multiple(
            xbmc.Player,
            getPlayingFile=MagicMock(),
            isPlayingVideo=MagicMock(),
            play=MagicMock(),
            stop=MagicMock(),
    ):
        def getPlayingFile_side_effect():
            if os.getenv('_KODI_GET_PLAYING_FILE'):
                return os.getenv('_KODI_GET_PLAYING_FILE')
            else:
                raise RuntimeError('Simulated RuntimeError')

        xbmc.Player.getPlayingFile.side_effect = getPlayingFile_side_effect

        def isPlayingVideo_side_effect():
            if os.getenv('_KODI_IS_PLAYING_VIDEO'):
                return True
            else:
                return False

        xbmc.Player.isPlayingVideo.side_effect = isPlayingVideo_side_effect

        yield Player()


@pytest.fixture(scope='function')
def mock_xbmcaddon_addon():
    with patch('xbmcaddon.Addon', spec=True) as mock_addon:
        mock_instance = mock_addon.return_value

        # Define a side effect function for getAddonInfo
        def getAddonInfo_side_effect(arg):
            if arg == 'path':
                return os.getcwd()  # Return current working directory for 'path'
            # Handle other arguments if necessary
            return 'default_value'  # Return a default value or raise an error

        # Set the side effect for getAddonInfo
        mock_instance.getAddonInfo.side_effect = getAddonInfo_side_effect

        yield mock_instance


@pytest.fixture(scope='function')
def mock_xbmcvfs():
    with patch('xbmcvfs.translatePath', spec=True) as mock_vfs:

        # override the translatePath method
        def translate_path(path: str):
            return path

        mock_vfs.side_effect = translate_path

        yield mock_vfs


@pytest.fixture(scope='function')
def mock_xbmc_get_cond_visibility():
    with patch('xbmc.getCondVisibility', spec=True) as mock_visibility:

        # override the getCondVisibility method
        def get_cond_visibility(condition: str):
            try:
                os.environ[f'_KODI_GET_COND_VISIBILITY_{condition}']
            except KeyError:
                return False
            else:
                return True

        mock_visibility.side_effect = get_cond_visibility

        yield mock_visibility
