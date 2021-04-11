
import json
import time

if __name__.startswith("scripts"):
    import sys
    sys.path.append("./scripts")

from datagatherer.miwrapper import MIApp

def get_cpu_reading( app: MIApp ) -> dict:
    """
    Method that returns a a reading of the CPU.
    **This function assumes that the system only has a single processor.**

    :param app: An initialized MIApp.
    :type app: MIApp
    :return: A dictionary containing CPU data
    :rtype: dict
    """
    processors = app.executeQuery(u"Win32_Processor", [u"Name", u"NumberOfCores", u"NumberOfLogicalProcessors", u"ThreadCount", u"VirtualizationFirmwareEnabled"])
    processors[0]["Cores"] = app.executeQuery(u"Win32_PerfFormattedData_PerfOS_Processor", [u"Name", u"PercentProcessorTime"])

    return {
        "timestamp": time.time(), 
        "processors": {
            "compressed": False,
            "data": processors
        }
    }