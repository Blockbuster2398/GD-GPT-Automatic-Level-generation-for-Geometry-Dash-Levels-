import sys
import datetime
import random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.Level import GMD_Level

level_name = "Bloodbath Auto"
encoded = GMD_Level("GMD_conversion_test_levels/" + level_name + ".gmd")
# encoded = GMD_Level("GMD_conversion_test_levels/OctagonForce.gdlvl")



print(encoded.tokens)
converted_level = GMD_Level("GMD_conversion_test_levels/" + level_name + ".gmd", GMD_Level.decode_tokens(";".join(encoded.tokens)))

encoded.create_gmd("generated_levels/conversion_output/out.gdlvl", "out", "conversion_test")
converted_level.create_gmd("generated_levels/conversion_output/converted_out.gdlvl", "converted_out", "conversion_test")