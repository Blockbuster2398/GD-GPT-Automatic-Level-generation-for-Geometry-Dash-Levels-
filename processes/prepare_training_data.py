import sys
import datetime
import random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.Level import GMD_Level

all_tokens = []
training_tokens = []
validation_tokens = []
levels_data = []
token_frequencies = dict()
dataset_dir = PROJECT_ROOT / "training_data" / "GMD_levels"
for file_path in dataset_dir.iterdir():
    print(f"Processing {file_path.stem}")
    level = GMD_Level(file_path, keepDetail=False, keepDeco=False)
    all_tokens += level.tokens
    level_unique_tokens = len(set(level.tokens))
    level_total_tokens = len(level.tokens)
    print(f"{file_path.stem} level has {level_unique_tokens} individual tokens")
    level_tuple = (file_path.stem, level.tokens, level_unique_tokens, level_total_tokens)
    levels_data.append(level_tuple)
    # print(level_tuple)
    print(f"Running object total = {len(all_tokens)}")

# print([(level[2]) for level in levels_data])
# levels = sorted(levels_data, key=lambda x: x[2]) # Optional sorting
levels = [level_tuple[1] for level_tuple in levels_data]
random.shuffle(levels) # Shuffle level order to prevent similarly named levels from clumping together (ex. the various remakes of Blast Processing)

for level_tuple in levels_data: print(f"Level {level_tuple[0]} has {level_tuple[2]} unique tokens, {level_tuple[3]} total tokens")

hold_out_ratio = .10
for i in range(len(levels)): 
    all_tokens += levels[i]
    if i < (len(levels) * (1-hold_out_ratio)):
        training_tokens += levels[i]
    else: validation_tokens += levels[1]

current_day = datetime.date.today()
parent_dirs = Path(PROJECT_ROOT / "training_data" / f"compiled_dataset@{current_day}")
parent_dirs.mkdir(parents=True, exist_ok=True)
with (open(PROJECT_ROOT / "training_data" / f"compiled_dataset@{current_day}" / "train.txt", "w") as t, 
      open(PROJECT_ROOT / "training_data" / f"compiled_dataset@{current_day}" / "validation.txt", "w") as v):
    training_token_string = ";".join(training_tokens)
    validation_token_string = ";".join(validation_tokens)
    t.write(training_token_string)
    v.write(validation_token_string)

print(f"There are a total of {len(levels)} levels with a total vocab size of {len(set(all_tokens))}")
print([(level_tuple[0], level_tuple[2]) for level_tuple in levels_data])

for i in all_tokens:
    token_frequencies[i] = token_frequencies.get(i, 0) + 1
sorted_tokens = sorted(token_frequencies.items(), key=lambda x: x[1], reverse=True)
for token, freq in sorted_tokens:
    print(token, freq)




