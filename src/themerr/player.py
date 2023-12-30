# standard imports
from typing import Optional

# kodi imports
import xbmc

# local imports
from . import logger
from . import youtube


class Player(xbmc.Player):
    """
    Kodi's player class.

    Creates a new player to control playback.

    Attributes
    ----------
    log : logging.Logger
        The logger for this class.
    theme_is_playing : bool
        True if a theme is currently playing, False otherwise.
    theme_is_playing_for : int
        The number of seconds the theme has been playing for.
    theme_playing_kodi_id : Optional[str]
        The Kodi ID of the theme currently playing.
    theme_playing_url : Optional[str]
        The URL of the theme currently playing.

    Methods
    -------
    ytdl_extract_url(url: str) -> Optional[str]
        Extract the audio URL from a YouTube URL.
    play_url(url: str, kodi_id: str, windowed: bool = False)
        Play a YouTube URL.
    stop()
        Stop playback.
    reset()
        Reset the player.

    Examples
    --------
    >>> player = Player()
    """
    def __init__(self):
        super().__init__()
        self.log = logger.log
        self.theme_is_playing = False
        self.theme_is_playing_for = 0
        self.theme_playing_kodi_id = None
        self.theme_playing_url = None

    @staticmethod
    def ytdl_extract_url(url: str) -> Optional[str]:
        mp3_url = youtube.process_youtube(url=url)
        return mp3_url if mp3_url else None

    def play_url(
            self,
            url: str,
            kodi_id: str,
            windowed: bool = False,
    ):
        """
        Play a YouTube URL.

        Given a user facing YouTube URL, extract the audio URL and play it.

        Parameters
        ----------
        url : str
            The url to play.
        kodi_id : str
            The Kodi ID of the item.
        windowed : bool
            True to play in a window, False otherwise.

        Examples
        --------
        >>> player = Player()
        >>> player.play_url(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", kodi_id='tmdb_1')
        """
        playable_url = self.ytdl_extract_url(url=url)
        if playable_url:
            self.play(item=playable_url, windowed=windowed)
            self.theme_is_playing = True
            self.theme_playing_kodi_id = kodi_id
            self.theme_playing_url = playable_url

    def stop(self):
        """
        Stop playback.

        This function will stop playback and reset the player.

        Examples
        --------
        >>> player = Player()
        >>> player.stop()
        """
        xbmc.Player.stop(self)
        self.reset()

    def reset(self):
        """
        Reset the player.

        Reset class variables to their default values.

        Examples
        --------
        >>> player = Player()
        >>> player.reset()
        """
        self.theme_is_playing = False
        self.theme_is_playing_for = 0
        self.theme_playing_kodi_id = None
        self.theme_playing_url = None
