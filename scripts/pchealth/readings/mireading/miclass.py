
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

    def executeQuery( self, wmiClass:str, wmiProperties:list ) -> list:

        attributes_string = ",".join(wmiProperties)

        query = self.session.exec_query(
            u"root\\cimv2",
            u"SELECT {} FROM {}".format(attributes_string, wmiClass)
        )

        result_dict = []
        
        while obj := query.get_next_instance():
            result_dict.append( xmltodict.parse(self.serializer.serialize_instance(obj)) )

        query.close()

        extractedData = self.__dataExtraction(result_dict, wmiProperties)
        
        result = self.__typeAssignment( extractedData )

        return result

    def __dataExtraction(self, extractedDict: dict, wmiProperties: list)->list:
        """
        Extracts the specified data from the wmi return string
        """


        extractedData = []

        for item in extractedDict:

            attribute_extractor = {}

            if type(item) != list:
                item = [item]

            for i in range( len(item) ):
                for prop in item[i]["INSTANCE"]["PROPERTY"]:
                    if prop["@NAME"] in wmiProperties:
                        if "VALUE" in prop.keys():
                            attribute_extractor[prop["@NAME"]] = {
                                "TYPE": prop["@TYPE"],
                                "VALUE": prop["VALUE"]
                            }

                extractedData.append( attribute_extractor ) 
    
        return extractedData

    def __typeAssignment(self, reading: list) -> list:
        '''
        Converts the type of each entry to its correct value.
        '''

        converted_readings = []
        for data in reading:
            
            converted_reading = {}

            for attribute in data:
                
                if data[attribute]['TYPE'] == 'string':
                    converted_reading[attribute] = data[attribute]["VALUE"] 

                elif data[attribute]['TYPE'] == 'uint32' or data[attribute]['TYPE'] == 'uint64' or data[attribute]['TYPE'] == 'uint16' or data[attribute]['TYPE'] == 'uint8':
                    converted_reading[attribute] =  int(data[attribute]["VALUE"])

                elif data[attribute]['TYPE'] == 'boolean':
                    
                    if data[attribute]['VALUE'] == 'false':
                        converted_reading[attribute] =  False
    
                    else:
                        converted_reading[attribute] =  True
    
                else:
                    raise TypeError( "In attribute {}, cannot convert the type {} yet, it should be implmented above.".format(attribute, data["TYPE"]) )
            converted_readings.append(converted_reading)
        
        return converted_readings

    def close(self) -> None:
        self.session.close()
        super().close()
