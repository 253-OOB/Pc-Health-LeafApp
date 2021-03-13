
import os
import time
import getpass

from miApp import miApp

app = miApp()

time_stamp = time.time()
computer_name = os.environ[u"COMPUTERNAME"]
logged_in_user = getpass.getuser()
cpu_per_core = app.executeQuery(u"Win32_PerfFormattedData_PerfOS_Processor", [u"Name", "PercentProcessorTime"])
available_ram_memory_mbytes = app.executeQuery(u"Win32_PerfFormattedData_PerfOS_Memory", [u"AvailableMBytes"])
total_ram_memory_bytes = app.executeQuery(u"Win32_ComputerSystem", [u"TotalPhysicalMemory"])
disk_free_space = app.executeQuery(u"Win32_LogicalDisk", [u"FreeSpace"])
processes = app.executeQuery(u"Win32_PerfFormattedData_PerfProc_Process", [u"Name", u"IDProcess", u"PercentProcessorTime", u"ThreadCount"])
cpu_temp = app.executeQuery(u"Win32_TemperatureProbe", [u"CurrentReading"])
services = app.executeQuery(u"Win32_Service", [u"Name", u"Caption", u"Description", u"PathName", u"Started", u"State", u"Status"])
primary_owner_name = app.executeQuery(u"Win32_ComputerSystem", [u"PrimaryOwnerName"])
model_and_manufacturer = app.executeQuery(u"Win32_ComputerSystem", [u"Model", u"Manufacturer"])
user_accounts = app.executeQuery(u"Win32_UserAccount", [u"Domain", u"Name", u"PasswordRequired", u"Disabled"])
operating_system_attributes = app.executeQuery(u"Win32_OperatingSystem", [u"Caption", u"InstallDate", u"LastBootUpTime", "LocalDateTime", u"Name", u"OSArchitecture", u"SerialNumber", u"SystemDrive", u"Version"])
drivers = app.executeQuery(u"Win32_SystemDriver", [u"Name", u"Caption", u"Description", u"PathName", u"ServiceType", u"State", u"Status"])

program_files = []
if os.path.exists("C:/Program Files"):
    program_files.extend(os.listdir("C:/Program Files"))
if os.path.exists("C:/Program Files (x86)"):
    program_files.extend(os.listdir("C:/Program Files (x86)"))

print("Queries took {:.3f} seconds.".format(time.time() - time_stamp))

# print(time_stamp)
# print(computer_name)
# print(logged_in_user)
# print(cpu_per_core)
# print(available_ram_memory)
# print(total_ram_memory_bytes)
# print(disk_free_space)
# print(processes)
# print(cpu_temp)
# print(services)
# print(primary_owner_name)
# print(model_and_manufacturer)
# print(user_accounts)
# print(operating_system_attributes)
# print(drivers)
# print(program_files)

app.close()