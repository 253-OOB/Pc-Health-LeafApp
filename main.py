
import os.path
import time

from scripts.logger.leaf_logger import appLogger

from scripts.leafconf.leaf_config import read_config
from scripts.leafconf.leaf_config import override_config

from scripts.networking.leaf_networking import LeafNetworking
from scripts.networking.leaf_networking import InitialisationTokenException
from scripts.networking.leaf_networking import RefreshTokenException

from scripts.datagatherer.miwrapper import MIApp

from scripts.readings.get_cpu_reading import get_cpu_reading
from scripts.readings.get_logical_disk_reading import get_logical_disk_reading
from scripts.readings.get_memory_reading import get_memory_reading
from scripts.readings.get_video_controller_reading import get_video_controller_reading
from scripts.readings.get_process_and_thread_reading import get_process_and_thread_readings
 
from scripts.notifications.leaf_notification import Notification

if __name__ == "__main__":

    # URL = "https://pchealth-leaf.azurewebsites.net/api/"
    URL = 'http://localhost:7071/api/'
    
    log = appLogger("logs/leaf")
    
    if os.path.isfile("config/leaf.json"):

        log.info("Started Application")

        app = MIApp()

        while True:

            config = read_config("config/leaf.json")

            if "init" in config:

                log.info("\"init\" found: attempting to initialise the leaf.")

                try:
                    LeafNetworking.initialiseLeaf(URL, config["init"]["special_auth_token"])

                except ConnectionError:

                    log.error("Initialisation: Could not connect to the server. Will try again in 5 min.")
                    time.sleep(60*5)

                except InitialisationTokenException:

                    log.critical( "The leaf cannot be intialised." )
                    log.critical( "The initialisation token is either wrong or expired" )
                    log.critical( "Shutting down the leaf." )
                    exit(-1)

            else:

                log.info("Initialising application networking.")

                try:

                    network = LeafNetworking(URL, config["configuration"]["leaf_refresh_token"])
                    

                except ConnectionError:

                    log.error("Connection: Could not connect to the server. Will try again in 5 min.")
                    time.sleep(60*5)
                    continue

                except RefreshTokenException:
                            
                    log.critical( "The refresh token token is wrong." )
                    log.critical( "Shutting down the leaf." )
                    exit(-1)

                notificationChecker = Notification( config["configuration"]["rules"]["notifications"] )

                for query_function in config["configuration"]["rules"]["queries"]:
                    query_result = locals()[query_function](app) # Calls the query functions by their string names
                    
                    res = network.send_to_root( query_result, config["configuration"]["rules"]["lastNotificationUpdate"] )

                    if ("notifications" in res) and ("_ts" in res):
                        
                        notifications = {}
                        
                        for notif in res["notifications"]:
                            for notifType in notif:
                                notifications[notifType] = notif[notifType] 
                        
                        config["configuration"]["rules"]["notifications"] = notifications
                        config["configuration"]["rules"]["lastNotificationUpdate"] = res["_ts"]

                        override_config( config )

                        continue

                    notificationList = notificationChecker.parse( query_result )
                    if len(notificationList) != 0:
                        network.send_notification_to_root( notificationList )

                time.sleep(60)

        app.close()

    else:
        pass