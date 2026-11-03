from pathlib import Path
import sys
import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.Level import GMD_Level



def visualize_level(level_path, resolution=1000, normalize_length=True):
    level = GMD_Level(level_path)
    tokens = level.tokens
    total_tokens = len(level.tokens)
    if normalize_length: x_values = [i / total_tokens for i in range(total_tokens-resolution)]
    else: x_values = [i for i in range(total_tokens-resolution)]
    variety = []
    for i in range(0, total_tokens-resolution):
        variety.append(len(set(tokens[i:i+resolution+1])))
    # print(len(variety))
    # print(len(x_values))

    fig, ax = plt.subplots()
    ax.plot(x_values, variety, label="Object variety")
    plt.show()

def visualize_levels(level_folder_path, resolution = 500, normalize_length=True):
    level_to_attributes = []
    fig, ax = plt.subplots()
    for level_path in Path(level_folder_path).iterdir():
        print(level_path)
        level = GMD_Level(level_path)
        tokens = level.tokens
        total_tokens = len(level.tokens)
        if normalize_length: x_values = [i / total_tokens for i in range(total_tokens-resolution)]
        else: x_values = [i for i in range(total_tokens-resolution)]
        variety = []
        for i in range(0, total_tokens-resolution):
            variety.append(len(set(tokens[i:i+resolution+1])))

        mean_variety = np.average(variety).item()
        disturbance_min = (np.average(variety) - min(variety)).item()
        disturbance_max = (max(variety)) - np.average(variety).item()
        level_to_attributes.append((level_path.name, mean_variety, disturbance_min, disturbance_max))
        ax.plot(x_values, variety, label=str(level_path))

    print(f"Means too low?") # Cut custom levels?
    print(sorted(level_to_attributes, key=lambda a: a[1])[:30])
    print(f"Means too high?") # Cut 5-10%?
    print(sorted(level_to_attributes, key=lambda a: a[1], reverse=True)[:30])
    
    print(f"disturbance Min too Low? (Is this Good?)") # This seems to somewhat correlate with good (training) levels
    print(sorted(level_to_attributes, key=lambda a: a[2])[:30])
    print(f"Disturbance Max too Low? (Is this Good?)") # This seems to mostly correlate with good (training) levels
    print(sorted(level_to_attributes, key=lambda a: a[3])[:30])
    
    print(f"disturbance Min too High?") # Get rid of values above 30?
    print(sorted(level_to_attributes, key=lambda a: a[2], reverse=True)[:30])
    print(f"Disturbance Max too High?") # Not that bad, get rid of values above 30?
    print(sorted(level_to_attributes, key=lambda a: a[3], reverse=True)[:30])
    
    plt.show()

# visualize_level(Path("training_data/main_levels/Back on Track.gmd"))
# visualize_level(Path("training_data/main_levels/Dry Out.gmd"))
# visualize_level(Path("training_data/GMD_levels/Heptagon Force.gmd"))

visualize_levels(Path("training_data/GMD_levels"), normalize_length=False)
# visualize_levels(Path("training_data/main_levels"), normalize_length=False)