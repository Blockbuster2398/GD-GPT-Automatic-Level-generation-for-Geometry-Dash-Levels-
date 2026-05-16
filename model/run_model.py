import pickle

from classes import Level
from classes.Level import GMD_Level
from model import Transformer
import torch

with open("temp_model/vocab.pkl", "rb") as f:
    vocab = pickle.load(f);
    # print(vocab)
with open("temp_model/h_params.pkl", "rb") as g:
    h_params = pickle.load(g)


vocab_size = len(vocab) + 1

transformer = Transformer(
    vocab_size, vocab_size,
    h_params["D_MODEL"], h_params["NUM_HEADS"], h_params["NUM_LAYERS"],
    h_params["D_FF"], h_params["MAX_SEQ_LENGTH"], h_params["DROPOUT"]
)

transformer.load_state_dict(torch.load("temp_model/transformer.pth"))
transformer.eval()  # set to inference mode

def encode(text, vocab):
    tokens = [obj for obj in text.split(";") if obj.strip()]
    # print(tokens)
    return [vocab.get(token, 0) for token in tokens]  # 0 for unknown tokens


def generate(transformer, src_tokens, max_len=500):
    transformer.eval()
    with torch.no_grad():
        src = torch.tensor(src_tokens).unsqueeze(0)  # add batch dimension
        tgt = torch.tensor([1]).unsqueeze(0)  # start with token 1 as the first input

        for _ in range(max_len):
            output = transformer(src, tgt)
            next_token = output[0, -1, :].argmax(dim=-1).item()  # pick highest probability token

            if next_token == 0:  # stop if padding token predicted
                break

            tgt = torch.cat([tgt, torch.tensor([[next_token]])], dim=1)

    return tgt[0].tolist()  # remove batch dimension

def decode(tokens, vocab):
    reverse_vocab = {idx: token for token, idx in vocab.items()}
    return ";".join(reverse_vocab.get(t, "?") for t in tokens)

input_text = "start;_;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-2;yellow_pad-0;x_reset;x_increment-20;x_increment-10;y_increment-10;y_increment-2;y_increment-1;spike-0;x_reset;x_increment-20;x_increment-10;spike-0;x_reset;x_increment-20;x_increment-10;spike-0;x_reset;x_increment-20;x_increment-10;spike-0;x_reset;x_increment-40;x_increment-20;y_reset;y_increment-5;y_increment-2;_;x_reset;x_increment-20;x_increment-10;y_increment-5;y_increment-2;y_increment-1;spike-0;x_reset;x_increment-20;x_increment-10;spike-0;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-5;y_increment-2;_;x_reset;x_increment-40;x_increment-20;_;x_reset;x_increment-20;x_increment-10;y_increment-5;y_increment-2;y_increment-1;spike-0;y_increment-80;y_increment-10;spike-180;y_increment-20;y_increment-10;full_block;y_increment-40;y_increment-5;y_increment-2;y_increment-2;_;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-5;y_increment-2;_;x_reset;x_increment-160;x_increment-40;x_increment-10;y_increment-5;y_increment-2;y_increment-1;spike-0;x_reset;x_increment-20;x_increment-10;spike-0;x_reset;x_increment-20;x_increment-10;full_block;y_increment-20;y_increment-5;y_increment-2;y_increment-2;_;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-2;spike_short-0;x_reset;x_increment-20;x_increment-10;spike_short-0;y_increment-10;y_increment-1;_;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-2;spike_short-0;x_reset;x_increment-20;x_increment-10;y_increment-10;y_increment-2;y_increment-1;full_block;y_increment-20;y_increment-10;full_block;y_increment-20;y_increment-5;y_increment-2;y_increment-2;_;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-2;spike_short-0;x_reset;x_increment-20;x_increment-10;spike_short-0;x_reset;x_increment-10;x_increment-5;x_increment-1;y_increment-10;y_increment-5;y_increment-2;_;x_reset;x_increment-10;x_increment-2;x_increment-2;y_reset;y_increment-2;spike_short-0;x_reset;x_increment-20;x_increment-10;spike_short-0;x_reset;x_increment-20;x_increment-10;y_increment-10;y_increment-2;y_increment-1;full_block;y_increment-20;y_increment-10;full_block;y_increment-20;y_increment-5;y_increment-2;y_increment-2;_;x_reset;x_increment-80;x_increment-40;y_reset;y_increment-2;yellow_pad-0;x_reset;x_increment-40;x_increment-20;y_increment-10;y_increment-2;y_increment-1;full_block;y_increment-20;y_increment-10;y_increment-5;y_increment-2;y_increment-1;half_block-0;y_increment-20;y_increment-2;spike-0;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-2;spike_short-0;x_reset;x_increment-20;x_increment-10;spike_short-0;y_increment-10;y_increment-1;_;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-2;spike_short-0;y_increment-40;y_increment-10;y_increment-1;half_block-0;y_increment-10;y_increment-2;y_increment-2;_;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-2;spike_short-0;x_reset;x_increment-20;x_increment-10;spike_short-0;x_reset;x_increment-20;x_increment-10;spike_short-0;y_increment-10;y_increment-5;y_increment-2;_;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-2;spike_short-0;y_increment-80;y_increment-1;half_block-0;y_increment-10;y_increment-2;y_increment-2;_;x_reset;x_increment-20;x_increment-10;y_reset;y_increment-2;spike_short-0;x_reset;x_increment-20;x_increment-10;y_increment-10;y_increment-2;y_increment-1;full_block;y_increment-20;y_increment-10;y_increment-5;y_increment-2;y_increment-1;half_block-0;y_increment-10;y_increment-2;y_increment-2;_;x_reset;x_increment-80;x_increment-40;x_increment-20;x_increment-10;y_reset;y_increment-10;y_increment-5;spike-0;x_reset;x_increment-20;x_increment-10;spike-0;x_reset;x_increment-20;x_increment-10;full_block;y_increment-20;y_increment-5;y_increment-2;y_increment-2;_;x_reset;x_increment-20;x_increment-10;y_reset;"
src_tokens = encode(input_text, vocab)
print(src_tokens)
output_tokens = generate(transformer, src_tokens)
output_text = decode(output_tokens, vocab)

print(output_text)

objects = GMD_Level.decode_tokens(input_text + output_text)
level = GMD_Level("_", objects)
level.create_gmd("../generated_levels/gen1.gmd", "gen1", "???")