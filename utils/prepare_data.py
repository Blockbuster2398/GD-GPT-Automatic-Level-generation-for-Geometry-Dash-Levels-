from classes.Level import GMD_Level
from pathlib import Path

all_tokens = []
# selected_levels = {"a_while.gmd", "nine_circles.gmd"}
selected_levels = {"the spanish flee.gmd"}
for file_path in Path("../training_data_levels/data_set_1/levels").iterdir():
    if str(file_path).split("\\")[-1] in selected_levels or True:
        print(file_path)
        level = GMD_Level(file_path)
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
