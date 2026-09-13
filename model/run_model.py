import os
import pickle
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from classes.Level import GMD_Level
import importlib.util
import torch

MODEL_MODULE_PATH = PROJECT_ROOT / "model" / "model.py"
MODEL_SPEC = importlib.util.spec_from_file_location("gd_model_module", MODEL_MODULE_PATH)
if MODEL_SPEC is None or MODEL_SPEC.loader is None:
    raise ImportError(f"Could not load model module from {MODEL_MODULE_PATH}")

model_module = importlib.util.module_from_spec(MODEL_SPEC)
MODEL_SPEC.loader.exec_module(model_module)
Transformer = model_module.Transformer


def generate_level(model : str, prompt : str, level_length : int, seq_length, temperature : float, level_name=None, boost_portals=True, dynamic_temperature=True):

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    model_name = model
    model_dir = PROJECT_ROOT / "model" / "models" / model_name
    with (open(model_dir / "vocab.pkl", "rb") as vocab_file,
          open(model_dir / "h_params.pkl", "rb") as params_file):
        vocab = pickle.load(vocab_file)
        h_params = pickle.load(params_file)

    if __name__ == "__main__":
        print(f"Vocab is the following: {vocab}")

    vocab_size = len(vocab) + 1
    transformer = Transformer(
        vocab_size, vocab_size,
        h_params["D_MODEL"], h_params["NUM_HEADS"], h_params["NUM_LAYERS"],
        h_params["D_FF"], h_params["MAX_SEQ_LENGTH"], h_params["DROPOUT"]
    )

    transformer.load_state_dict(torch.load(model_dir / "transformer.pth", map_location=device))
    transformer.to(device)


    print(f"Running {model_name} with parameters: {h_params}")
    transformer.eval()

    # use actual start token index from the vocab if present (fallback to 1)
    start_idx = vocab.get("start", vocab.get("<START>", 1))

    def encode(text, vocab):
        tokens = [obj for obj in text.split(";") if obj.strip()]
        # print(tokens)
        return [vocab.get(token, 0) for token in tokens]  # 0 for unknown tokens


    def generate(transformer, src_tokens, max_len=level_length, max_seq_length=seq_length, temp=temperature, boost_portals=True, dynamic_temperature=True):
        transformer.eval()
        with torch.no_grad():
            # initialize tgt with the proper start token index
            tgt = torch.tensor([start_idx]).unsqueeze(0).to(device)
            original_temp = temp
            portal_logger = ["cube_mode"]
            gravity_logger = ["normal_gravity"]
            for i in range(max_len):
                # Slide both windows to stay within max_seq_length
                src = torch.tensor(src_tokens[-max_seq_length:]).unsqueeze(0).to(device)
                tgt_window = tgt[:, -max_seq_length:]

                output = transformer(src, tgt_window)

                logits = output[0, -1, :]
                #print(f"\rLogits for token {i}: {logits}", end='', flush=True)
                # Implement portal token bias
                if boost_portals:
                    logits[vocab.get("ship_portal", 0)] *= 1.25
                    #logits[vocab.get("cube_portal", 0)] *= 1.5
                    logits[vocab.get("ball_portal", 0)] *= 1.25
                    logits[vocab.get("wave_portal", 0)] *= 1.25
                    logits[vocab.get("ufo_portal", 0)] *= 1.25
                    logits[vocab.get("robot_portal", 0)] *= 1.25
                    logits[vocab.get("spider_portal", 0)] *= 1.25
                logits[vocab.get("end", 0)] *= 0.1  # Decrease probability of end token
                probs = torch.softmax(logits / temp, dim=-1)
                next_token = torch.multinomial(probs, 1).item()
                next_token_readable = decode([next_token], vocab)
                #print(f"Next obj type:{next_token_readable}", flush=True)
                if "portal" in next_token_readable or "mode" in next_token_readable:
                    #print(f"Next portal type:{next_token_readable}", flush=True)
                    if next_token_readable != portal_logger[-1]:
                        portal_logger.append(next_token_readable)
                if "gravity" in next_token_readable:
                    if next_token_readable != gravity_logger[-1]:
                        gravity_logger.append(next_token_readable)

                # Append to the full tgt sequence (not just the window)
                tgt = torch.cat([tgt, torch.tensor([[next_token]], device=device)], dim=1)
                # Also grow src_tokens so the src window slides forward too
                src_tokens = src_tokens + [next_token]
                # Audit token diversity
                last_n_tokens = set(src_tokens[-100:])
                if dynamic_temperature:
                    if len(last_n_tokens) <= 10:
                        temp *= 1.001  # Increase temperature to encourage diversity
                    elif len(last_n_tokens) > 15:
                        temp = (temp + original_temp)/2  # Decrease temperature to encourage convergence
                print(f"\r{i}/{max_len} tokens generated: {i / max_len * 100:.2f}% Complete! 100 token diversity: {len(last_n_tokens)} unique tokens with temperature: {temp:.4f}", end='', flush=True)

        result = tgt[0].tolist()

        print("\n")
        print(f"Portal Logger is {portal_logger}")
        print(f"Gravity Logger is {gravity_logger}")
        
        # strip the leading start token so it doesn't become a real object in output
        if len(result) > 0 and result[0] == start_idx:
            result = result[1:]
        return result

    def decode(tokens, vocab):
        reverse_vocab = {idx: token for token, idx in vocab.items()}
        return ";".join(reverse_vocab.get(t, "?") for t in tokens)

    input_text = prompt

    src_tokens = encode(input_text, vocab)
    #print(src_tokens)
    output_tokens = generate(transformer, src_tokens, boost_portals=boost_portals, dynamic_temperature=dynamic_temperature)
    output_text = decode(output_tokens, vocab)




    objects = GMD_Level.decode_tokens("x_increment-50;" + input_text + ";" + output_text)
    output_folder = PROJECT_ROOT / "generated_levels" / model_name
    if not output_folder.exists(): output_folder.mkdir(parents=True, exist_ok=True)
    file_count = sum(1 for item in output_folder.iterdir() if item.is_file())
    level = GMD_Level("_", objects)

    #print(output_text)

    if level_name:
        level.create_gmd(output_folder / f"{level_name}@temperature={temperature}_{file_count}.gmd", f"{model_name}/{level_name}_{file_count}", "AI Generated")
    else:
        level.create_gmd(output_folder / f"{model_name}@temperature={temperature}_{file_count}.gmd", f"{model_name}/{model_name}_{file_count}", "AI Generated")


