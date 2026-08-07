import sys
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from classes.Level import GMD_Level
from utils.ObjectMapping import ObjectMap



level_path = PROJECT_ROOT / "GMD_conversion_test_levels" / "nine_circles.gmd"
level_path = PROJECT_ROOT / "main_levels" / "Theory Of Everything.gmd"
# level_path = PROJECT_ROOT / "main_levels" / "Electroman Adventure.gmd"
level = GMD_Level(level_path, keepDetail=False)
# level = GMD_Level(PROJECT_ROOT / "GMD_conversion_test_levels" / "iceland.gmd")
level.create_tokens()
token_string = ";".join(level.tokens)
data_tokenized_path = PROJECT_ROOT / "resources" / "data_tokenized.txt"
data_tokenized_path.parent.mkdir(parents=True, exist_ok=True)
with open(data_tokenized_path, "w") as f:
    f.write(token_string)


with open(data_tokenized_path, "r") as f:
    objects = GMD_Level.decode_tokens(f.read())
    # print(objects)

    level_reconstructed = GMD_Level(objects_list=objects)
    output_gmd_path = PROJECT_ROOT / "conversion_output" / "output.gmd"
    output_gmd_path.parent.mkdir(parents=True, exist_ok=True)
    level_reconstructed.create_gmd(output_gmd_path, "conversion_level", "???")
    print(f"Level reconstructed: {level_reconstructed}")


    # level = GMD_Level("GMD_conversion_test_levels/the Spanish flee.gmd")
    # print(f"Level: {level}")
