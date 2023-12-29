# standard imports
import os
import sys
from unittest.mock import MagicMock

# lib imports
import pytest

# local imports
from src.themerr import plugin


@pytest.fixture(scope='function')
def plugin_obj():
    """Return the plugin object"""
    return plugin.Themerr()


def test_plugin_init(mock_xbmcaddon_addon, mock_xbmcvfs, plugin_obj):
    """Test plugin object initialization"""
    assert plugin_obj.monitor
    assert plugin_obj.settings
    assert not plugin_obj.gui
    assert plugin_obj.add_on
    assert plugin_obj.cwd == os.getcwd()
    assert plugin_obj.lib_dir.endswith(f'resources{os.sep}lib')

    assert plugin_obj.lib_dir in sys.path
    assert plugin_obj.threads == []


def test_start(plugin_obj):
    """Test plugin start method"""
    plugin_obj.start()
    assert plugin_obj.gui
    assert plugin_obj.threads


def test_terminate(plugin_obj):
    """Test plugin terminate method"""
    plugin_obj.start()
    plugin_obj.monitor = MagicMock()

    plugin_obj.terminate()

    for thread in plugin_obj.threads:
        assert not thread.is_alive()

    with pytest.raises(AttributeError):
        _ = plugin_obj.monitor
