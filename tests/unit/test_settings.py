# lib imports
import pytest

# local imports
from src.themerr import settings


@pytest.fixture(scope='function')
def settings_obj():
    """Return the Settings object"""
    return settings.Settings()


def test_settings_init(mock_xbmcaddon_addon, settings_obj):
    """Test the Settings class __init__ method"""
    assert settings_obj.addon == mock_xbmcaddon_addon
