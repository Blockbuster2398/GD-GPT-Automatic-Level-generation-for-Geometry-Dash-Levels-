import base64
import gzip

# 1. DEFINE THE KEY MAP (Human Readable -> GD ID)
# This must match the keys you used in your parser
REVERSE_KEY_MAP = {
    'id': '1',
    'x': '2',
    'y': '3',
    'flip_h': '4',
    'flip_v': '5',
    'rotation': '6',
    'red': '7',
    'green': '8',
    'blue': '9',
    'duration': '10',
    'touch_trigger': '11',
    'editor_layer': '20',
    'color_1': '21',
    'color_2': '22',
    'z_layer': '24',
    'z_order': '25',
    'group': '57',
    'scale': '32'
}


def objects_to_string(object_list):
    """
    Converts a list of Python dictionaries back into a GD object string.
    e.g., [{'id': 1, 'x': 30}] -> "1,1,2,30"
    """
    obj_strings = []

    for obj in object_list:
        properties = []
        for key, value in obj.items():
            # Get the numeric GD ID (default to key if not in map)
            gd_key = REVERSE_KEY_MAP.get(key, key)

            # GD specific formatting: booleans are 1/0, floats need checking
            if isinstance(value, bool):
                value = '1' if value else '0'
            elif isinstance(value, float) and value.is_integer():
                value = int(value)  # GD prefers "30", not "30.0"

            properties.append(f"{gd_key},{value}")

        obj_strings.append(",".join(properties))

    print(";".join(obj_strings))
    return ";".join(obj_strings)


def create_level_string(header_string, object_list):
    """
    Combines the header and objects, compresses, and encodes them.
    """
    # 1. Build the raw text string
    # GD input_levels always end with a semicolon
    raw_body = objects_to_string(object_list)
    full_level_text = f"{header_string};{raw_body};"

    # 2. Gzip Compress
    # specific compress level isn't strictly required, but usually 6-9
    compressed_data = gzip.compress(full_level_text.encode('utf-8'))

    # 3. Base64 Encode
    b64_encoded = base64.b64encode(compressed_data).decode('utf-8')

    # 4. URL-Safe Replacement (GD specific)
    # Replace + with - and / with _
    gd_encoded = b64_encoded.replace('+', '-').replace('/', '_')

    return gd_encoded


def save_to_gmd(filename, level_name, level_desc, level_string):
    """
    Writes the XML structure for a .gmd file.
    """
    # This is a template based on the file structure you provided.
    # Note: k4 is the level string, k2 is the name.
    xml_template = f"""<?xml version="1.0"?><plist version="1.0" gjver="2.0"><dict><k>kCEK</k><i>4</i><k>k1</k><i>11940</i><k>k18</k><i>13</i><k>k36</k><i>400</i><k>k85</k><i>128</i><k>k86</k><i>85</i><k>k87</k><i>2184369</i><k>k88</k><s>43,52,5</s><k>k89</k><t /><k>k23</k><i>3</i><k>k19</k><i>100</i><k>k71</k><i>100</i><k>k90</k><i>100</i><k>k26</k><i>3</i><k>k2</k><s>{level_name}</s><k>k3</k><s>{base64.b64encode(level_desc.encode()).decode()}</s><k>k4</k><s>{level_string}</s><k>k6</k><i>2565</i><k>k9</k><i>10</i><k>k10</k><i>20</i><k>k11</k><i>96949825</i><k>k22</k><i>4436974</i><k>k21</k><i>3</i><k>k16</k><i>1</i><k>k17</k><i>7</i><k>k83</k><i>823</i><k>k27</k><i>47</i><k>k50</k><i>45</i></dict></plist>"""

    with open(filename, 'w') as f:
        f.write(xml_template)
    print(f"Successfully created {filename}")


# --- USAGE EXAMPLE ---

# 1. Define your new objects (Code Representation)
# Example: A line of spikes
new_objects = []

for i in range(15):
    new_objects.append({
        'id': 3,  # Spike ID
        'x': 100 + (i * 30),
        'y': 30,
        'group': 1
    })


# 2. Define the Level Header
# This string defines background, speed, song, etc.
# Ideally, keep the one from the file you decoded earlier.
# If you don't have one, this is a standard "Empty Level" header:
default_header = "kA13,0,kA15,0,kA16,0,kA14,,kA6,0,kA7,0,kA17,0,kA18,0,kS38,1,1,1,255,2,255,3,255,4,255,5,1,8,1"

# 3. Process
final_string = create_level_string(default_header, new_objects)

# 4. Save
save_to_gmd("new_level.gmd", "My PyLevel (Nightmare)", "Generated with Python", final_string)