import json
from time import time


class NotificationTree():
    pass


class Notification(object):

    def __init__(self, notification_conf: dict) -> list:

        self.conf = notification_conf

    def parse(self, reading: dict) -> list:
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
            return self.__processors(reading)
        elif "logical_disks" in reading:
            return self.__logical_disk(reading)
        elif "memory" in reading:
            return self.__memory(reading)

    def __processors(self, reading):
        notifs = []
        data = json.loads(reading["processors"]["data"])
        cores = data[0]["Cores"]
        for core in cores:
            if core["Name"] == "_Total":
                total_perc_proc_time = core["PercentProcessorTime"]
                break
        operator = self.conf["notifications"]["PercentProcessorTime"]["Comparison"]["operator"]
        comparison_value = self.conf["notifications"]["PercentProcessorTime"]["Comparison"]["value"]
        if self.should_trigger(operator, total_perc_proc_time, comparison_value):
            notif = self.generate_notif(reading, "PercentProcessorTime")
            notifs.append(notif)
        return notifs

    def __logical_disk(self, reading):
        notifs = []
        data = json.loads(reading["logical_disks"]["data"])
        for disk in data:
            free_space = disk["PercentFreeSpace"]
            operator = self.conf["notifications"]["LogicalDisk"]["Comparison"]["operator"]
            comparison_value = self.conf["notifications"]["LogicalDisk"]["Comparison"]["value"]
            if self.should_trigger(operator, free_space, comparison_value):
                notif = self.generate_notif(reading, "LogicalDisk")
                notifs.append(notif)
        return notifs

    def __memory(self, reading):
        notifs = []
        data = json.loads(reading["memory"]["data"])
        free_mem = data[0]["AvailableMBytes"]
        operator = self.conf["notifications"]["Memory"]["Comparison"]["operator"]
        comparison_value = self.conf["notifications"]["Memory"]["Comparison"]["value"]
        if self.should_trigger(operator, free_mem, comparison_value):
            notif = self.generate_notif(reading, "Memory")
            notifs.append(notif)
        return notifs

    def should_trigger(self, operator, current_value, comparison_value):
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

    def generate_notif(self, reading, notif_type):
        notif = {}
        notif["TimeStamp"] = int(time())
        notif["Title"] = self.conf["notifications"][notif_type]["Title"]
        notif["Content"] = self.conf["notifications"][notif_type]["Content"]
        return notif


with open("get_logical_disk_reading.json") as f:
    cpu_data = json.load(f)
with open("leaf_sample.json") as f:
    config = json.load(f)


notif = Notification(config["configuration"]["rules"])
print(notif.parse(cpu_data))
