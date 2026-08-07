import importlib.util
import json
import pickle
import sys
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

MODEL_MODULE_PATH = PROJECT_ROOT / "model" / "model.py"
MODEL_SPEC = importlib.util.spec_from_file_location("gd_model_module", MODEL_MODULE_PATH)
if MODEL_SPEC is None or MODEL_SPEC.loader is None:
    raise ImportError(f"Could not load model module from {MODEL_MODULE_PATH}")

model_module = importlib.util.module_from_spec(MODEL_SPEC)
MODEL_SPEC.loader.exec_module(model_module)
Transformer = model_module.Transformer

checkpoint_name = None
do_load_checkpoint = input("Loading from a checkpoint?: ").upper()
if do_load_checkpoint in "YES":
    checkpoint_name = input("Checkpoint name?: ")
    # details = pickle.load()

new_model_name = input("New model name?: ")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

MODEL_ROOT = PROJECT_ROOT / "model" / "models"
DATASET_PATH = PROJECT_ROOT / "training_data_levels" / "full_dataset_retokenized" / "full_dataset_retokenized.txt"

save_all_epochs = True

if checkpoint_name:
    h_params = pickle.load(open(MODEL_ROOT / checkpoint_name / "h_params.pkl", "rb"))
    print(datetime.now())
    print(f"Loading model with...\n{h_params}")
else:
    """h_params = {
        "D_MODEL": 256,
        "NUM_HEADS": 16,
        "NUM_LAYERS": 16,
        "D_FF": 512,
        "MAX_SEQ_LENGTH": 500,
        "DROPOUT": .2,
        "BATCH_SIZE": 8,
        "EPOCHS": 500,
        "COMPLETED_EPOCHS": 0,
        "LR": 0.0001,
        "OBJECTS_OF_DATASET": 850000,
        "TRAINING_LOSS": None
    }"""
    h_params = {
            "D_MODEL": 384,
            "NUM_HEADS": 16,
            "NUM_LAYERS": 16,
            "D_FF": 1536,
            "MAX_SEQ_LENGTH": 400,
            "DROPOUT": .2,
            "BATCH_SIZE": 2,
            "ACCUMULATION_STEPS": 8,
            "EPOCHS": 500,
            "COMPLETED_EPOCHS": 0,
            "LR": 0.0001,
            "OBJECTS_OF_DATASET": 2000000,
            "TRAINING_LOSS": None
        }
    print(f"Training model with...\n{h_params}\n")

# Data Loading
with open(DATASET_PATH) as d:
    content = d.read()
    #content = f.read() + g.read() + h.read()

# print(f"Dataset original size: {len([obj for obj in content.split(";") if obj.strip()])}")
print(f"Objects available in dataset: {len([obj for obj in content.split(";") if obj.strip()])}")
objects = [obj for obj in content.split(";") if obj.strip()][:h_params["OBJECTS_OF_DATASET"]]
#print(len(objects))
#objects = objects[250000:]
#print(len(objects))

vocab = {token: idx+1 for idx, token in enumerate(sorted(set(objects)))}  # 0 reserved for padding
vocab_size = len(vocab) + 1  # +1 for padding token
# print(f"Dataset size: {len(objects)}, Vocab size: {vocab_size}")

# Tokenize
num_seq = torch.tensor([vocab[obj] for obj in objects])

# Build src/tgt pairs (sliding window)
sequences = num_seq.unfold(0, h_params["MAX_SEQ_LENGTH"], 1)  # (num_samples, MAX_SEQ_LENGTH)
src_data = sequences[:-1].to(device)  # input sequences
tgt_data = sequences[1:].to(device)    # target sequences shifted by 1

# DataLoader
dataset = TensorDataset(src_data, tgt_data)
loader = DataLoader(dataset, batch_size=h_params["BATCH_SIZE"], shuffle=True)

# Model
transformer = Transformer(
    vocab_size, vocab_size,
    h_params["D_MODEL"], h_params["NUM_HEADS"], h_params["NUM_LAYERS"],
    h_params["D_FF"], h_params["MAX_SEQ_LENGTH"], h_params["DROPOUT"]
)

criterion = nn.CrossEntropyLoss(ignore_index=0)
optimizer = optim.Adam(transformer.parameters(), lr=h_params["LR"], betas=(0.9, 0.98), eps=1e-9)
transformer = transformer.to(device)

