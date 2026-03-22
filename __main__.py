from classes.Level import GMD_Level
from pathlib import Path
from collections import defaultdict
from utils.ObjectMapping import ObjectMap


# level = GMD_Level("input_levels/color_test.gmd")

# level = GMD_Level("input_levels/nine_circles.gmd")
# print(level)
# print(level.tokens)
# level.create_gmd("output_levels/ten_circles.gmd", "ten_circles", "(10/10)")

level = GMD_Level("input_levels_short/nine_circles.gmd")
# level = GMD_Level("input_levels/iceland.gmd")
level.create_tokens()
token_string = ";".join(level.tokens)
with open("resources/data_tokenized.txt", "w") as f:
    f.write(token_string)


with open("./resources/data_tokenized.txt", "r") as f:
    objects = GMD_Level.decode_tokens(f.read())
    # print(objects)

    level_reconstructed = GMD_Level("_", objects)
    level_reconstructed.create_gmd("output_levels/output3.22.26.gmd", "output31626", "???")
    print(f"Level reconstructed: {level_reconstructed}")


    # level = GMD_Level("input_levels/the spanish flee.gmd")
    # print(f"Level: {level}")
