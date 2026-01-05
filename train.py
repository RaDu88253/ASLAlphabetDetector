import os
import torch
from fontTools.svgLib.path import PathBuilder
from torch import nn
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import datasets, transforms
import numpy as np
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
FILENAMES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k',
             'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
             'v', 'w', 'x', 'y']

NUM_CLASSES = len(FILENAMES)

# Dataset

class HandLandmarkDataset(Dataset):
    def __init__(self, landmarks, labels):
        self.landmarks = landmarks
        self.labels = labels

    def __len__(self):
        return len(self.landmarks)

    def __getitem__(self, idx):
        x = torch.tensor(self.landmarks[idx], dtype=torch.float32)
        y = torch.tensor(self.labels[idx], dtype=torch.long)
        return x, y


# Models

class HandMLP(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(63, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        x = x.view(x.size(  0), -1)
        return self.net(x)



def fetch_data():
    data = []
    labels = []
    for name in FILENAMES:
        read_file_path = Path(os.getenv('DATASET_FOLDER')) / f'{name}.txt'
        with open(read_file_path, "r") as f:
            lines = f.readlines()

        hands = [line.rstrip("\n").split(';') for line in lines]

        for hand in hands:
            landmarks = []
            for landmark in hand:
                x, y, z = landmark.split(',')
                landmarks.append([float(x), float(y), float(z)])
            assert len(landmarks) == 21
            data.append(landmarks)
            labels.append(name)
    data = np.array(data, dtype=np.float32)
    return data, labels

def encode_labels(string_labels):
    unique_labels = sorted(set(string_labels))

    label_to_idx = {label: i for i, label in enumerate(unique_labels)}
    idx_to_label = {i: label for label, i in label_to_idx.items()}

    encoded = [label_to_idx[l] for l in string_labels]
    return encoded, idx_to_label

# Training


def main():

    data, string_labels = fetch_data()
    encoded_labels, labels_dict = encode_labels(string_labels)


    dataset = HandLandmarkDataset(data, encoded_labels)

    n_total = len(dataset)
    n_train = int(0.8 * n_total)
    n_val = n_total - n_train

    train_ds, val_ds = random_split(dataset, [n_train, n_val])
    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=32)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = HandMLP(num_classes=NUM_CLASSES).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()

    for epoch in range(30):
        model.train()
        for xb, yb in train_loader:
            xb, yb = xb.to(device), yb.to(device)
            optimizer.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            optimizer.step()

        model.eval()
        correct = 0
        total = 0

        with torch.no_grad():
            for xb, yb in val_loader:
                xb, yb = xb.to(device), yb.to(device)

                logits = model(xb)
                preds = logits.argmax(dim=1)

                correct += (preds == yb).sum().item()
                total += yb.size(0)

        acc = correct / total
        print(f"Epoch {epoch + 1}: val accuracy = {acc:.3f}")

    torch.save(model.state_dict(), "models/hand_model_100_samples.pt")

    import json

    with open("label_map.json", "w") as f:
        json.dump(labels_dict, f)


if __name__ == "__main__":
    main()