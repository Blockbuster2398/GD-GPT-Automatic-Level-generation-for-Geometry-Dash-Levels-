import json

from model.run_model import generate_level


#from model.run_model import generate_level


def run_benchmark(model_name : str, prompt_cutoff = 500, temperature = 1.0, prompt_source="benchmark_levels.json"):

    with open(prompt_source, "r") as file:
        levels_dict = json.load(file)
    for key in levels_dict:
        print(f"Generating a level from: {key}")
        tokens = levels_dict[key].split(";")
        tokens = tokens[:500]
        token_string = ";".join(tokens)
        generate_level(model=model_name,
                       prompt = token_string,
                       level_length=1000,
                       seq_length=500,
                       temperature=1.5,
                       level_name=key)

if __name__ == "__main__":
    run_benchmark(model_name="video-3.0@epoch=1",
                  prompt_cutoff=500,
                  temperature=1.5)