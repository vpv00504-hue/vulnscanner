import os
import json
import torch
from transformers import AutoTokenizer, AutoModel
from torch_geometric.data import Data

DATA_PATH = "data/raw/devign.json"
SAVE_PATH = "data/processed/"
os.makedirs(SAVE_PATH, exist_ok=True)

tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
bert_model = AutoModel.from_pretrained("microsoft/codebert-base")
bert_model.eval()


def build_graph(code, label):
    inputs = tokenizer(code, return_tensors="pt", truncation=True, max_length=256)

    with torch.no_grad():
        outputs = bert_model(**inputs)

    emb = outputs.last_hidden_state.squeeze(0)
    cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze(0)

    num_nodes = emb.size(0)
    edge_index = []

    # window
    for i in range(num_nodes):
        for j in range(i+1, min(i+9, num_nodes)):
            edge_index.append([i, j])
            edge_index.append([j, i])

    # skip
    for i in range(0, num_nodes, 5):
        for j in range(i+5, min(i+15, num_nodes)):
            edge_index.append([i, j])
            edge_index.append([j, i])

    # cfg
    for i in range(num_nodes - 1):
        edge_index.append([i, i+1])
        edge_index.append([i+1, i])

    # extra edges
    for i in range(0, num_nodes - 10, 10):
        edge_index.append([i, i+10])
        edge_index.append([i+10, i])

    edge_index = torch.tensor(edge_index).t().contiguous()

    return Data(
        x=emb,
        edge_index=edge_index,
        y=torch.tensor([label]),
        code=code,
        cls=cls_embedding   # 🔥 saved
    )


with open(DATA_PATH) as f:
    data = json.load(f)

for i, item in enumerate(data):
    g = build_graph(item["func"], item["target"])
    torch.save(g, f"{SAVE_PATH}/{i}.pt")

print("✅ Preprocessing DONE (FAST MODE)")