import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from classes import Level
from model.run_model import generate_level


#from model.run_model import generate_level

def run_benchmark(model_name : str, prompt_cutoff = 500, temperature = 1.0, prompt_source="main_levels", boost_portals=True, dynamic_temperature=True, level_length=5000):
    total_objects = 0
    prompt_path = Path(prompt_source)
    if not prompt_path.is_absolute():
        prompt_path = PROJECT_ROOT / prompt_path
    for file in os.listdir(prompt_source):
        print(f"Generating a level from: {PROJECT_ROOT / prompt_path / file}")
        level_object = Level.GMD_Level(PROJECT_ROOT / prompt_path / file)
        tokens = level_object.tokens
        total_objects += len(tokens)
        tokens = tokens[:500]
        token_string = ";".join(tokens)
        #print(total_objects)
        generate_level(model=model_name,
                    prompt = token_string,
                    level_length=level_length,
                    seq_length=200,
                    temperature=temperature,
                    level_name=file,
                    boost_portals=boost_portals,
                    dynamic_temperature=dynamic_temperature)

if __name__ == "__main__":
    run_benchmark(model_name="gravity-test-ablated",
                  level_length=3000,
                  prompt_cutoff=500,
                  temperature=1,
                  boost_portals=False,
                  dynamic_temperature=True)
    """run_benchmark(model_name="setback@epoch=1",
                      prompt_cutoff=500,
                      temperature=2)"""