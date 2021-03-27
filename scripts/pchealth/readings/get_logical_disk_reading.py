
import json

from pchealth.readings.mireading.miclass import miApp

def get_logical_disk_reading(app: miApp) -> dict:
    """
    Method that returns a reading of the leaf **logical disks**.

    :param app: An initialized miApp.
    :type app: miApp
    :return: A dictionary containing **logical disk** data
    :rtype: dict
    """
    disks = app.executeQuery(u"Win32_LogicalDisk", [u"Name", u"FreeSpace", u"Size", u"FileSystem"])
    disk_perf = app.executeQuery(u"Win32_PerfFormattedData_PerfDisk_LogicalDisk", [u"Name", u"DiskBytesPersec", u"DiskReadBytesPersec", u"DiskWriteBytesPersec", u"PercentFreeSpace"])

    logical_disks = []
    for disk in disks:
        for perf in disk_perf:
            if disk["Name"] == perf["Name"]:
                disk["FreeSpace"] = disk["FreeSpace"] / pow(1024, 3) # Number represents 1GiB
                disk["Size"] = disk["Size"] / pow(1024, 3) # Number represents 1GiB
                logical_disks.append( disk | perf )
    
    return { 
        "logical_disks": {
            "compressed": False,
            "data": json.dumps(logical_disks)
        }
    }