spike_cap = "spike-0;x_reset;x_increment-80;x_increment-40;x_increment-20;x_increment-10;spike-0;x_reset;x_increment-80;x_increment-40;x_increment-20;x_increment-10;spike-0;x_reset;x_increment-160;x_increment-80;spike-0;x_reset;x_increment-20;x_increment-10;spike-0;x_reset;x_increment-20;x_increment-10;full_block;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-2;spike_short-0;x_reset;x_increment-20;x_increment-10;spike_short-0;x_reset;x_increment-5;x_increment-2;x_increment-1;y_increment-10;y_increment-5;y_increment-2;_;x_reset;x_increment-20;x_increment-2;y_reset;y_increment-2;spike_short-0;x_reset;x_increment-20;x_increment-10;spike_short-0;y_increment-10;y_increment-2;y_increment-1;full_block;y_increment-20;y_increment-10;full_block;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-2;spike_short-0;x_reset;x_increment-20;x_increment-10;spike_short-0;y_increment-10;y_increment-1;_;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-2;spike_short-0;x_reset;x_increment-20;x_increment-10;spike_short-0;y_increment-10;y_increment-2;y_increment-1;full_block;y_increment-20;y_increment-10;full_block;y_increment-20;y_increment-10;full_block;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-2;spike_short-0;y_increment-40;y_increment-20;y_increment-10;y_increment-2;y_increment-1;full_block;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-2;spike_short-0;y_increment-40;y_increment-20;y_increment-10;y_increment-2;y_increment-1;full_block;y_increment-20;y_increment-10;spike-0;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-2;spike_short-0;y_increment-10;y_increment-5;y_increment-2;_;y_increment-40;y_increment-10;y_increment-5;y_increment-1;full_block;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-2;spike_short-0;y_increment-40;y_increment-20;y_increment-10;y_increment-2;y_increment-1;full_block;y_increment-20;y_increment-10;spike-0;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-2;spike_short-0;y_increment-10;y_increment-2;y_increment-1;full_block;y_increment-20;y_increment-10;full_block;y_increment-20;y_increment-10;full_block;y_increment-20;y_increment-10;full_block;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-2;spike_short-0;x_reset;x_increment-10;x_increment-2;x_increment-2;y_increment-5;y_increment-2;y_increment-2;_;x_reset;x_increment-10;x_increment-5;x_increment-1;y_reset;y_increment-2;spike_short-0;y_increment-160;y_increment-20;"

if __name__ == "__main__":
    generate_level(model = "video-3.0@epoch=1",
                   prompt = spike_cap,
                   level_length=1000,
                   seq_length=500,
                   temperature=1,
                   level_name=None)