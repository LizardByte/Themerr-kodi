# kodi imports
import xbmc

# local imports
from . import logger
from . import settings


class ThemerrMonitor(xbmc.Monitor):
    """
    Kodi's monitor class.

    Creates a new monitor to notify addon about changes.

    Attributes
    ----------
    log : logging.Logger
        The logger of the ThemerrMonitor class.

    Methods
    -------
    abortRequested() -> bool
        Check if Kodi is requesting an abort.
    onSettingsChanged()
        Check if Kodi settings have been modified.

    Examples
    --------
    >>> monitor = ThemerrMonitor()
    """
    def __init__(self):
        super().__init__()
        self.log = logger.log

    def abortRequested(self) -> bool:
        """
        Check if Kodi is requesting an abort.

        Re-definition of the abortRequested method from xbmc.Monitor.

        Returns
        -------
        bool
            True if Kodi is requesting an abort, False otherwise.

        Examples
        --------
        >>> monitor = ThemerrMonitor()
        >>> monitor.abortRequested()
        False
        """
        return xbmc.Monitor.abortRequested(self)

    def onSettingsChanged(self):
        """
        Check if Kodi settings have been modified.

        This method is automatically called when Kodi settings have been modified.

        Examples
        --------
        >>> monitor = ThemerrMonitor()
        >>> monitor.onSettingsChanged()
        """
        self.log.debug("ThemerrMonitor: Settings have been modified")

        # reload the settings
        settings.settings = settings.Settings()
