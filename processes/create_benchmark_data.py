import json
from pathlib import Path
from collections import defaultdict

from classes.Level import GMD_Level

levels = defaultdict()

for file_path in Path(f"../main_levels/").iterdir():
    print(f"Processing: {file_path}")
    level = GMD_Level(file_path, keepDetail=False, keepDeco=False)
    level_name = str(file_path).split(f'\\')[-1][:-4]
    print(level_name)

    levels[level_name] = ";".join(level.tokens)

with open("benchmark_levels.json", "w") as f:
    json.dump(levels, f)


