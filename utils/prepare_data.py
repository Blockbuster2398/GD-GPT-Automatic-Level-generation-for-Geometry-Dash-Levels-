from classes.Level import GMD_Level
from pathlib import Path

all_tokens = []
# selected_levels = {"a_while.gmd", "nine_circles.gmd"}
selected_levels = {"the spanish flee.gmd"}
for file_path in Path("../input_levels").iterdir():
    if str(file_path).split("\\")[-1] in selected_levels or True:
        print(file_path)
        level = GMD_Level(file_path)
        all_tokens += level.tokens
        print(f"Running object total = {len(all_tokens)}")

"""token_frequency = defaultdict(int)
for i in all_tokens:
    token_frequency[i] += 1
print(token_frequency)
print(len(token_frequency))"""

token_string = ";".join(all_tokens)

with open("../resources/data_tokenized.txt", "w") as f:
    f.write(token_string)
