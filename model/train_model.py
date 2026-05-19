import json
import time

from model import Transformer
import pickle
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

h_params = {
    "D_MODEL": 16,
    "NUM_HEADS": 8,
    "NUM_LAYERS": 4,
    "D_FF": 8,
    "MAX_SEQ_LENGTH": 500,
    "DROPOUT": .20,
    "BATCH_SIZE": 4,
    "EPOCHS": 10,
    "LR": 0.0001,
    "OBJECTS_OF_DATASET": 1000}

# Data Loading
with open("../training_data_levels/data_set_1/dataset_1.txt") as f:
    content = f.read()
print(f"Dataset original size: {len([obj for obj in content.split(";") if obj.strip()])}")
objects = [obj for obj in content.split(";") if obj.strip()][:h_params["OBJECTS_OF_DATASET"]]

vocab = {token: idx+1 for idx, token in enumerate(sorted(set(objects)))}  # 0 reserved for padding
vocab_size = len(vocab) + 1  # +1 for padding token
print(f"Dataset size: {len(objects)}, Vocab size: {vocab_size}")

# Tokenize
num_seq = torch.tensor([vocab[obj] for obj in objects])

# Build src/tgt pairs (sliding window)
sequences = num_seq.unfold(0, h_params["MAX_SEQ_LENGTH"], 1)  # (num_samples, MAX_SEQ_LENGTH)
src_data = sequences[:-1]   # input sequences
tgt_data = sequences[1:]    # target sequences shifted by 1

# DataLoader
dataset = TensorDataset(src_data, tgt_data)
print(f"Dataset: {dataset}")
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


# Training
transformer.train()
for epoch in range(h_params["EPOCHS"]):
    print(time.ctime())
    total_loss = 0
    for src_batch, tgt_batch in loader:
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

    print(f"Epoch {epoch + 1}/{h_params["EPOCHS"]} - Training Loss: {total_loss / len(loader):.4f}")

    # Save
    with (open("models/temp_model/transformer.pth", "wb")) as f:
        checkpoint = {"epoch" : epoch,
                      "model_state_dict" : transformer.state_dict(),
                      "optimizer_state_dict" : optimizer.state_dict()
                      }
        torch.save(checkpoint, "models/temp_model/transformer.pth")

    with (open("models/temp_model/vocab.pkl", "wb")) as f:
        pickle.dump(vocab, f)
    with (open("models/temp_model/h_params.pkl", "wb")) as g:
        pickle.dump(h_params, g)
    with (open("models/temp_model/details.txt", "w")) as h:
        json.dump(h_params, h)

# --- Validation ---
"""transformer.eval()
with torch.no_grad():
    val_output = transformer(src_data[:BATCH_SIZE], tgt_data[:BATCH_SIZE, :-1])
    val_loss = criterion(
        val_output.contiguous().view(-1, vocab_size),
        tgt_data[:BATCH_SIZE, 1:].contiguous().view(-1)
    )
    print(f"Validation Loss: {val_loss.item():.4f}")
"""

