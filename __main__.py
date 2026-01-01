from classes.Level import GMD_Level
from pathlib import Path
from utils.ObjectMapping import ObjectMap


# level = GMD_Level("input_levels/color_test.gmd")

level = GMD_Level("input_levels/nine_circles.gmd")
# print(level)
# level.create_gmd("output_levels/ten_circles.gmd", "ten_circles", "(10/10)")

"""for file_path in Path("./input_levels").iterdir():
    print(file_path)
    level = GMD_Level(file_path)"""