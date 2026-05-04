import sys
import os
import torch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.preprocess import build_graph


def preprocess_code(code):
    data = build_graph(code, 0)

    # shape fix
    if data.cls.dim() == 1:
        data.cls = data.cls.unsqueeze(0)

    data.num_graphs = 1

    return data