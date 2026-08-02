import json
from datetime import datetime, timedelta

from model import Transformer
import pickle
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from pathlib import Path

checkpoint_name = None
do_load_checkpoint = input("Loading from a checkpoint?: ").upper()
if do_load_checkpoint in "YES":
    checkpoint_name = input("Checkpoint name?: ")
    # details = pickle.load()

new_model_name = input("New model name?: ")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

if checkpoint_name:
    h_params = pickle.load(open(f"models/{checkpoint_name}/h_params.pkl", "rb"))
    print(datetime.now())
    print(f"Loading model with...\n{h_params}")
else:
    h_params = {
        "D_MODEL": 512,
        "NUM_HEADS": 8,
        "NUM_LAYERS": 12,
        "D_FF": 2048,
        "MAX_SEQ_LENGTH": 600,
        "DROPOUT": .20,
        "BATCH_SIZE": 50,
        "EPOCHS": 2,
        "LR": 0.0002,
        "OBJECTS_OF_DATASET": 601}
    print(f"Training model with...\n{h_params}\n")

# Data Loading
with (
    open("../training_data_levels/dataset_1/dataset_1.txt") as f,
    open("../training_data_levels/dataset_2/dataset_2.txt") as g,
    open("../training_data_levels/dataset_3/dataset_3.txt") as h):
    content = f.read() + g.read() + h.read()

# print(f"Dataset original size: {len([obj for obj in content.split(";") if obj.strip()])}")
print(f"Objects available in dataset: {len([obj for obj in content.split(";") if obj.strip()])}")
objects = [obj for obj in content.split(";") if obj.strip()][:h_params["OBJECTS_OF_DATASET"]]

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
    checkpoint = torch.load(f"./models/{checkpoint_name}/transformer_checkpoint.pth")
    transformer.load_state_dict(checkpoint["model_state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
    epoch = checkpoint['epoch']
    # loss = checkpoint['loss'] Not needed apparently

# Training
transformer.train()
batches_per_epoch = (h_params["OBJECTS_OF_DATASET"]-h_params["MAX_SEQ_LENGTH"])
time_per_batch = timedelta()

print("Epoch 0/10 - Training Loss: N/A")
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
    print(f"Epoch {epoch + 1}/{h_params["EPOCHS"]} - Training Loss: {total_loss / len(loader):.4f}")

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
    Path(f"models/{new_model_name}").mkdir(parents=False, exist_ok=True)
    with (
            open(f"models/{new_model_name}/transformer.pth", "wb") as model_file,
            open(f"models/{new_model_name}/transformer_checkpoint.pth", "wb") as checkpoint_file,
            open(f"models/{new_model_name}/vocab.pkl", "wb") as vocab_file,
            open(f"models/{new_model_name}/h_params.pkl", "wb") as params_file,
            open(f"models/{new_model_name}/details.txt", "w") as details_file):
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