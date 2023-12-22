# standard imports
from typing import Optional

# kodi imports
import xbmcgui

# local imports
from . import constants


class Notifier:
    """
    A class to show notification dialogs.

    A wrapper class for the ``xbmcgui.Dialog.notification`` method.

    Parameters
    ----------
    heading : Optional[str]
        The heading of the notification dialog.
    icon : Optional[str]
        The icon of the notification dialog.
    time : Optional[int]
        The time to show the notification dialog.
    sound : Optional[bool]
        Whether to play a sound when showing the notification dialog.

    Attributes
    ----------
    dialog : xbmcgui.Dialog
        The notification dialog.
    heading : Optional[str]
        The heading of the notification dialog.
    icon : Optional[str]
        The icon of the notification dialog.
    time : Optional[int]
        The time to show the notification dialog.
    sound : Optional[bool]
        Whether to play a sound when showing the notification dialog.

    Methods
    -------
    notify(
        message: str,
        heading: Optional[str] = None,
        icon: Optional[str] = None,
        time: Optional[int] = None,
        sound: Optional[bool] = None,
    )
        Show a notification dialog.

    Examples
    --------
    >>> notifier = Notifier()
    """
    def __init__(
            self,
            heading: Optional[str] = constants.name,
            icon: Optional[str] = xbmcgui.NOTIFICATION_INFO,
            time: Optional[int] = 5000,
            sound: Optional[bool] = True,
    ):
        self.dialog = xbmcgui.Dialog()
        self.heading = heading
        self.icon = icon
        self.time = time
        self.sound = sound

    def notify(
            self,
            message: str,
            heading: Optional[str] = None,
            icon: Optional[str] = None,
            time: Optional[int] = None,
            sound: Optional[bool] = None,
    ):
        """
        Show a notification dialog.

        Use the ``xbmcgui.Dialog.notification`` method to show a notification dialog.

        Parameters
        ----------
        message : str
            The message of the notification dialog.
        heading : Optional[str]
            The heading of the notification dialog.
        icon : Optional[str]
            The icon of the notification dialog.
        time : Optional[int]
            The time to show the notification dialog.
        sound : Optional[bool]
            Whether to play a sound when showing the notification dialog.

        Examples
        --------
        >>> notifier = Notifier()
        >>> notifier.notify("Hello World!")
        """
        # get default values if not provided
        heading = heading if heading is not None else self.heading
        icon = icon if icon is not None else self.icon
        time = time if time is not None else self.time
        sound = sound if sound is not None else self.sound

        self.dialog.notification(
            heading=heading,
            message=message,
            icon=icon,
            time=time,
            sound=sound,
        )
