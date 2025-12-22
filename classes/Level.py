import base64
import zlib

from classes.Object import GMD_Object
from utils.ObjectDetailMapping import ObjectMapping


class GMD_Level:
    objects_list = []
    plain_object_data = ""
    # raw_string = None
    def __init__(self, path):
        k4 = ""
        try:
            with open(path, "r") as file:
                content = file.read()
                # print(content)
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"An error occured: {e}")

        try:
            # Attempts to extract level object data from file contents
            # k4 = content.split("</s><k>k4</k><s>")[1].split("==")[0]
            k4 = content.split("</s><k>k4</k><s>")[1].split("</s>")[0]
        except IndexError:
            print("GMD file likely improperly formatted.")
        except Exception as e:
            print(f"An error occured: {e}")
        safe_string = k4.replace('-', '+').replace('_', '/')
        padding = len(safe_string) % 4
        if padding:
            safe_string += '=' * (4 - padding)
        compressed_data = base64.b64decode(safe_string)
        self.plain_object_data = zlib.decompress(compressed_data, 15 + 32).decode('utf-8').split(";")
        # print(self.plain_object_data)
        # For every object in data, add the object to the object list with data
        map = ObjectMapping()
        for i in range(len(self.plain_object_data))[1:]:
            object = self.plain_object_data[i]
            object_segmented = object.split(",")
            new_object = GMD_Object()

            for j in range(int(len(object_segmented)/2)):
                if int(object_segmented[j*2]) in map.key_to_attribute.keys():
                    new_object.details[map.key_to_attribute[int(object_segmented[j*2])]] = object_segmented[j*2+1]
                self.objects_list.append(new_object)
    def print_objects(self):
        for i in range(len(self.objects_list)):
            print(str(i) + "th object: " + str(self.objects_list[i]))


    def create_gmd(self, new_file_name):
        default_header = "kA13,0,kA15,0,kA16,0,kA14,,kA6,0,kA7,0,kA17,0,kA18,0,kS38,1,1,1,255,2,255,3,255,4,255,5,1,8,1"


