import os
import torch
from torch.utils.data import Dataset


class DevignDataset(Dataset):
    def __init__(self, path):
        self.files = [os.path.join(path, f) for f in os.listdir(path)]

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        data = torch.load(self.files[idx])

        if not hasattr(data, "code"):
            data.code = ""

        if not hasattr(data, "cls"):
            data.cls = torch.zeros(768)

        return data