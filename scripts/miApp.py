
import mi
import time
import json
import xmltodict

# TODO: Write documentation
# TODO: If a Logical Disk does not have storage space (ex: USB Hub), no values will be shown, and the code will crash.

class miApp(mi.Application):
    
    def __init__(self):

        super().__init__()
        
        self.session = super().create_session(
            protocol=mi.PROTOCOL_WMIDCOM
        )
        
        self.serializer = super().create_serializer()

    def executeQuery( self, wmiClass:str, wmiProperties:list ) -> str:

        attributes_string = ""
        for i in range( len(wmiProperties) ):
            attributes_string += wmiProperties[i] + ","

        query = self.session.exec_query(
            u"root\\cimv2",
            u"SELECT {} FROM {}".format(attributes_string[:-1], wmiClass)
        )

        result = []

        while obj := query.get_next_instance():

            result_dict = xmltodict.parse(self.serializer.serialize_instance(obj))

            attribute_extractor = {}

            # It is possible to have a Logical Disk with no FreeSpace. It will appear with no value. This will crash the program.

            if type(result_dict) != list:
                result_dict = [result_dict]

            for i in range( len(result_dict) ):
                for prop in result_dict[i]["INSTANCE"]["PROPERTY"]:
                    if prop["@NAME"] in wmiProperties:
                        attribute_extractor = {
                            "NAME": prop["@NAME"],
                            "TYPE": prop["@TYPE"],
                            "VALUE": prop["VALUE"]
                        }

            result.append( attribute_extractor )

        query.close()

        return result

    def close(self) -> None:
        self.session.close()
        super().close()
