# lib imports
import pytest

# local imports
from src.themerr import locale


@pytest.fixture(scope='function')
def locale_obj():
    """Create a Locale object"""
    return locale.Locale()


def test_addon(locale_obj):
    """Test the addon method"""
    strings = locale_obj.addon()
    assert 'addon.extension.description' in strings
    assert 'addon.extension.summary' in strings

    for key, value in strings.items():
        assert isinstance(value, str)


def test_settings(locale_obj):
    """Test the settings method"""
    strings = locale_obj.settings()
    assert 31001 in strings

    keys = strings.keys()
    assert min(keys) == 31001, "The first key should be 31001"

    for key, value in strings.items():
        assert isinstance(key, int)
        assert isinstance(value, str)
