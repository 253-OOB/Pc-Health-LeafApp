
import json

from pchealth.readings.mireading.miclass import miApp

def get_memory_reading(app: miApp) -> dict:
    """
    Method that returns a reading of the leaf RAM.

    :param app: An initialized miApp.
    :type app: miApp
    :return: A dictionary containing RAM data
    :rtype: dict
    """
    memory_sticks = app.executeQuery(u"Win32_PhysicalMemory", [u"Capacity"])

    TotalPhysicalMemory = 0    
    for stick in memory_sticks:
        TotalPhysicalMemory += stick["Capacity"]

    memory = app.executeQuery(u"Win32_PerfFormattedData_PerfOS_Memory", [u"AvailableMBytes", u"PageFaultsPersec"])

    memory[0]["AvailableMBytes"] = memory[0]["AvailableMBytes"]/1024
    memory[0]["TotalMemory"] = TotalPhysicalMemory/pow(1024, 3) # Number represents 1GiB

    return { 
        "memory": {
            "compressed": False,
            "data": json.dumps(memory)
        }
    }