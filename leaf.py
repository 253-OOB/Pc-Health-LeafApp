import os
import wmi
import time
import json
import requests

from typing import List
from typing import Dict

def pymi_to_dict(pymi_obj: wmi._Instance) -> Dict[str, str]:
    """
    Convert a PyMI object to a dict of attributes.

    Arguments:
        pymi_obj (wmi._Instance): The PyMI instance object that contains the attributes.

    e.g.
    
    {'Name': 'C:', 'Size': '1234567', 'FreeSpace': '123456'}

    Returns:
        attributes (Dict[str, str]): The dict of attributes and values that make up the PyMI object.
    """
    attributes = {}
    instance = pymi_obj._instance
    for i in range(len(instance)):
        elem = instance.get_element(i)
        name = str(elem[0])
        value = str(elem[2])
        attributes[name] = value
    return attributes

def query(conn: wmi._Connection, cls: str, attributes: List[str] = []) -> List[Dict[str, str]]:
    """
    Query a WMI class and return all or specified attributes.

    Select the attributes specified in the `attributes` list. If empty, select all.

    e.g.

    [
        {'Name': 'C:', 'Size': '1234567', 'FreeSpace': '123456'}, 
        {'Name': 'D:', 'Size': '1234567', 'FreeSpace': '123456'}
    ]
    
    Arguments:
        conn (wmi._Connection): The WMI object.
        cls (str): The class to query.
        attributes (List[str]): The list of attributes to select from the query. If empty select all.

    Returns:
        data (List[Dict[str, str]]): The query result as a list of rows, each a dict of attributes.
    """
    data = []
    for q in conn.query("select * from " + cls):
        d = pymi_to_dict(q)
        if attributes:
            d = {attr: d[attr] for attr in attributes} # Select attributes
        data.append(d)
    return data

while True:
    time_stamp = int(time.time())

    conn = wmi.WMI()

    disk_usage = query(conn, "Win32_LogicalDisk", ["Name", "Size", "FreeSpace"])
    free_memory = query(conn, "Win32_PerfFormattedData_PerfOS_Memory", ["AvailableMBytes"])
    load_percentage = query(conn, "Win32_Processor", ["LoadPercentage"])
    computer_name = os.environ['COMPUTERNAME']
    
    output_dict = {"timestamp": str(time_stamp), "LeafNames": [computer_name], "RAM": [free_memory], "Disk": [disk_usage], "CurrentLoadPercentage": [load_percentage]}

    print(output_dict)

    r = requests.post('http://207.154.247.72:5000/leaf', json=output_dict)

    time.sleep(1)

