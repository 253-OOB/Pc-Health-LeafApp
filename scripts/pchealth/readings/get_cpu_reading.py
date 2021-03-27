
import json

from pchealth.readings.mireading.miclass import miApp

def get_cpu_reading( app: miApp ) -> dict:
    """
    Method that returns a a reading of the CPU.
    **This function assumes that the system only has a single processor.**

    :param app: An initialized miApp.
    :type app: miApp
    :return: A dictionary containing CPU data
    :rtype: dict
    """
    processors = app.executeQuery(u"Win32_Processor", [u"Name", u"NumberOfCores", u"NumberOfLogicalProcessors", u"ThreadCount", u"VirtualizationFirmwareEnabled"])
    processors[0]["Cores"] = app.executeQuery(u"Win32_PerfFormattedData_PerfOS_Processor", [u"Name", u"PercentProcessorTime"])
    
    return { 
        "processors": {
            "compressed": False,
            "data": json.dumps(processors)
        }
    }