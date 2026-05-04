import os
import sys
import torch
import torch.nn.functional as F
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from torch_geometric.loader import DataLoader
from torch.utils.data import random_split, WeightedRandomSampler

from models.gnn_model import VulnGNN
from utils.dataset import DevignDataset
from utils.metrics import compute_metrics
from config import Config


# =========================
# 🔥 STABLE FOCAL LOSS
# =========================
class FocalLoss(torch.nn.Module):
    def __init__(self, gamma=1.2, alpha=0.6):
        super().__init__()
        self.gamma = gamma
        self.alpha = alpha

    def forward(self, inputs, targets):
        ce_loss = F.cross_entropy(inputs, targets, reduction='none')
        pt = torch.exp(-ce_loss)
        loss = self.alpha * (1 - pt) ** self.gamma * ce_loss
        return loss.mean()


# =========================
# PATHS
# =========================
DATA_PATH = "data/processed/"
MODEL_PATH = "models/saved/best_model.pth"
os.makedirs("models/saved", exist_ok=True)


# =========================
# LOAD DATASET
# =========================
dataset = DevignDataset(DATA_PATH)

train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = random_split(dataset, [train_size, test_size])


# =========================
# BALANCED SAMPLING
# =========================
train_labels = [train_dataset[i].y.item() for i in range(len(train_dataset))]
class_count = [train_labels.count(0), train_labels.count(1)]

print("Train class count:", class_count)

weights = [1.0 / class_count[label] for label in train_labels]
sampler = WeightedRandomSampler(weights, len(weights))


# =========================
# DATALOADER
# =========================
train_loader = DataLoader(train_dataset, batch_size=Config.BATCH_SIZE, sampler=sampler)
test_loader = DataLoader(test_dataset, batch_size=Config.BATCH_SIZE)


# =========================
# MODEL
# =========================
model = VulnGNN().to(Config.DEVICE)

optimizer = torch.optim.Adam(model.parameters(), lr=Config.LR)

criterion = FocalLoss()  # 🔥 stable version

scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=50)


# =========================
# TRAIN SETTINGS
# =========================
best_f1 = 0
patience = 15
no_improve = 0

print("\n🚀 Training Started...\n")


# =========================
# TRAIN LOOP
# =========================
for epoch in range(Config.EPOCHS):

    model.train()
    total_loss = 0

    for data in tqdm(train_loader):
        data = data.to(Config.DEVICE)

        # 🔥 FIXED CLS SHAPE
        cls_embedding = data.cls.view(data.num_graphs, -1).to(Config.DEVICE)

        # 🔥 Balanced CLS contribution
        cls_embedding = cls_embedding * 0.65

        optimizer.zero_grad()

        out = model(data, cls_embedding)

        loss = criterion(out, data.y)
        loss.backward()

        # 🔥 GRADIENT CLIPPING (IMPORTANT)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

        optimizer.step()

        total_loss += loss.item()

    scheduler.step()

    # =========================
    # VALIDATION
    # =========================
    model.eval()
    all_preds, all_labels = [], []

    with torch.no_grad():
        for data in test_loader:
            data = data.to(Config.DEVICE)

            cls_embedding = data.cls.view(data.num_graphs, -1).to(Config.DEVICE)
            cls_embedding = cls_embedding * 0.65

            out = model(data, cls_embedding)

            preds = out.argmax(dim=1).cpu().numpy()
            labels = data.y.cpu().numpy()

            all_preds.extend(preds)
            all_labels.extend(labels)

    metrics = compute_metrics(all_labels, all_preds)

    print(f"\nEpoch {epoch+1}/{Config.EPOCHS}")
    print(f"Loss: {total_loss:.2f}")
    print(metrics)
    print("-" * 40)

    # =========================
    # SAVE BEST MODEL
    # =========================
    if metrics["f1"] > best_f1:
        best_f1 = metrics["f1"]
        torch.save(model.state_dict(), MODEL_PATH)
        print("✅ Best model saved!\n")
        no_improve = 0
    else:
        no_improve += 1

    # =========================
    # EARLY STOPPING
    # =========================
    if no_improve >= patience:
        print("⏹ Early stopping triggered")
        break


print(f"\n🔥 FINAL BEST F1: {best_f1:.4f}")