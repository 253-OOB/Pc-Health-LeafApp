
import time
import json

from scripts.datagatherer.miwrapper import MIApp

from scripts.readings.get_cpu_reading import get_cpu_reading
from scripts.readings.get_logical_disk_reading import get_logical_disk_reading
from scripts.readings.get_memory_reading import get_memory_reading
from scripts.readings.get_video_controller_reading import get_video_controller_reading
from scripts.readings.get_process_and_thread_reading import get_process_and_thread_readings

from scripts.leafconf.leaf_config import read_config

config = read_config("config/leaf.json")

app = MIApp()


running_avg = 0
i = 1
while i<101:

    start = time.time()

    for query_function in config["configuration"]["queries"]:
        query_result = locals()[query_function](app) # Calls the query functions by their string names
        fp = open("data/" + query_function + ".json", "a")
        inp = json.dumps(query_result)
        if i < 100:
            inp += ","
        fp.write(inp)
        fp.close()

    end = time.time()

    running_avg += (end - start)

    print( "Current iteration: {}, Running Average: {}, ETA: {}".format(i, running_avg/i, (100-i) * (running_avg/i) ), end="\r" )

    i+=1

app.close()


