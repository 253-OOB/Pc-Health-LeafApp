
import json
import zlib

from pchealth.readings.mireading.miclass import miApp

def get_process_and_thread_readings( app: miApp ) -> dict:
    """
    Method that returns a reading of the leaf processes coupled with their associated threads.

    :param app: An initialized miApp.
    :type app: miApp
    :return: A dictionary containing process data
    :rtype: dict
    """
    processes = app.executeQuery(u"Win32_PerfFormattedData_PerfProc_Process", [u"Name", u"IDProcess", u"IODataBytesPersec", u"IOReadBytesPersec", u"IOWriteBytesPersec", u"PageFaultsPersec", u"PercentProcessorTime", u"ThreadCount", u"WorkingSet"])
    
    threads = app.executeQuery(u"Win32_PerfFormattedData_PerfProc_Thread", [u"Name", u"IDThread", u"IDProcess", u"PercentProcessorTime", u"ThreadState" ])

    processes.append({"Name": "Other - Lone Threads", "IDProcess": -1, "WorkingSet": 0})

    processes_and_threads = []

    for i in range( len(processes) ):

        if processes[i]["Name"] == "_Total":
            processes[i]["IDProcess"] = -1

        processes[i]["WorkingSet"] = processes[i]["WorkingSet"] / 1024 # Return Value in KiB
        
    # Veryyyyy sloowww operation must be improved
    
    for i in range( len(processes) ):

        processes[i]["Threads"] = []

        for j in range( len(threads) ):

            if processes[i]["IDProcess"] == threads[j]["IDProcess"]:
                processes[i]["Threads"].append(threads[j])

        processes_and_threads.append(processes[i])


    threadState = ["Initialized", "Ready", "Running", "Standby", "Terminated", "Wait", "Transition", "Unknown"]

    for i in range(len(processes_and_threads)):
        for j in range(len(processes_and_threads[i]["Threads"])):

            del processes_and_threads[i]["Threads"][j]["IDProcess"]

            state = processes_and_threads[i]["Threads"][j]["ThreadState"]
            del processes_and_threads[i]["Threads"][j]["ThreadState"]
            processes_and_threads[i]["Threads"][j]["ThreadState"] = threadState[state]
            
    compressed = zlib.compress(json.dumps(processes_and_threads).encode("utf8"))
    
    return { 
        "processes": {
            "compressed": True,
            "data": compressed
        }
    }