if checkpoint_name:
    checkpoint = torch.load(MODEL_ROOT / checkpoint_name / "transformer_checkpoint.pth", map_location=device)
    transformer.load_state_dict(checkpoint["model_state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
    epoch = checkpoint['epoch']
    # loss = checkpoint['loss'] Not needed apparently

# Training
transformer.train()
batches_per_epoch = (h_params["OBJECTS_OF_DATASET"]-h_params["MAX_SEQ_LENGTH"])
time_per_batch = timedelta()

print(f"Epoch 0/{h_params["EPOCHS"]} - Training Loss: N/A")
for epoch in range(h_params["EPOCHS"]):
    total_loss = 0
    i = 0
    for src_batch, tgt_batch in loader:
        batch_start = datetime.now()
        i = i + 1
        src_batch = src_batch.to(device)  # move here
        tgt_batch = tgt_batch.to(device)  # move here

        optimizer.zero_grad()
        output = transformer(src_batch, tgt_batch[:, :-1])
        loss = criterion(
            output.contiguous().view(-1, vocab_size),
            tgt_batch[:, 1:].contiguous().view(-1)
        )
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        time_per_batch = (time_per_batch*i + datetime.now() - batch_start)/(i+1)
        time_per_epoch = time_per_batch * batches_per_epoch / h_params["BATCH_SIZE"]
        total_completion_time = datetime.now() + time_per_batch * (batches_per_epoch-i*4)
        print(f"\rEpoch: {(i * 100 * h_params["BATCH_SIZE"] / batches_per_epoch):.2f}%"
              f" -- Time per Epoch: {time_per_epoch}"
              f" -- Estimated Epoch Completion: {datetime.now() + time_per_batch * (batches_per_epoch-i*4)}"
              f" -- Estimated Total Completion: {datetime.now() + time_per_epoch * (h_params["EPOCHS"] - epoch-1)}"
              # f"- It is currently {datetime.now()}"
              f"", end='', flush=True)
    print(f"\n{datetime.now()}")
    h_params["TRAINING_LOSS"] = total_loss / len(loader)
    print(f"Epoch {epoch + 1}/{h_params["EPOCHS"]} - Training Loss: {h_params["TRAINING_LOSS"]:.4f}")

    # Validation
    """transformer.eval()
    with torch.no_grad():
        val_output = transformer(src_data[h_params["OBJECTS_OF_DATASET"]:-1],
                                 tgt_data[h_params["OBJECTS_OF_DATASET"]:-1])
        print(src_data.shape)
        print(tgt_data.shape)
        print(f"srclen{len(src_data[h_params["OBJECTS_OF_DATASET"]:-1])}")
        print(f"tgtlen{len(tgt_data[h_params["OBJECTS_OF_DATASET"]:-1])}")
        print(val_output)
        val_loss = criterion(
            val_output.contiguous().view(-1, vocab_size),
            tgt_data[:h_params["OBJECTS_OF_DATASET"], 1:].contiguous().view(-1)
        )
        print(f"Validation Loss: {val_loss.item():.4f}")

    print(f"Epoch {epoch + 1}/{h_params["EPOCHS"]} - Training Loss: {total_loss / len(loader):.4f} - Validation Loss: {val_loss:.4f}")
    """
    # Save checkpoint for further use
    model_save_name = new_model_name
    if "COMPLETED_EPOCHS" in h_params:
        h_params["COMPLETED_EPOCHS"] += 1
        # Custom naming for saving all epochs of a model
        if save_all_epochs:
            model_save_name = new_model_name
            if "@epoch" in model_save_name:
                model_save_name = model_save_name[:model_save_name.index("-epoch")+1]
            model_save_name += f"@epoch={h_params["COMPLETED_EPOCHS"]}"



    save_dir = MODEL_ROOT / model_save_name
    save_dir.mkdir(parents=False, exist_ok=True)
    with (
            open(save_dir / "transformer.pth", "wb") as model_file,
            open(save_dir / "transformer_checkpoint.pth", "wb") as checkpoint_file,
            open(save_dir / "vocab.pkl", "wb") as vocab_file,
            open(save_dir / "h_params.pkl", "wb") as params_file,
            open(save_dir / "details.txt", "w") as details_file):
        checkpoint = {"epoch" : epoch,
                      "model_state_dict" : transformer.state_dict(),
                      "optimizer_state_dict" : optimizer.state_dict()}
        torch.save(checkpoint, checkpoint_file)
        pickle.dump(vocab, vocab_file)
        pickle.dump(h_params, params_file)
        json.dump(h_params, details_file)

        # Save model itself
        torch.save(transformer.state_dict(), model_file)


        # expanse_series_1.4 loss: .026