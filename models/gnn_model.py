import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv, global_mean_pool


class VulnGNN(nn.Module):
    def __init__(self):
        super().__init__()

        hidden = 256

        self.gat1 = GATConv(768, hidden, heads=4, dropout=0.3)
        self.gat2 = GATConv(hidden * 4, hidden, heads=4, dropout=0.3)
        self.gat3 = GATConv(hidden * 4, hidden, heads=2, dropout=0.3)

        self.norm1 = nn.LayerNorm(hidden * 4)
        self.norm2 = nn.LayerNorm(hidden * 4)
        self.norm3 = nn.LayerNorm(hidden * 2)

        self.dropout = nn.Dropout(0.3)

        # 🔥 Learnable balance
        self.alpha = nn.Parameter(torch.tensor(0.5))

        self.fc1 = nn.Linear(1280, 256)
        self.fc2 = nn.Linear(256, 64)
        self.fc3 = nn.Linear(64, 2)

    def forward(self, data, cls_embedding):
        x, edge_index, batch = data.x, data.edge_index, data.batch

        x1 = F.elu(self.norm1(self.gat1(x, edge_index)))
        x2 = F.elu(self.norm2(self.gat2(x1, edge_index)))
        x2 = x2 + x1[:, :x2.shape[1]]

        x3 = F.elu(self.norm3(self.gat3(x2, edge_index)))
        x = self.dropout(x3)

        x = global_mean_pool(x, batch)

        # 🔥 Learnable fusion
        w = torch.sigmoid(self.alpha)

        x = torch.cat([
            x * (1 - w),
            cls_embedding * w
        ], dim=1)

        x = self.dropout(x)

        x = F.relu(self.fc1(x))
        x = self.dropout(x)

        x = F.relu(self.fc2(x))
        x = self.dropout(x)

        return self.fc3(x)