# kodi imports
import xbmcaddon

# local imports
from . import constants


class Settings:
    """
    Settings class to access addon settings.

    This class is used to access addon settings.

    Attributes
    ----------
    addon : xbmcaddon.Addon
        addon instance

    Methods
    -------
    dev_mode()
        Get the dev mode setting.
    theme_timeout()
        Get the theme timeout setting.

    Examples
    --------
    >>> addon_settings = Settings()
    """
    def __init__(self):
        self.addon = xbmcaddon.Addon(id=constants.addon_id)

    def dev_mode(self) -> bool:
        """
        Get the dev mode setting.

        Get the dev mode setting from the addon settings.

        Returns
        -------
        bool
            The dev mode setting.

        Examples
        --------
        >>> addon_settings = Settings()
        >>> addon_settings.dev_mode()
        False
        """
        return self.addon.getSettingBool(id='devMode')

    def theme_timeout(self) -> int:
        """
        Get the theme timeout setting.

        Get the theme timeout setting from the addon settings.

        Returns
        -------
        int
            The theme timeout setting.

        Examples
        --------
        >>> addon_settings = Settings()
        >>> addon_settings.theme_timeout()
        3
        """
        return self.addon.getSettingInt(id='themeTimeout')


settings = Settings()
