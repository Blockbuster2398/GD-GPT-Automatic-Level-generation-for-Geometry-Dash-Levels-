from classes.Level import GMD_Level
from pathlib import Path
from utils.ObjectDetailMapping import ObjectMapping
from utils.gmd_to_objects import gmd_to_objects

# level1 = GMD_Level("levels/Sonar 2.gmd")
level2 = GMD_Level("levels/the_nightmare.gmd")
# level3 = Level("levels/level_easy.gmd")
# level4 = GMD_Level("levels/level_easy.gmd")
# level1 = GMD_Level("levels/nine_circles.gmd")

level2.print_objects()

"""for file_path in Path("./levels").iterdir():
    print(file_path)
    level = GMD_Level(file_path)"""