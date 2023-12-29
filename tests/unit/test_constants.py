# local imports
from src.themerr import constants


def test_name():
    assert constants.name == "Themerr"


def test_addon_type():
    assert constants.addon_type == "service"


def test_addon_id():
    assert constants.addon_id == "service.themerr"
