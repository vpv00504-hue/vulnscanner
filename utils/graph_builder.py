import torch
from torch_geometric.data import Data

def build_graph(code, tokenizer, model):
    inputs = tokenizer(code, return_tensors="pt", truncation=True, max_length=256)

    with torch.no_grad():
        outputs = model(**inputs)

    embeddings = outputs.last_hidden_state.squeeze(0)

    num_nodes = embeddings.shape[0]

    edge_index = []
    for i in range(num_nodes - 1):
        edge_index.append([i, i+1])
        edge_index.append([i+1, i])

    edge_index = torch.tensor(edge_index).t().contiguous()

    return Data(x=embeddings, edge_index=edge_index)