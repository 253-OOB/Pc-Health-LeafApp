import os
import requests
import time
import json

if __name__.startswith("scripts"):
    import sys
    sys.path.append("./scripts")

from logger.leaf_logger import appLogger
from leafconf.leaf_config import override_config

log = appLogger("logs/leaf")

class RefreshTokenException(Exception):
    """
    Raised when the server returns a 403 error after being sent a refresh token.
    An error notification should be sent to the admin to notify him of the configuration error
    """
    pass

class InitialisationTokenException(Exception):
    """
    Raised when the server returns a 403 error after being sent an initialisation token.
    An error notification should be sent to the admin to notify him of the configuration error.
    """
    pass

class LeafNetworking(object):
    """
    Create a new LeadfNetworking instance.

    :param url: The url to which data should be sent.
    :type url: str

    :param refreshToken: The particular refresh token associated with this leaf.
    :type refreshToken: str

    :raises RefreshTokenException: Occurs when the token is deemed to be invalid.
    :raises ConnectionError: Occurs when the leaf cannot connect to the server.       

    """


    def __init__( self, url: str, refreshToken: str ):

        self.__url = url

        self.__refreshToken = refreshToken

        # res = requests.post(self.__url, {
        #     "RefreshToken": self.__refreshToken
        # }, verify=False)

        # if res.status_code == 200:

        #     # Connection was successful the accessToken was gathered.
        #     self.__accessToken = res.json()["AccessToken"]
        
        # elif res.status_code == 403:

        #     # In this case an email will be sent to the admin notifying him that there was configuration error with the leaf.
        #     # TODO Log this as a critical error.
        #     raise RefreshTokenException( "There was a problem with the refresh token." )

        # else:

        #     # In this case the caller should retry after a moment
        #     # TODO Log this error as an error
        #     raise ConnectionError("There was a problem accessing the server. Please retry after a moment.")
        

    def send_to_root( self, data: dict ):
        """Sends data to the server

        :param data: Data to send to the server
        :type data: str
        :raises RefreshTokenException: Occurs when the token is deemed to be invalid.
        :raises ConnectionError: Occurs when the leaf cannot connect to the server. 
        """

        print(data)

        # payload = {

        #     "AccessToken": self.__accessToken,
        #     "RefreshToken": self.__refreshToken,
        #     "Timestamp": time.time(),
        #     "Data": data

        # }

        # res = requests.post( self.__url, data=payload )

        # if res.status_code == 200:

        #     resData = res.json()

        #     if "AccessToken" in resData:
        #         self.__accessToken = resData["AccessToken"]

        # elif res.status_code == 403:

        #     log.critical( "The refresh token token is wrong." )
        #     raise RefreshTokenException("There was a problem with the refresh token.")

        # else:

        #     raise ConnectionError("There was a problem accessing the server. Please retry after a moment.")            

    @staticmethod
    def openChannelNotification( ):
        """
        Send an open channel notification.

        Only use this method when you cannot authorize this leaf through the regular channels.
        """
        # TODO 

        pass
    
    @staticmethod
    def initialiseLeaf( url, initialisationToken):
        """
        Function to initialise a new leaf.
        
        After a successful initialisation, a new configuration file will be installed.

        :param url: The url to connect to.
        :type url: str
        :param initialisationToken: The initialisation token (In the leaf.json file).
        :type initialisationToken: str
        """

        payload = {
            "InitialisationToken": initialisationToken,
            "ComputerName": os.environ["COMPUTERNAME"]
        }

        log.info("Sending initialisation data.")

        res = requests.post(url + "/default.json", data=json.dumps(payload), verify=False)

        if res.status_code == 200:

            log.info( "Successfully initialised the leaf on the server." )

            print(res.status_code)
            data = res.json()

            conf = json.loads(data["Configuration"])
            conf["configuration"]["leaf_refresh_token"] = data["RefreshToken"]

            override_config( conf )

            log.info("Successfully installed the new configuration.")

        elif res.status_code == 403:

            log.critical( "The leaf cannot be intialised." )
            log.critical( "The initialisation token is either wrong or expired" )

            raise InitialisationTokenException("There was a problem with the initialisation token.")
        
        else:
            raise ConnectionError("Connection error. Please try again.")