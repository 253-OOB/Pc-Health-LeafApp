
import json

from pchealth.readings.mireading.miclass import miApp

def get_video_controller_reading(app: miApp) -> dict:
    """
    Method that returns a reading of the leaf video controller.

    :param app: An initialized miApp.
    :type app: miApp
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