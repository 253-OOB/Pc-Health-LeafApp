
import json

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
        "videoController": {
            "compressed": False,
            "data": json.dumps(videoController)
        }
    }