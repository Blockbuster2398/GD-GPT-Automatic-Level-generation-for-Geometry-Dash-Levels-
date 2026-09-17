import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from classes.Level import GMD_Level

all_tokens = []
# selected_levels = {"a_while.gmd", "nine_circles.gmd"}
total_datasets = 9


levels_data = []
for i in range(total_datasets):
    dataset_dir = PROJECT_ROOT / "training_data_levels" / f"dataset_{i + 1}" / "levels"
    for file_path in dataset_dir.iterdir():
        
        #print(file_path)
        level = GMD_Level(file_path, keepDetail=False, keepDeco=False)
        all_tokens += level.tokens
        level_unique_tokens = len(set(level.tokens))
        # print(f"{file_path} level has {level_unique_tokens} individual tokens")
        level_tuple = (file_path, level.tokens, level_unique_tokens)
        levels_data.append(level_tuple)
        #print(f"Running object total = {len(all_tokens)}")

print([(level[2]) for level in levels_data])
sorted_levels = sorted(levels_data, key=lambda x: x[2])
#print([(str(level[0]).split("\\")[-1], level[2]) for level in sorted_levels])
print(f"There are a total of {len(sorted_levels)} levels with a total vocab size of {len(set(all_tokens))}")
for level in sorted_levels:
    all_tokens += level[1]
    print(f"Level {str(level[0]).split("\\")[-1]} has {level[2]} unique tokens")
# print(all_tokens)

token_frequency = dict()

for i in all_tokens:
    token_frequency[i] = token_frequency.get(i, 0) + 1
sorted_tokens = sorted(token_frequency.items(), key=lambda x: x[1], reverse=True)
for token, freq in sorted_tokens:
    print(token, freq)

token_string = ";".join(all_tokens)

with open(PROJECT_ROOT / "resources" / "data_tokenized_sorted.txt", "w") as f:
    f.write(token_string)
