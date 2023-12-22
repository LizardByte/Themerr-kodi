# kodi imports
import xbmc

# lib imports
import pytest

# local imports
from src.themerr import constants
from src.themerr import logger


@pytest.fixture(scope='module')
def logger_obj():
    """Create a logger object"""
    return logger.Logger()


def test_default_log(mock_xbmc_log, logger_obj):
    """Test log method"""
    message = 'Test message'
    logger_obj.log(msg=message)

    expected_message = f'{constants.name}: [DEBUG]: {message}'
    mock_xbmc_log.assert_called_once_with(
        msg=expected_message,
        level=xbmc.LOGDEBUG,
    )


@pytest.mark.parametrize('level', [
    xbmc.LOGDEBUG,
    xbmc.LOGINFO,
    xbmc.LOGWARNING,
    xbmc.LOGERROR,
    xbmc.LOGFATAL,
])
def test_log(mock_xbmc_log, logger_obj, level):
    """Test log method"""
    message = 'Test message'
    logger_obj.log(msg=message, level=level)

    expected_message = f'{constants.name}: [{logger_obj.level_mapper[level]}]: {message}'
    expected_level = xbmc.LOGDEBUG if level < xbmc.LOGDEBUG else level
    mock_xbmc_log.assert_called_once_with(
        msg=expected_message,
        level=expected_level,
    )


def test_debug(mock_xbmc_log, logger_obj):
    """Test debug method"""
    message = 'Test message'
    logger_obj.debug(msg=message)

    expected_message = f'{constants.name}: [DEBUG]: {message}'
    mock_xbmc_log.assert_called_once_with(
        msg=expected_message,
        level=xbmc.LOGDEBUG,
    )


def test_info(mock_xbmc_log, logger_obj):
    """Test info method"""
    message = 'Test message'
    logger_obj.info(msg=message)

    expected_message = f'{constants.name}: [INFO]: {message}'
    mock_xbmc_log.assert_called_once_with(
        msg=expected_message,
        level=xbmc.LOGINFO,
    )


def test_warning(mock_xbmc_log, logger_obj):
    """Test warning method"""
    message = 'Test message'
    logger_obj.warning(msg=message)

    expected_message = f'{constants.name}: [WARNING]: {message}'
    mock_xbmc_log.assert_called_once_with(
        msg=expected_message,
        level=xbmc.LOGWARNING,
    )


def test_error(mock_xbmc_log, logger_obj):
    """Test error method"""
    message = 'Test message'
    logger_obj.error(msg=message)

    expected_message = f'{constants.name}: [ERROR]: {message}'
    mock_xbmc_log.assert_called_once_with(
        msg=expected_message,
        level=xbmc.LOGERROR,
    )


def test_fatal(mock_xbmc_log, logger_obj):
    """Test fatal method"""
    message = 'Test message'
    logger_obj.fatal(msg=message)

    expected_message = f'{constants.name}: [FATAL]: {message}'
    mock_xbmc_log.assert_called_once_with(
        msg=expected_message,
        level=xbmc.LOGFATAL,
    )
