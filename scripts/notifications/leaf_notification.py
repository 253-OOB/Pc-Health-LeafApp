from time import time


class NotificationTree():
    pass


class Notification(object):

    """
    {
        "LeafID": 1,
        "OrganisationID": 3,
        "Title": "TestTitle",
        "TimeStamp": 1618496385,
        "Content": "TestContent",
        "CausingValue": "TestCausingValue",
        "CommunicationMethod": "sms"
    }
    """

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
            self.__processors(reading)
        elif "logical_disks" in reading:
            self.__logical_disk(reading)
        elif "memory" in reading:
            self.__memory(reading)

    def __processors(self, reading):
        notifs = []
        cores = reading["data"][0]["Cores"]
        for core in cores:
            if core["Name"] == "_Total":
                total_perc_proc_time = core["PercentProcessorTime"]
                break
        operator = self.conf["notifications"]["PercentProcessorTime"]["Comparison"]["operator"]
        comparison_value = self.conf["notifications"]["PercentProcessorTime"]["Comparison"]["value"]
        if should_trigger(operator, total_perc_proc_time, comparison_value):
            notif = generate_notif(reading, "PercentProcessorTime")
            notifs.append(notif)
        return notifs

    def __logical_disk(self, reading):
        notifs = []
        for disk in reading["data"]:
            free_space = disk["PercentFreeSpace"]
            operator = self.conf["notifications"]["LogicalDisk"]["Comparison"]["operator"]
            comparison_value = self.conf["notifications"]["LogicalDisk"]["Comparison"]["value"]
            if should_trigger(operator, free_space, comparison_value):
                notif = generate_notif(reading, "LogicalDisk")
                notifs.append(notif)
        return notifs

    def __memory(self, reading):
        notifs = []
        free_mem = reading["data"][0]["AvailableMBytes"]
        operator = self.conf["notifications"]["Memory"]["Comparison"]["operator"]
        comparison_value = self.conf["notifications"]["Memory"]["Comparison"]["value"]
        if should_trigger(operator, free_mem, comparison_value):
            notif = generate_notif(reading, "Memory")
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
