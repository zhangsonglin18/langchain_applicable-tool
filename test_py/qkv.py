import torch
import torch.nn as nn

class qkv():
    def __init__(self):
        self.q = nn.Linear(512, 512)
        self.k = nn.Linear(512, 512)
        self.v = nn.Linear(512, 512)

    def attentiton(self,x):
        q = self.q(x)
        k = self.k(x)
        v = self.v(x)
        scores = torch.matmul(q, k.transpose(-2, -1)) / torch.sqrt(torch.tensor(self.d_k, dtype=torch.float32))
        scores = torch.softmax(scores, dim=-1)
        output = torch.matmul(scores, v)
        return output



