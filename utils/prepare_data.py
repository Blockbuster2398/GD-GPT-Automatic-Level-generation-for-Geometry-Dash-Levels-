from classes.Level import GMD_Level
from pathlib import Path

all_tokens = []
# selected_levels = {"a_while.gmd", "nine_circles.gmd"}
total_datasets = 3

for i in range(total_datasets):
    for file_path in Path(f"../training_data_levels/dataset_{i+1}/levels").iterdir():
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

with open("../resources/data_tokenized.txt", "w") as f:
    f.write(token_string)
