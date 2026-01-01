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
        self.tokens = []
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
        self.map = ObjectMap()
        for i in (range(len(self.plain_object_data))[1:-1]):
            object = self.plain_object_data[i]
            object_segmented = object.split(",")
            new_object = GMD_Object()
            new_object.sequence_order = i-1
            for j in range(int(len(object_segmented)/2)):
                # Initializes all normal attributes of the new object
                if int(object_segmented[j*2]) in self.map.key_to_attribute.keys():
                    new_object.details[self.map.key_to_attribute[int(object_segmented[j*2])]] = object_segmented[j*2+1]
                else:
                    self.is_modified = True
            new_object.details["x_position"] = int(float(new_object.details["x_position"]))
            new_object.details["y_position"] = int(float(new_object.details["y_position"]))

            self.objects_list.append((new_object))
        self.sort()
        # Initializes relative distances of objects
        x_distance = 0
        y_distance = 0
        # Creates relative object distances
        for i in range(len(self.objects_list))[1:]:
            """# If the difference between the objects has changed, change the distance between objects
            if float(self.objects_list[i].details["x_position"]) != float(self.objects_list[i-1].details["x_position"]):
                x_distance = float(self.objects_list[i].details["x_position"]) - float(self.objects_list[i-1].details["x_position"])
                x_distance = float(int(x_distance * 100)) / 100
            if float(self.objects_list[i].details["y_position"]) != float(self.objects_list[i-1].details["y_position"]):
                y_distance = float(self.objects_list[i].details["y_position"]) - float(self.objects_list[i-1].details["y_position"])
                y_distance = float(int(y_distance * 100)) / 100
            self.objects_list[i].details["x_distance"] = int(x_distance)
            self.objects_list[i].details["y_distance"] = int(y_distance)"""

            self.objects_list[i].details["x_distance"] = self.objects_list[i].details["x_position"] - self.objects_list[i-1].details["x_position"]
            self.objects_list[i].details["y_distance"] = self.objects_list[i].details["y_position"] - self.objects_list[i-1].details["y_position"]

        self.create_tokens()
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

    def create_tokens(self):
        def get_90_rotation_spike(rotation, vFlip, hFlip):
            # Watch out for stupid infinite negative edge case
            rotation = int(rotation)
            vFlip = int(vFlip)
            hFlip = int(hFlip)
            # print(rotation)
            # print(f"hFlip: {hFlip}")
            # print(f"vFlip: {vFlip}")
            if rotation < 0: rotation = 360 + rotation
            # print(rotation)
            rotation = rotation - rotation % 90
            # print(rotation)
            if (rotation == 90 or rotation == 270):
                rotation += 180 * hFlip
            elif (rotation == 0 or rotation == 180):
                rotation += 180 * vFlip
            rotation = rotation - rotation % 90
            # print(rotation)
            return str(rotation)
        def get_180_rotation(rotation, vFlip):
            rotation = int(rotation)
            if rotation < 0: rotation = 360 + rotation
            rotation = rotation - rotation % 180
            rotation += 180 * int(vFlip)
            return str(rotation)

        def get_90_rotation_slope(rotation, vFlip, hFlip):
            rot = 0
            if (hFlip != 0 and vFlip == 0): rot += 90
            if (vFlip != 0 and hFlip == 0): rot += 270
            if (hFlip != 0 and vFlip != 0): rot += 180
            rotation = int(rotation)
            rotation = rotation - rotation % 90
            rotation += rot
            rotation = rotation % 360

            return str(rotation)

        tokens = []
        current_x_distance = 0
        tokens.append("start")
        # Fix deco not being added
        for i in self.objects_list:
            # handle dx dy tokens
            # print(i)
            if i.details["x_distance"] != None and i.details["x_distance"] > 0:
                tokens.append("x_increment" + str(i.details["x_distance"]))
            if i.details["y_distance"] != None:
                if i.details["y_distance"] > 0:
                    tokens.append("y_increment" + str(i.details["y_distance"]))
                elif i.details["y_distance"] < 0:
                    tokens.append("y_reset")


            # Handle object categorization

            # No rotational details
            if int(i.details["object_id"]) in (self.map.category_to_id['full_block']):
                tokens.append("full_block")
            elif int(i.details["object_id"]) in (self.map.category_to_id['mini_block']):
                tokens.append("mini_block")
            elif int(i.details["object_id"]) in (self.map.category_to_id['saw_mini']):
                tokens.append("saw_mini")
            elif int(i.details["object_id"]) in (self.map.category_to_id['saw_med']):
                tokens.append("saw_med")
            elif int(i.details["object_id"]) in (self.map.category_to_id['saw_large']):
                tokens.append("saw_large")

            elif int(i.details["object_id"]) in (self.map.category_to_id['x1_speed']):
                tokens.append("x1_speed")
            elif int(i.details["object_id"]) in (self.map.category_to_id['x2_speed']):
                tokens.append("x2_speed")
            elif int(i.details["object_id"]) in (self.map.category_to_id['x3_speed']):
                tokens.append("x3_speed")
            elif int(i.details["object_id"]) in (self.map.category_to_id['x4_speed']):
                tokens.append("x4_speed")

            elif int(i.details["object_id"]) in (self.map.category_to_id['green_orb']): tokens.append("green_orb")
            elif int(i.details["object_id"]) in (self.map.category_to_id['red_orb']):tokens.append("red_orb")
            elif int(i.details["object_id"]) in (self.map.category_to_id['black_orb']):tokens.append("black_orb")
            elif int(i.details["object_id"]) in (self.map.category_to_id['purple_orb']):tokens.append("purple_orb")
            elif int(i.details["object_id"]) in (self.map.category_to_id['yellow_orb']):tokens.append("yellow_orb")
            elif int(i.details["object_id"]) in (self.map.category_to_id['blue_orb']):tokens.append("blue_orb")

            elif int(i.details["object_id"]) in (self.map.category_to_id['blue_gravity']):tokens.append("blue_gravity")
            elif int(i.details["object_id"]) in (self.map.category_to_id['yellow_gravity']):tokens.append("yellow_gravity")
            elif int(i.details["object_id"]) in (self.map.category_to_id['cube_portal']):tokens.append("cube_portal")
            elif int(i.details["object_id"]) in (self.map.category_to_id['ship_portal']):tokens.append("ship_portal")
            elif int(i.details["object_id"]) in (self.map.category_to_id['ball_portal']):tokens.append("ball_portal")
            elif int(i.details["object_id"]) in (self.map.category_to_id['ufo_portal']):tokens.append("ufo_portal")
            elif int(i.details["object_id"]) in (self.map.category_to_id['wave_portal']):tokens.append("wave_portal")
            elif int(i.details["object_id"]) in (self.map.category_to_id['robot_portal']):tokens.append("robot_portal")
            elif int(i.details["object_id"]) in (self.map.category_to_id['spider_portal']):tokens.append("spider_portal")

            elif int(i.details["object_id"]) in (self.map.category_to_id['teleport_portal']):tokens.append("teleport_portal")

            elif int(i.details["object_id"]) in (self.map.category_to_id['green_size']):tokens.append("green_size")
            elif int(i.details["object_id"]) in (self.map.category_to_id['pink_size']):tokens.append("pink_size")

            elif int(i.details["object_id"]) in (self.map.category_to_id['start_dual']):tokens.append("start_dual")
            elif int(i.details["object_id"]) in (self.map.category_to_id['end_dual']):tokens.append("end_dual")

            elif int(i.details["object_id"]) in (self.map.category_to_id['orange_reflect']):tokens.append("orange_reflect")
            elif int(i.details["object_id"]) in (self.map.category_to_id['blue_reflect']):tokens.append("blue_reflect")

            # Require special logic

            # Half Blocks
            elif int(i.details["object_id"]) in (self.map.category_to_id['half_block']):
                tokens.append("half_block_" + get_180_rotation(i.details["rotation"], i.details["flip_vertical"]))
            # Pads
            elif int(i.details["object_id"]) in (self.map.category_to_id['red_pad']):
                tokens.append("red_pad_" + get_180_rotation(i.details["rotation"], i.details["flip_vertical"]))
            elif int(i.details["object_id"]) in (self.map.category_to_id['yellow_pad']):
                tokens.append("yellow_pad_" + get_180_rotation(i.details["rotation"], i.details["flip_vertical"]))
            elif int(i.details["object_id"]) in (self.map.category_to_id['blue_pad']):
                tokens.append("blue_pad_" + get_180_rotation(i.details["rotation"], i.details["flip_vertical"]))
            elif int(i.details["object_id"]) in (self.map.category_to_id['purple_pad']):
                tokens.append("purple_pad_" + get_180_rotation(i.details["rotation"], i.details["flip_vertical"]))

            # Spikes
            elif int(i.details["object_id"]) in (self.map.category_to_id['spike']):
                tokens.append("spike_" + get_90_rotation_spike(i.details["rotation"], i.details["flip_vertical"], i.details["flip_horizontal"]))
            elif int(i.details["object_id"]) in (self.map.category_to_id['spike_short']):
                tokens.append("spike_short_" + get_90_rotation_spike(i.details["rotation"], i.details["flip_vertical"], i.details["flip_horizontal"]))
            elif int(i.details["object_id"]) in (self.map.category_to_id['spike_mini']):
                tokens.append("spike_mini_" + get_90_rotation_spike(i.details["rotation"], i.details["flip_vertical"], i.details["flip_horizontal"]))

            # Slopes
            elif int(i.details["object_id"]) in (self.map.category_to_id['slope']):
                tokens.append("slope_" + get_90_rotation_slope(i.details["rotation"], i.details["flip_vertical"], i.details["flip_horizontal"]))
            elif int(i.details["object_id"]) in (self.map.category_to_id['slope_long']):
                tokens.append("slope_long_" + get_90_rotation_slope(i.details["rotation"], i.details["flip_vertical"], i.details["flip_horizontal"]))
            else:
                tokens.append("_")
        tokens.append("end")
        # print(tokens)
        self.tokens = tokens

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