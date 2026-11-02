from pathlib import Path
import sys
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.Level import GMD_Level



def visualize_level(level_path, resolution=1000):
    level = GMD_Level(level_path)
    tokens = level.tokens
    total_tokens = len(level.tokens)
    x_values = [i / total_tokens for i in range(total_tokens-resolution)]
    variety = []
    for i in range(0, total_tokens-resolution):
        variety.append(len(set(tokens[i:i+resolution+1])))
    # print(len(variety))
    # print(len(x_values))

    fig, ax = plt.subplots()
    ax.plot(x_values, variety, label="Object variety")
    plt.show()

visualize_level(Path("training_data/main_levels/Back on Track.gmd"))
visualize_level(Path("training_data/main_levels/Dry Out.gmd"))
visualize_level(Path("training_data/GMD_levels/Heptagon Force.gmd"))
