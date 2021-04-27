import json
from time import time
import datetime

class Notification(object):

    def __init__(self, notification_conf: dict) -> list:

        self.conf = notification_conf

    def parse(self, reading: dict) -> dict:
        """
        Processors
            PercentProcessorTime
        LogicalDisk
            DiskBytesPersec
            PercentFreeSpace
        Memory
            AvailableMBytes
        """ 
        if reading["type"] == "processors":
            return self.__processors(reading)
        elif reading["type"] == "logical_disks":
            return self.__logical_disk(reading)
        elif reading["type"] == "memory":
            return self.__memory(reading)
        else:
            return []

    def __processors(self, reading):
        
        cores = reading["data"][0]["Cores"]
        
        for core in cores:
            if core["Name"] == "_Total":
                total_perc_proc_time = core["PercentProcessorTime"]
                break

        notifs = []

        if "PercentProcessorTime" in self.conf:

            operator = self.conf["PercentProcessorTime"]["Comparison"]["operator"]
            comparison_value = self.conf["PercentProcessorTime"]["Comparison"]["value"]
            
            if self.__should_trigger(operator, total_perc_proc_time, comparison_value):
                notif = self.__generate_notif(reading, "PercentProcessorTime", total_perc_proc_time)
                notifs.append(notif)

        return notifs

    def __logical_disk(self, reading):
        
        disks = reading["data"]

        notifs = []

        if "PercentFreeSpace" in self.conf:

            for disk in disks:
                free_space = disk["PercentFreeSpace"]
                operator = self.conf["PercentFreeSpace"]["Comparison"]["operator"]
                comparison_value = self.conf["PercentFreeSpace"]["Comparison"]["value"]

                if self.__should_trigger(operator, free_space, comparison_value):
                    notif = self.__generate_notif(reading, "PercentFreeSpace", free_space)
                    notifs.append(notif)

        return notifs

    def __memory(self, reading):

        data = reading["data"]

        if "AvailableMBytes" in self.conf:
            
            notifs = []

            free_mem = data[0]["AvailableMBytes"]
            operator = self.conf["AvailableMBytes"]["Comparison"]["operator"]
            comparison_value = self.conf["AvailableMBytes"]["Comparison"]["value"]

            if self.__should_trigger(operator, free_mem, comparison_value):
                notif = self.__generate_notif(reading, "AvailableMBytes", free_mem)
                notifs.append(notif)
        
            return notifs

    def __should_trigger(self, operator, current_value, comparison_value):
        if operator == "<":
            return current_value < comparison_value
        elif operator == ">":
            return current_value > comparison_value
        elif operator == "<=":
            return current_value <= comparison_value
        elif operator == ">=":
            return current_value >= comparison_value
        elif operator == "=":
            return current_value == comparison_value
        elif operator == "!=":
            return current_value != comparison_value
        else:
            return False

    def __generate_notif(self, reading, notif_type, CausingValue):
        notif = {}
        notif["TimeStamp"] = datetime.datetime.fromtimestamp( int(time()) ).strftime('%Y-%m-%d %H:%M:%S')
        notif["Title"] = self.conf[notif_type]["Title"]
        notif["Content"] = self.conf[notif_type]["Content"]
        notif["CommunicationMethod"] = self.conf[notif_type]["CommunicationMethod"]
        notif["CausingValue"] = "{}".format(CausingValue)
        return notif
    