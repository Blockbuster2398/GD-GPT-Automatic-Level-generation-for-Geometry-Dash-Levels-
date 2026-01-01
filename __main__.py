from classes.Level import GMD_Level
from pathlib import Path
from collections import defaultdict
from utils.ObjectMapping import ObjectMap


# level = GMD_Level("input_levels/color_test.gmd")

# level = GMD_Level("input_levels/nine_circles.gmd")
# print(level)
# print(level.tokens)
# level.create_gmd("output_levels/ten_circles.gmd", "ten_circles", "(10/10)")
with open("./resources/data_tokenized.txt", "r") as f:
    objects = GMD_Level.decode_tokens(f.read())
    print(objects)
    for i in objects: print(i)

level = GMD_Level("_", objects)
level.create_gmd("output_levels/square.gmd", "squares", "???")
