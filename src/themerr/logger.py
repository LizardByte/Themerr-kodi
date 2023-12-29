# kodi imports
import xbmc
import xbmcgui

# local imports
from . import constants
from . import notifier
from . import settings


class Logger(object):
    """
    Themerr's logger class.

    Creates a new logger to log to the Kodi log.

    Attributes
    ----------
    notifier : Notifier
        The notifier to use to display notifications to the user.
    icons : dict
        A dictionary mapping log levels to notification icons.
    level_mapper : dict
        A dictionary mapping log levels to strings.

    Methods
    -------
    log(msg: str, level: int = xbmc.LOGDEBUG)
        Log a message to the Kodi log.
    debug(msg: str)
        Log a debug message to the Kodi log.
    info(msg: str)
        Log an info message to the Kodi log.
    warning(msg: str)
        Log a warning message to the Kodi log.
    error(msg: str)
        Log an error message to the Kodi log.
    fatal(msg: str)
        Log a fatal message to the Kodi log.

    Examples
    --------
    >>> logger = Logger()
    """
    def __init__(self):
        self.notifier = notifier.Notifier()
        self.icons = {
            xbmc.LOGDEBUG: xbmcgui.NOTIFICATION_INFO,
            xbmc.LOGINFO: xbmcgui.NOTIFICATION_INFO,
            xbmc.LOGWARNING: xbmcgui.NOTIFICATION_WARNING,
            xbmc.LOGERROR: xbmcgui.NOTIFICATION_ERROR,
            xbmc.LOGFATAL: xbmcgui.NOTIFICATION_ERROR,
        }
        self.level_mapper = {
            xbmc.LOGDEBUG: "DEBUG",
            xbmc.LOGINFO: "INFO",
            xbmc.LOGWARNING: "WARNING",
            xbmc.LOGERROR: "ERROR",
            xbmc.LOGFATAL: "FATAL",
        }

    def log(self, msg: str, level: int = xbmc.LOGDEBUG):
        """
        Log a message to the Kodi log.

        This method will log a debug message to the Kodi log.
        The level parameter will be included in the log message.
        Additionally, a notification will be displayed to the user if the addon is in development mode.

        Parameters
        ----------
        msg : str
            The message to log.
        level : int
            The log level to log the message at.

        Examples
        --------
        >>> logger = Logger()
        >>> logger.log("This is a debug message", xbmc.LOGDEBUG)
        """
        xbmc.log(
            msg=f"{constants.name}: [{self.level_mapper[level]}]: {msg}",
            level=xbmc.LOGDEBUG if level < xbmc.LOGDEBUG else level,  # kodi doesn't want us to log below debug
        )

        if settings.settings.dev_mode():
            self.notifier.notify(
                message=msg,
                icon=self.icons[level],
            )

    def debug(self, msg: str):
        """
        Log a debug message to the Kodi log.

        Passes the message to the log method with the debug log level.

        Parameters
        ----------
        msg : str
            The message to log.

        Examples
        --------
        >>> logger = Logger()
        >>> logger.debug("This is a debug message")
        """
        self.log(msg=msg, level=xbmc.LOGDEBUG)

    def info(self, msg: str):
        """
        Log an info message to the Kodi log.

        Passes the message to the log method with the info log level.

        Parameters
        ----------
        msg : str
            The message to log.

        Examples
        --------
        >>> logger = Logger()
        >>> logger.info("This is an info message")
        """
        self.log(msg=msg, level=xbmc.LOGINFO)

    def warning(self, msg: str):
        """
        Log a warning message to the Kodi log.

        Passes the message to the log method with the warning log level.

        Parameters
        ----------
        msg : str
            The message to log.

        Examples
        --------
        >>> logger = Logger()
        >>> logger.warning("This is a warning message")
        """
        self.log(msg=msg, level=xbmc.LOGWARNING)

    def error(self, msg: str):
        """
        Log an error message to the Kodi log.

        Passes the message to the log method with the error log level.

        Parameters
        ----------
        msg : str
            The message to log.

        Examples
        --------
        >>> logger = Logger()
        >>> logger.error("This is an error message")
        """
        self.log(msg=msg, level=xbmc.LOGERROR)

    def fatal(self, msg: str):
        """
        Log a fatal message to the Kodi log.

        Passes the message to the log method with the fatal log level.

        Parameters
        ----------
        msg : str
            The message to log.

        Examples
        --------
        >>> logger = Logger()
        >>> logger.fatal("This is a fatal message")
        """
        self.log(msg=msg, level=xbmc.LOGFATAL)


log = Logger()
