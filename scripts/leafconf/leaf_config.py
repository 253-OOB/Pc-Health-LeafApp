
import json

def override_config( jsonData: dict ):
    """Function to override the content of the leaf.json config file

    :param jsonData: The json data that you want to override the leaf.json file with.
    :type jsonData: dict
    """

    fp = open("config/leaf.json", "w")
    fp.write( json.dumps(jsonData) )
    fp.close()

def read_config( path: str ):
    """Retrieves the contents of the leaf.json config file and converts it to a dictionary.

    :param path: Path to the json file.
    :type path: str

    :return: A dictionary containing the configuration of a leaf.
    :rtype: dict
    """

    fp = open(path, "r")
    data = json.load(fp)
    fp.close()

    return data