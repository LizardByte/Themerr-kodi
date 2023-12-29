# standard imports
import os
import sys
from threading import Thread

# kodi imports
import xbmcvfs

# local imports
from . import constants
from . import logger
from . import monitor
from . import settings


class Themerr:
    """
    The Themerr class is the main class for the Themerr addon.

    This class is responsible for starting and terminating the addon.

    Attributes
    ----------
    log : logger.Logger
        The logger instance for the Themerr addon.
    monitor : monitor.ThemerrMonitor
        The monitor instance for the Themerr addon.
    settings : settings.Settings
        The settings instance for the Themerr addon.
    gui : gui.Window
        The gui instance for the Themerr addon.
    add_on : xbmcaddon.Addon
        The xbmcaddon.Addon instance for the Themerr addon.
    cwd : str
        The current working directory for the Themerr addon.
    lib_dir : str
        The lib directory for the Themerr addon.
    threads : list
        A list of threads for the Themerr addon.

    Methods
    -------
    start()
        Start the Themerr addon.
    terminate()
        Terminate the Themerr addon.

    Examples
    --------
    >>> Themerr().start()
    """
    def __init__(self):
        self.log = logger.Logger()
        self.monitor = monitor.ThemerrMonitor()
        self.settings = settings.Settings()
        self.gui = None
        self.add_on = self.settings.addon
        self.cwd = self.add_on.getAddonInfo('path')
        self.lib_dir = xbmcvfs.translatePath(os.path.join(self.cwd, 'resources', 'lib'))

        # add the lib directory to the python path
        if self.lib_dir not in sys.path:
            sys.path.insert(0, self.lib_dir)

        self.log.debug(f"Themerr lib directory: {self.lib_dir}")
        self.log.debug(f"Themerr cwd: {self.cwd}")
        for p in sys.path:
            self.log.debug(f"Themerr sys.path: {p}")

        self.threads = []

    def start(self):
        """
        Start the Themerr addon.

        The window watcher thread is started, then the addon waits for kodi to stop the addon.

        Examples
        --------
        >>> Themerr().start()
        """
        # this must be imported after the lib directory has been added to the python path
        from . import gui
        self.gui = gui.Window()

        self.log.debug(f"Starting {constants.name} Service {self.add_on.getAddonInfo('version')}")

        # start the window watcher
        window_watcher = Thread(
            name='ThemerrWindowWatcher',
            target=self.gui.window_watcher,
            daemon=True,  # terminate the thread when the main thread terminates
        )
        self.threads.append(window_watcher)
        window_watcher.start()

        # wait for the addon to be stopped by kodi
        self.monitor.waitForAbort()
        self.terminate()

    def terminate(self):
        """
        Terminate the Themerr addon.

        The monitor is deleted, then all threads are joined.

        Examples
        --------
        >>> Themerr().terminate()
        """
        self.log.debug(f"Terminating {constants.name} Service {self.add_on.getAddonInfo('version')}")

        del self.monitor

        # try to terminate all threads
        for thread in self.threads:
            thread.join()
