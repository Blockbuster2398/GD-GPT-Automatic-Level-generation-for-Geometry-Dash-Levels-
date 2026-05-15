from model import Transformer
import pickle
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# --- Config ---
D_MODEL = 512
NUM_HEADS = 8
NUM_LAYERS = 6
D_FF = 2048
MAX_SEQ_LENGTH = 50
DROPOUT = 0.1
BATCH_SIZE = 32
EPOCHS = 5
LR = 0.0001

# --- Data Loading ---
with open("../training_data_levels/data_set_1/dataset_1.txt") as f:
    content = f.read()

objects = [obj for obj in content.split(";") if obj.strip()][:200]
vocab = {token: idx+1 for idx, token in enumerate(sorted(set(objects)))}  # 0 reserved for padding
vocab_size = len(vocab) + 1  # +1 for padding token

print(f"Dataset size: {len(objects)}, Vocab size: {vocab_size}")

# --- Tokenize ---
num_seq = torch.tensor([vocab[obj] for obj in objects])

# --- Build src/tgt pairs (sliding window) ---
sequences = num_seq.unfold(0, MAX_SEQ_LENGTH, 1)  # (num_samples, MAX_SEQ_LENGTH)
src_data = sequences[:-1]   # input sequences
tgt_data = sequences[1:]    # target sequences shifted by 1

# --- DataLoader ---
dataset = TensorDataset(src_data, tgt_data)
print(f"Dataset: {dataset}")
loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# --- Model ---
transformer = Transformer(
    vocab_size, vocab_size,
    D_MODEL, NUM_HEADS, NUM_LAYERS,
    D_FF, MAX_SEQ_LENGTH, DROPOUT
)

criterion = nn.CrossEntropyLoss(ignore_index=0)
optimizer = optim.Adam(transformer.parameters(), lr=LR, betas=(0.9, 0.98), eps=1e-9)

# --- Training ---
transformer.train()
for epoch in range(EPOCHS): # Iterates over epochs (entire dataset)
    total_loss = 0
    for src_batch, tgt_batch in loader: # Iterates over batches (sets of examples)
        optimizer.zero_grad()
        output = transformer(src_batch, tgt_batch[:, :-1])
        loss = criterion(
            output.contiguous().view(-1, vocab_size),
            tgt_batch[:, 1:].contiguous().view(-1)
        )
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(f"Epoch {epoch+1}/{EPOCHS} — Loss: {total_loss / len(loader):.4f}")

# Save

torch.save(transformer.state_dict(), "transformer.pth")

# --- Validation ---
transformer.eval()
with torch.no_grad():
    val_output = transformer(src_data[:BATCH_SIZE], tgt_data[:BATCH_SIZE, :-1])
    val_loss = criterion(
        val_output.contiguous().view(-1, vocab_size),
        tgt_data[:BATCH_SIZE, 1:].contiguous().view(-1)
    )
    print(f"Validation Loss: {val_loss.item():.4f}")


