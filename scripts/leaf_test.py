
import requests
import json
import time
import logging
import os

from miApp import miApp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s-[%(levelname)s]:%(message)s"
)

logging.info("Initializing the Application..")

app = miApp()

logging.info("Succesfully started the application.")

while True:

    logging.info("Gathering wmi data..")

    json_data = {
        "TIMESTAMP": int(time.time()),
        "LEAFNAME": os.environ[u"COMPUTERNAME"],
        "PROCESSORLOAD": app.executeQuery(u"Win32_Processor", [u"LoadPercentage"]),
        "RAMUSAGE": app.executeQuery(u"Win32_PerfFormattedData_PerfOS_Memory", [u"AvailableMBytes"]),
        "DISKUSAGE": app.executeQuery(u"Win32_LogicalDisk", [u"FreeSpace"])
    }
    
    logging.info("Successfully gathered WMI data.")

    r = requests.post('http://207.154.247.72:5000/leaf', json=json.dumps(json_data))

    logging.info("Succesfully sent the data.")

    time.sleep(1)

app.close()

