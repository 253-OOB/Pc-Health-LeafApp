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

    :param leafToken: The particular refresh token associated with this leaf.
    :type leafToken: str     

    """

    def __init__( self, url: str, leafToken: str ):
        self.__url = url
        self.__leafToken = leafToken

    def send_to_root( self, data: dict ):
        """Sends data to the server

        :param data: Data to send to the server
        :type data: str
        :raises RefreshTokenException: Occurs when the token is deemed to be invalid.
        :raises ConnectionError: Occurs when the leaf cannot connect to the server. 
        """

        data["leaftoken"] = self.__leafToken

        payload = {
            "LeafToken": self.__leafToken,
            "Data": data
        }

        res = requests.post( self.__url + 'fSendLeafData', data=json.dumps(payload) )

        if res.status_code == 200:
            pass
            # resData = res.json()
            # Handle cases where the server might want to return updates.
            
        elif res.status_code == 403:

            raise RefreshTokenException("There was a problem with the refresh token.")

        else:
            log.error(res.status_code)
            raise ConnectionError("There was a problem accessing the server. Please retry after a moment.")            

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

        res = requests.post(url + "fInitialiseLeaf/default.json", data=json.dumps(payload), verify=False)

        if res.status_code == 200:

            log.info( "Successfully initialised the leaf on the server." )

            print(res.status_code)
            data = res.json()

            conf = json.loads(data["Configuration"])
            conf["configuration"]["leaf_refresh_token"] = data["RefreshToken"]

            override_config( conf )

            log.info("Successfully installed the new configuration.")

        elif res.status_code == 403:

            raise InitialisationTokenException("There was a problem with the initialisation token.")
        
        else:
            log.error(res.status_code)
            raise ConnectionError("Connection error. Please try again.")