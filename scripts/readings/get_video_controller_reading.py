
import json
import time

if __name__.startswith("scripts"):
    import sys
    sys.path.append("./scripts")

from datagatherer.miwrapper import MIApp

def get_video_controller_reading(app: MIApp) -> dict:
    """
    Method that returns a reading of the leaf video controller.

    :param app: An initialized MIApp.
    :type app: MIApp
    :return: A dictionary containing video controller data
    :rtype: dict
    """

    videoController = app.executeQuery(u"Win32_VideoController", [u"Name"])

    return {
        "timestamp": time.time(),
        "videoController": {
            "compressed": False,
            "data": videoController
        }
    }