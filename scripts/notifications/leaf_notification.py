

class NotificationTree():
    pass

class Notification(object):

    def __init__(self, notification_conf: dict) -> list:

        self.conf = notification_conf

    def parse( self, reading: dict ) -> list: 

        """
        Processors
            PercentProcessorTime
        LogicalDisk
            DiskBytesPersec
            PercentFreeSpace
        Memory
            AvailableMBytes
        """


        if "processors" in reading:
            self.__processors( reading )

    
    def __processors( self, reading ):
        pass