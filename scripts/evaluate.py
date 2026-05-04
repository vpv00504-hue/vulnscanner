import torch
from torch_geometric.loader import DataLoader
from models.gnn_model import VulnGNN
from utils.dataset import DevignDataset
from utils.metrics import compute_metrics

dataset = DevignDataset("data/raw/devign.json")
loader = DataLoader(dataset, batch_size=32)

model = VulnGNN()
model.load_state_dict(torch.load("model.pth"))
model.eval()

all_preds, all_labels = [], []

with torch.no_grad():
    for data in loader:
        out = model(data)
        preds = out.argmax(dim=1).numpy()
        labels = data.y.numpy()

        all_preds.extend(preds)
        all_labels.extend(labels)

print(compute_metrics(all_labels, all_preds))