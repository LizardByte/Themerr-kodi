# lib imports
import pytest

# local imports
from src.themerr import monitor
from src.themerr import settings


@pytest.fixture(scope='function')
def monitor_obj():
    """Return a new Monitor object"""
    return monitor.ThemerrMonitor()


def test_abort_requested(monitor_obj):
    """Test that abort_requested returns the correct value"""
    assert monitor_obj.abortRequested() is True  # kodistubs returns True only


def test_on_settings_changed(monitor_obj):
    """Test that on_settings_changed updates the monitor's settings"""
    og_settings = settings.settings

    monitor_obj.onSettingsChanged()

    assert settings.settings != og_settings
