import torch
from torch import tensor as tt

a = tt(list(range(9))).view(3,3)+1
# print(a)
# buffer = tt([1,2,3])
# print(buffer.shape)

# a[2,:] = buffer

# print(a)

b = a[2,:].view(1,-1)
print(b)
c = torch.rot90(b,1,[0,1])


a[:,[2]] = c#torch.rot90(c,1,[0,1])

print(a)