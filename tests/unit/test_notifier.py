# kodi imports
import xbmcgui

# lib imports
import pytest

# local imports
from src.themerr import notifier


@pytest.fixture(scope='function')
def notifier_obj():
    """Create a notifier object"""
    return notifier.Notifier()


def test_default_notify(mock_xbmcgui_dialog, notifier_obj):
    """Test notify method"""
    message = 'Test message'
    notifier_obj.notify(message=message)

    mock_xbmcgui_dialog.notification.assert_called_once_with(
        heading=notifier_obj.heading,
        message=message,
        icon=notifier_obj.icon,
        time=notifier_obj.time,
        sound=notifier_obj.sound,
    )


@pytest.mark.parametrize('heading, icon, time, sound', [
    ('Test heading', xbmcgui.NOTIFICATION_INFO, 10000, False),
    ('Test heading', xbmcgui.NOTIFICATION_INFO, -1, False),
    ('Test heading', xbmcgui.NOTIFICATION_WARNING, 0, False),
    ('Test heading', xbmcgui.NOTIFICATION_ERROR, 10000, True),
])
def test_notify(mock_xbmcgui_dialog, notifier_obj, heading, icon, time, sound):
    """Test notify method"""
    message = 'Test message'
    notifier_obj.notify(
        message=message,
        heading=heading,
        icon=icon,
        time=time,
        sound=sound,
    )

    mock_xbmcgui_dialog.notification.assert_called_once_with(
        heading=heading,
        message=message,
        icon=icon,
        time=time,
        sound=sound,
    )
