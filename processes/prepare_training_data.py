import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from classes.Level import GMD_Level

all_tokens = []
# selected_levels = {"a_while.gmd", "nine_circles.gmd"}
total_datasets = 6

for i in range(total_datasets):
    dataset_dir = PROJECT_ROOT / "training_data_levels" / f"dataset_{i + 1}" / "levels"
    for file_path in dataset_dir.iterdir():
        print(file_path)
        level = GMD_Level(file_path, keepDetail=False, keepDeco=False)
        all_tokens += level.tokens
        print(f"Running object total = {len(all_tokens)}")

token_frequency = dict()

for i in all_tokens:
    token_frequency[i] = token_frequency.get(i, 0) + 1
sorted_tokens = sorted(token_frequency.items(), key=lambda x: x[1], reverse=True)
for token, freq in sorted_tokens:
    print(token, freq)

token_string = ";".join(all_tokens)

with open(PROJECT_ROOT / "resources" / "data_tokenized.txt", "w") as f:
    f.write(token_string)
