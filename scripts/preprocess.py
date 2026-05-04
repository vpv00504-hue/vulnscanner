import os
import torch
from transformers import AutoTokenizer, AutoModel
from torch_geometric.data import Data

# =========================
# LOAD MODEL ONLY ONCE
# =========================
print("🚀 Loading CodeBERT (only once)...")

tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
bert_model = AutoModel.from_pretrained("microsoft/codebert-base")

bert_model.eval()

print("✅ CodeBERT Ready!")

# =========================
# BUILD GRAPH FUNCTION
# =========================
def build_graph(code, label):

    # 🔥 reduce tokens for speed
    inputs = tokenizer(
        code,
        return_tensors="pt",
        truncation=True,
        max_length=128   # ⚡ faster than 256
    )

    with torch.no_grad():
        outputs = bert_model(**inputs)

    emb = outputs.last_hidden_state.squeeze(0)  # (tokens, 768)
    cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze(0)

    num_nodes = emb.shape[0]

    # 🔥 simple sequential graph (fast)
    edge_index = []
    for i in range(num_nodes - 1):
        edge_index.append([i, i + 1])
        edge_index.append([i + 1, i])

    edge_index = torch.tensor(edge_index).t().contiguous()

    data = Data(
        x=emb,
        edge_index=edge_index,
        y=torch.tensor([label])
    )

    data.cls = cls_embedding

    return data