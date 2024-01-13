# standard imports
from datetime import datetime
import json
from typing import List, Optional, Set, Union

# lib imports
import requests

# kodi imports
import xbmc

# local imports
from . import logger
from . import monitor
from . import player
from . import settings


class Window:
    """
    A class to represent the Kodi window.

    This class watches for changes to the selected item in the Kodi window and starts/stops the theme accordingly.

    Parameters
    ----------
    player_instance : Optional[player.Player]
        A player instance to use for testing purposes.

    Attributes
    ----------
    log : logger.Logger
        The logger object.
    monitor : monitor.ThemerrMonitor
        The monitor object.
    player : player.Player
        The player object.
    item_selected_for : int
        The number of seconds the current item has been selected for.
    playing_item_not_selected_for : int
        The number of seconds the playing item has not been selected for.
    current_selected_item_id : Optional[int]
        The current selected item ID.
    last_selected_item_id : Optional[int]
        The last selected item ID.
    uuid_mapping : dict
        A mapping of uuids to YouTube URLs.
        The UUID will be the database type and the database ID, separated by an underscore. e.g. `tmdb_1`
        This is used to cache the YouTube URLs for faster lookups.

    Methods
    -------
    window_watcher()
        The main method that watches for changes to the Kodi window.
    pre_checks()
        Perform pre-checks before starting/stopping the theme.
    process_kodi_id(kodi_id: str)
        Process the Kodi ID and return a YouTube URL.
    process_movie(kodi_id: int)
        Process the Kodi ID and return a dictionary of IDs.
    find_youtube_url(kodi_id: str, db_type: str)
        Find the YouTube URL from the IDs.
    any_true(check: Optional[bool] = None, checks: Optional[Union[List[bool], Set[bool]]] = ())
        Determine if the check is True or if any of the checks are True.
    is_home()
        Determine if the Kodi window is the home screen.
    is_movies()
        Determine if the Kodi window is a movies screen.
    is_movie_set()
        Determine if the Kodi window is a movie set screen.
    is_tv_shows()
        Determine if the Kodi window is a TV shows screen.
    is_seasons()
        Determine if the Kodi window is a seasons screen.
    is_episodes()
        Determine if the Kodi window is an episodes screen.

    Examples
    --------
    >>> window = Window()
    >>> window.window_watcher()
    ...
    >>> window = Window(player_instance=player.Player())
    >>> window.window_watcher()
    """
    def __init__(self, player_instance=None):
        self.log = logger.log
        self.monitor = monitor.ThemerrMonitor()

        # allow providing a player for test purposes
        self.player = player_instance if player_instance else player.Player()

        self.item_selected_for = 0
        self.playing_item_not_selected_for = 0
        self.current_selected_item_id = None
        self.last_selected_item_id = None
        self.uuid_mapping = {}
        self.last_selected_show_id = None

        self._kodi_db_map = {
            'tmdb': 'themoviedb',
            'imdb': 'imdb',
        }
        self._supported_dbs = {
            'games': ['igdb'],
            'game_collections': ['igdb'],
            'game_franchises': ['igdb'],
            'movies': ['themoviedb', 'imdb'],
            'movie_collections': ['themoviedb'],
            'tv_shows': ['themoviedb'],
        }
        self._dbs = (
            'tmdb',
            'imdb',
            # 'igdb',  # placeholder for video game support
        )

    def window_watcher(self):
        """
        Watch the Kodi window for changes.

        This method is the main method that watches for changes to the Kodi window.

        Examples
        --------
        >>> window = Window()
        >>> window.window_watcher()
        """
        self.log.debug("Window watcher started")

        sleep_time = 50  # 50ms

        while not self.monitor.abortRequested():
            # put timeout_factor within the loop, so we can update it if the user changes the setting
            timeout_factor = settings.settings.theme_timeout()
            timeout = timeout_factor * (1000 / sleep_time)

            selected_title = xbmc.getInfoLabel("ListItem.Label")  # this is only used for logging

            kodi_id = None

            if self.is_seasons() or self.is_episodes():
                kodi_id = self.last_selected_show_id

            if not kodi_id:
                for db in self._dbs:
                    db_id = xbmc.getInfoLabel(f'ListItem.UniqueID({db})')
                    if db_id:
                        kodi_id = f"{db}_{db_id}"

                        if self.is_tv_shows():
                            # TheMovieDB TV Shows addon does not set uniqueID properly for seasons and episodes.
                            # So we will use the last selected TV show ID instead.
                            # See: https://github.com/xbmc/metadata.tvshows.themoviedb.org.python/issues/119
                            self.last_selected_show_id = kodi_id
                        break  # break on the first supported db

            # prefetch the YouTube url (if not already cached or cache is greater than 1 hour)
            if kodi_id and (kodi_id not in list(self.uuid_mapping.keys())
                            or (datetime.now().timestamp() - self.uuid_mapping[kodi_id]['timestamp']) > 3600):
                self.uuid_mapping[kodi_id] = {
                    'timestamp': datetime.now().timestamp(),
                    'youtube_url': self.process_kodi_id(kodi_id=kodi_id)
                }

            # this is used for our timeout counter
            xbmc.sleep(sleep_time)

            if not self.pre_checks():
                continue

            if kodi_id == self.current_selected_item_id:
                self.item_selected_for += 1
            else:
                self.item_selected_for = 0
                self.current_selected_item_id = kodi_id

            # Logic for stopping theme and potentially starting a new one
            if self.player.theme_is_playing:
                if self.player.theme_playing_kodi_id != kodi_id:
                    self.playing_item_not_selected_for += 1
                    if self.playing_item_not_selected_for >= timeout:
                        self.log.debug(f"Stopping theme due to {timeout} seconds of non-selection")
                        self.player.stop()
                        self.playing_item_not_selected_for = 0
                else:
                    self.playing_item_not_selected_for = 0
            if not self.player.theme_is_playing and self.item_selected_for >= timeout:
                if not self.uuid_mapping.get(kodi_id):
                    continue
                if not self.uuid_mapping[kodi_id].get('youtube_url'):
                    continue
                self.log.debug(f"Playing theme for {selected_title}, ID: {kodi_id}")
                self.player.play_url(
                    url=self.uuid_mapping[kodi_id]['youtube_url'],
                    kodi_id=kodi_id,
                )

        self.log.debug("Window watcher stopped")

    def pre_checks(self) -> bool:
        """
        Perform pre-checks before starting/stopping the theme.

        A series of checks are performed to determine if the theme should be played.

        Returns
        -------
        bool
            True if the theme should be played, otherwise False.

        Examples
        --------
        >>> window = Window()
        >>> window.pre_checks()
        True
        """
        try:
            playing_item = self.player.getPlayingFile()
            self.log.debug(f"playing item: {playing_item}")
        except RuntimeError:
            # we need to return now because item may not be playing even though the theme_playing_url was already set
            return True  # no item is playing

        # check if a video is playing
        if self.player.isPlayingVideo():
            self.log.debug("video is playing")
            return False

        # check if user started playing an item different that what we started playing
        if playing_item != self.player.theme_playing_url:
            self.log.debug(f"items are not equal, {playing_item} != {self.player.theme_playing_url}")
            self.player.reset()
            return False

        self.log.debug("pre-checks passed")
        return True

    def process_kodi_id(self, kodi_id: str) -> Optional[str]:
        """
        Generate YouTube URL from a given Kodi ID.

        This method takes a Kodi ID and returns a YouTube URL.

        Parameters
        ----------
        kodi_id : str
            The Kodi ID to process.

        Returns
        -------
        Optional[str]
            A YouTube URL if found, otherwise None.

        Examples
        --------
        >>> window = Window()
        >>> window.process_kodi_id(kodi_id='tmdb_1')
        """
        database_type = None
        if self.is_movies():
            database_type = 'movies'
        elif self.is_movie_set():
            database_type = 'movie_collections'
        elif self.is_tv_shows():
            database_type = 'tv_shows'
        elif self.is_episodes():
            database_type = 'tv_shows'
        elif self.is_seasons():
            database_type = 'tv_shows'

        if database_type:
            youtube_url = self.find_youtube_url(
                kodi_id=kodi_id,
                db_type=database_type,
            )

            return youtube_url

    def find_youtube_url(self, kodi_id: str, db_type: str) -> Optional[str]:
        """
        Find YouTube URL from the Dictionary of IDs.

        Given a dictionary of IDs, this method will query the Themerr DB to find the YouTube URL.

        Parameters
        ----------
        kodi_id : str
            The Kodi ID to process.
        db_type : str
            The database type.

        Returns
        -------
        Optional[str]
            A YouTube URL if found, otherwise None.

        Examples
        --------
        >>> window = Window()
        >>> window.find_youtube_url(kodi_id='tmdb_1', db_type='movies')
        """
        split_id = kodi_id.split('_')
        db = self._kodi_db_map[split_id[0]]

        if db_type not in self._supported_dbs.keys() or db not in self._supported_dbs[db_type]:
            return None

        db_id = split_id[1]

        self.log.debug(f"{db.upper()}_ID: {db_id}")
        themerr_db_url = f"https://app.lizardbyte.dev/ThemerrDB/{db_type}/{db}/{db_id}.json"
        self.log.debug(f"Themerr DB URL: {themerr_db_url}")

        try:
            response_data = requests.get(
                url=themerr_db_url,
            ).json()
        except requests.exceptions.RequestException as e:
            self.log.debug(f"Exception getting data from {themerr_db_url}: {e}")
        except json.decoder.JSONDecodeError:
            self.log.debug(f"Exception decoding JSON from {themerr_db_url}")
        else:
            youtube_theme_url = response_data['youtube_theme_url']
            self.log.debug(f"Youtube theme URL: {youtube_theme_url}")

            return youtube_theme_url

    @staticmethod
    def any_true(check: Optional[bool] = None, checks: Optional[Union[List[bool], Set[bool]]] = ()):
        """
        Determine if the check is True or if any of the checks are True.

        This method can be used to determine if at least one condition is True out of a list of multiple conditions.

        Parameters
        ----------
        check : Optional[bool]
            The check to perform.
        checks : Optional[List[bool]]
            The checks to perform.

        Returns
        -------
        bool
            True if any of the checks are True, otherwise False.

        Examples
        --------
        >>> Window().any_true(checks=[True, False, False])
        True
        >>> Window().any_true(checks=[False, False, False])
        False
        >>> Window().any_true(check=True)
        True
        >>> Window().any_true(check=False)
        False
        """
        if len(checks) == 0:
            return check

        for c in checks:
            if c:
                return True

        # if we get here, none of the checks were True
        return False

    def is_home(self) -> bool:
        """
        Check if the Kodi window is the home screen.

        This method uses ``xbmc.getCondVisibility()`` to determine if the Kodi window is the home screen.

        Returns
        -------
        bool
            True if the Kodi window is the home screen, otherwise False.

        Examples
        --------
        >>> Window().is_home()
        """
        return self.any_true(check=xbmc.getCondVisibility("Window.IsVisible(home)"))

    def is_movies(self) -> bool:
        """
        Check if the Kodi window is a movies screen.

        This method uses ``xbmc.getCondVisibility()`` and ``xbmc.getInfoLabel()`` to determine if the Kodi window is a
        movies screen.

        Returns
        -------
        bool
            True if the Kodi window is a movies screen, otherwise False.

        Examples
        --------
        >>> Window().is_movies()
        """
        return self.any_true(checks=[
            xbmc.getCondVisibility("Container.Content(movies)"),
            (xbmc.getInfoLabel("ListItem.DBTYPE") == 'movie'),
        ])

    def is_movie_set(self) -> bool:
        """
        Check if the Kodi window is a movie set screen.

        This method uses ``xbmc.getCondVisibility()`` and ``xbmc.getInfoLabel()`` to determine if the Kodi window is a
        movie set screen.

        Returns
        -------
        bool
            True if the Kodi window is a movie set screen, otherwise False.

        Examples
        --------
        >>> Window().is_movie_set()
        """
        # i.e. collections
        return self.any_true(check=xbmc.getCondVisibility("ListItem.IsCollection"))

    def is_tv_shows(self) -> bool:
        """
        Check if the Kodi window is a TV shows screen.

        This method uses ``xbmc.getCondVisibility()`` and ``xbmc.getInfoLabel()`` to determine if the Kodi window is a
        TV shows screen.

        Returns
        -------
        bool
            True if the Kodi window is a TV shows screen, otherwise False.

        Examples
        --------
        >>> Window().is_tv_shows()
        """
        return self.any_true(checks=[
            xbmc.getCondVisibility("Container.Content(tvshows)"),
            (xbmc.getInfoLabel("ListItem.DBTYPE") == 'tvshow'),
        ])

    def is_seasons(self) -> bool:
        """
        Check if the Kodi window is a seasons screen.

        This method uses ``xbmc.getCondVisibility()`` and ``xbmc.getInfoLabel()`` to determine if the Kodi window is a
        seasons screen.

        Returns
        -------
        bool
            True if the Kodi window is a seasons screen, otherwise False.

        Examples
        --------
        >>> Window().is_seasons()
        """
        return self.any_true(checks=[
            xbmc.getCondVisibility("Container.Content(Seasons)"),
            (xbmc.getInfoLabel("ListItem.DBTYPE") == 'season'),
        ])

    def is_episodes(self) -> bool:
        """
        Check if the Kodi window is an episodes screen.

        This method uses ``xbmc.getCondVisibility()`` and ``xbmc.getInfoLabel()`` to determine if the Kodi window is an
        episodes screen.

        Returns
        -------
        bool
            True if the Kodi window is an episodes screen, otherwise False.

        Examples
        --------
        >>> Window().is_episodes()
        """
        return self.any_true(checks=[
            xbmc.getCondVisibility("Container.Content(Episodes)"),
            (xbmc.getInfoLabel("ListItem.DBTYPE") == 'episode'),
        ])
