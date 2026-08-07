import json
import sys
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from classes.Level import GMD_Level

levels = defaultdict()
main_levels_dir = PROJECT_ROOT / "main_levels"

for file_path in main_levels_dir.iterdir():
    print(f"Processing: {file_path}")
    level = GMD_Level(file_path, keepDetail=False, keepDeco=False)
    level_name = str(file_path).split(f'\\')[-1][:-4]
    print(level_name)

    levels[level_name] = ";".join(level.tokens)

with open(PROJECT_ROOT / "benchmark_levels.json", "w") as f:
    json.dump(levels, f)


