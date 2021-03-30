
import os.path
import time

from scripts.logger.leaf_logger import appLogger

from scripts.leafconf.leaf_config import read_config

from scripts.networking.leaf_networking import LeafNetworking
from scripts.networking.leaf_networking import InitialisationTokenException
from scripts.networking.leaf_networking import RefreshTokenException

from scripts.datagatherer.miwrapper import MIApp

from scripts.readings.get_cpu_reading import get_cpu_reading
from scripts.readings.get_logical_disk_reading import get_logical_disk_reading
from scripts.readings.get_memory_reading import get_memory_reading
from scripts.readings.get_video_controller_reading import get_video_controller_reading
from scripts.readings.get_process_and_thread_reading import get_process_and_thread_readings
 


if __name__ == "__main__":

    URL = "https://localhost:7071/api/fInitialiseLeaf"

    log = appLogger("logs/leaf")
    if os.path.isfile("config/leaf.json"):

        log.info("Started Application")

        app = MIApp()

        while True:

            config = read_config("config/leaf.json")

            if "init" in config:

                log.info("\"init\" found: attempting to initialise the leaf.")

                try:
                    print(config)
                    LeafNetworking.initialiseLeaf(URL, config["init"]["special_auth_token"])

                except ConnectionError:

                    log.error("Could not connect. Will try again in 5 min.")
                    time.sleep(60*5)

                except InitialisationTokenException:

                    log.critical( "Shutting down the leaf." )
                    exit(-1)

            else:

                log.info("Initialising application networking.")

                try:

                    network = LeafNetworking(URL, config["configuration"]["leaf_refresh_token"])

                except ConnectionError:

                    log.error("Could not connect. Will try again in 5 min.")
                    time.sleep(60*5)
                    continue

                except RefreshTokenException:

                    log.critical( "Shutting down the leaf." )
                    exit(-1)

                for query_function in config["configuration"]["rules"]["queries"]:
                    query_result = locals()[query_function](app) # Calls the query functions by their string names
                    network.send_to_root( query_result )

                time.sleep(60)

        app.close()

    else:
        # TODO: Send message on the open notification channel
        pass

    


    

# import os
# import time
# import getpass

# from proj09package.miclass import miApp

# app = miApp()

# time_stamp = time.time()
# computer_name = os.environ[u"COMPUTERNAME"]
# logged_in_user = getpass.getuser()
# cpu_per_core = app.executeQuery(u"Win32_PerfFormattedData_PerfOS_Processor", [u"Name", "PercentProcessorTime"])
# available_ram_memory_mbytes = app.executeQuery(u"Win32_PerfFormattedData_PerfOS_Memory", [u"AvailableMBytes"])
# total_ram_memory_bytes = app.executeQuery(u"Win32_ComputerSystem", [u"TotalPhysicalMemory"])
# disk_space = app.executeQuery(u"Win32_LogicalDisk", [u"FreeSpace", u"Size"])
# processes = app.executeQuery(u"Win32_PerfFormattedData_PerfProc_Process", [u"Name", u"IDProcess", u"PercentProcessorTime", u"ThreadCount"])
# cpu_temp = app.executeQuery(u"Win32_TemperatureProbe", [u"CurrentReading"])
# services = app.executeQuery(u"Win32_Service", [u"Name", u"Caption", u"Description", u"PathName", u"Started", u"State", u"Status"])
# primary_owner_name = app.executeQuery(u"Win32_ComputerSystem", [u"PrimaryOwnerName"])
# model_and_manufacturer = app.executeQuery(u"Win32_ComputerSystem", [u"Model", u"Manufacturer"])
# user_accounts = app.executeQuery(u"Win32_UserAccount", [u"Domain", u"Name", u"PasswordRequired", u"Disabled"])
# operating_system_attributes = app.executeQuery(u"Win32_OperatingSystem", [u"Caption", u"InstallDate", u"LastBootUpTime", "LocalDateTime", u"Name", u"OSArchitecture", u"SerialNumber", u"SystemDrive", u"Version"])
# drivers = app.executeQuery(u"Win32_SystemDriver", [u"Name", u"Caption", u"Description", u"PathName", u"ServiceType", u"State", u"Status"])

# program_files = []
# if os.path.exists("C:/Program Files"):
#     program_files.extend(os.listdir("C:/Program Files"))
# if os.path.exists("C:/Program Files (x86)"):
#     program_files.extend(os.listdir("C:/Program Files (x86)"))

# print("Queries took {:.3f} seconds.".format(time.time() - time_stamp))

# # print(time_stamp)
# # print(computer_name)
# # print(logged_in_user)
# # print(cpu_per_core)
# # print(available_ram_memory)
# # print(total_ram_memory_bytes)
# # print(disk_space)
# # print(processes)
# # print(cpu_temp)
# # print(services)
# # print(primary_owner_name)
# # print(model_and_manufacturer)
# # print(user_accounts)
# # print(operating_system_attributes)
# # print(drivers)
# # print(program_files)

# app.close()

# --------------------


# import requests
# import json
# import time
# import logging
# import os

# from proj09package.miclass import miApp

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s-[%(levelname)s]:%(message)s"
# )

# logging.info("Initializing the Application..")

# app = miApp()

# logging.info("Succesfully started the application.")

# while True:

#     logging.info("Gathering wmi data..")

#     json_data = {
#         "TIMESTAMP": time.time(),
#         "LEAFNAME": os.environ[u"COMPUTERNAME"],
#         "PROCESSORLOAD": app.executeQuery(u"Win32_Processor", [u"LoadPercentage"]),
#         "RAMUSAGE": app.executeQuery(u"Win32_PerfFormattedData_PerfOS_Memory", [u"AvailableMBytes"]),
#         "DISKUSAGE": app.executeQuery(u"Win32_LogicalDisk", [u"FreeSpace"])
#     }
    
#     logging.info("Successfully gathered WMI data.")

#     r = requests.post('https://41b93760208f.ngrok.io/api/PostToTable', json=json.dumps(json_data))
#     # r = requests.post('http://localhost:7071/api/PostToTable', json=json.dumps(json_data))

#     logging.info("Succesfully sent the data.")

#     time.sleep(10)

# app.close()

