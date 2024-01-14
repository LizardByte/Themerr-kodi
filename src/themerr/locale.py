# standard imports
from gettext import pgettext


class Locale:
    """
    Locale class.

    This class is used to handle the localization of strings. Currently, it used only to extract strings from the
    ``settings.xml`` file.

    Methods
    -------
    settings()
        Get the strings used in the ``settings.xml`` file.

    Examples
    --------
    >>> Locale.settings()
    {30001: '...', ...}
    """
    @staticmethod
    def addon() -> dict:
        """
        Get the strings used in the addon.xml file.

        This method uses the ``pgettext`` function to extract the strings needed for the addon.xml file.
        Using ``pgettext`` allows us to add the msgctxt to the po file, which is needed for Kodi to find the correct
        translation.

        Returns
        -------
        dict
            Dictionary of strings used in the addon.xml file.

        Examples
        --------
        >>> Locale.addon()
        {"addon.extension.description": '...', ...}
        """
        strings = {
            "addon.extension.description": pgettext(
                "addon.extension.description",
                "Plugin for Kodi that adds theme songs to movies and tv shows using ThemerrDB."),
            "addon.extension.summary": pgettext(
                "addon.extension.summary",
                "Play theme songs while browsing movies"),
        }

        return strings

    @staticmethod
    def settings() -> dict:
        """
        Get the strings used in the ``settings.xml`` file.

        This method uses the ``pgettext`` function to extract the strings needed for the ``settings.xml`` file.
        Using ``pgettext`` allows us to add the msgctxt to the po file, which is needed for Kodi to find the correct
        translation.

        Returns
        -------
        dict
            Dictionary of strings used in the ``settings.xml`` file.

        Examples
        --------
        >>> Locale.settings()
        {30001: '...', ...}
        """
        strings = {
            31001: pgettext("#31001", "General"),
            31002: pgettext("#31002", "Theme timeout"),
            31003: pgettext("#31003", "Time to wait before playing or switching themes (in seconds)"),
            31004: pgettext("#31004", "Dev mode"),
            31005: pgettext("#31005", "Display log messages in Kodi's notification area"),
        }

        return strings
