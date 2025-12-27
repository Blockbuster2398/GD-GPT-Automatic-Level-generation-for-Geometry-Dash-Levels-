import base64
import gzip
import zlib
import math
from operator import attrgetter

from classes.Object import GMD_Object
from utils.ObjectMapping import ObjectMap


class GMD_Level:

    # raw_string = None
    def __init__(self, path):
        self.objects_list = []
        self.plain_object_data = ""
        self.is_modified = False
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
        # For every object in data, add the object to the object list with data
        # print(self.plain_object_data)
        map = ObjectMap()
        for i in (range(len(self.plain_object_data))[1:-1]):
            object = self.plain_object_data[i]
            object_segmented = object.split(",")
            new_object = GMD_Object()
            new_object.sequence_order = i-1
            for j in range(int(len(object_segmented)/2)):
                # Initializes all normal attributes of the new object
                if int(object_segmented[j*2]) in map.key_to_attribute.keys():
                    new_object.details[map.key_to_attribute[int(object_segmented[j*2])]] = object_segmented[j*2+1]
                else:
                    self.is_modified = True
            self.objects_list.append((new_object))
        self.sort()
        # Initializes relative distances of objects
        x_distance = 0
        y_distance = 0
        for i in range(len(self.objects_list))[1:]:
            # If the difference between the objects has changed, change the distance between objects
            if float(self.objects_list[i].details["x_position"]) != float(self.objects_list[i-1].details["x_position"]):
                x_distance = float(self.objects_list[i].details["x_position"]) - float(self.objects_list[i-1].details["x_position"])
                x_distance = float(int(x_distance * 100)) / 100
            if float(self.objects_list[i].details["y_position"]) != float(self.objects_list[i-1].details["y_position"]):
                y_distance = float(self.objects_list[i].details["y_position"]) - float(self.objects_list[i-1].details["y_position"])
                y_distance = float(int(y_distance * 100)) / 100
            self.objects_list[i].details["x_distance"] = x_distance
            self.objects_list[i].details["y_distance"] = y_distance




    def __str__(self):
        to_string = ""
        for i in self.objects_list:
            to_string += ("\n" + str(i))
        to_string += f"\nIs Modified: {self.is_modified}"
        return to_string
    def sort(self):
        self.objects_list = sorted(
            self.objects_list,
            key=lambda GMDObject: (float(GMDObject.details['x_position']), float(GMDObject.details['y_position'])))
        for i in range(len(self.objects_list)):
            self.objects_list[i].sequence_order = i
    def create_gmd(self, filename, level_name, level_description):
        full_level_text = ""
        k4_prefix = ""
        k4_suffix = ""
        default_header = "kA13,0,kA15,0,kA16,0,kA14,,kA6,0,kA7,0,kA17,0,kA18,0,kS38,1,1,1,255,2,255,3,255,4,255,5,1,8,1"
        full_level_text += default_header + ";"
        for i in self.objects_list:
            full_level_text += i.to_gmd_format() + ";"
        # print(full_level_text)
        compressed_data = gzip.compress(full_level_text.encode("utf-8"))
        # print(compressed_data)
        encoded_b64 = base64.b64encode(compressed_data).decode("utf-8")
        # print(encoded_b64)
        gd_encoded_final = encoded_b64.replace('+', '-').replace('/', '_')
        # print(gd_encoded_final)
        xml_template = f"""<?xml version="1.0"?><plist version="1.0" gjver="2.0"><dict><k>kCEK</k><i>4</i><k>k1</k><i>11940</i><k>k18</k><i>13</i><k>k36</k><i>400</i><k>k85</k><i>128</i><k>k86</k><i>85</i><k>k87</k><i>2184369</i><k>k88</k><s>43,52,5</s><k>k89</k><t /><k>k23</k><i>3</i><k>k19</k><i>100</i><k>k71</k><i>100</i><k>k90</k><i>100</i><k>k26</k><i>3</i><k>k2</k><s>{level_name}</s><k>k3</k><s>{base64.b64encode(level_description.encode()).decode()}</s><k>k4</k><s>{gd_encoded_final}</s><k>k6</k><i>2565</i><k>k9</k><i>10</i><k>k10</k><i>20</i><k>k11</k><i>96949825</i><k>k22</k><i>4436974</i><k>k21</k><i>3</i><k>k16</k><i>1</i><k>k17</k><i>7</i><k>k83</k><i>823</i><k>k27</k><i>47</i><k>k50</k><i>45</i></dict></plist>"""
        # print(xml_template)
        with open(filename, "w") as f:
            f.write(xml_template)
        print(f"Created {filename}")

# level = GMD_Level("../input_levels/nine_circles.gmd")
# level.create_gmd("../output_levels/ten_circles.gmd", "ten_circles", "(10/10)")