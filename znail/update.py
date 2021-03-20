import os

_update_available = False


def update_available():
    global _update_available
    _update_available = True


def is_update_available():
    if "ZNAIL_FORCE_UPDATE_STATE" in os.environ:
        return os.environ["ZNAIL_FORCE_UPDATE_STATE"]
    return _update_available
