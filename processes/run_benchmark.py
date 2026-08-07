import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from model.run_model import generate_level


#from model.run_model import generate_level

def run_benchmark(model_name : str, prompt_cutoff = 500, temperature = 1.0, prompt_source="benchmark_levels.json"):
    total_objects = 0
    prompt_path = Path(prompt_source)
    if not prompt_path.is_absolute():
        prompt_path = PROJECT_ROOT / prompt_path

    with open(prompt_path, "r") as file:
        levels_dict = json.load(file)
    for key in levels_dict:
        print(f"Generating a level from: {key}")
        tokens = levels_dict[key].split(";")
        total_objects += len(tokens)
        tokens = tokens[:500]
        token_string = ";".join(tokens)
        #print(total_objects)
        generate_level(model=model_name,
                       prompt = token_string,
                       level_length=5000,
                       seq_length=200,
                       temperature=temperature,
                       level_name=key)

if __name__ == "__main__":
    run_benchmark(model_name="video-6.0@epoch=1",
                  prompt_cutoff=500,
                  temperature=1)
    run_benchmark(model_name="video-6.0@epoch=1",
                      prompt_cutoff=500,
                      temperature=2)