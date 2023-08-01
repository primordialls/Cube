import torch
from torch import tensor as tt

a = torch.randint(10,(3,3))
print(a)
a = torch.rot90(a, 2, [0, 1])
print(a)