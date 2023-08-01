import torch
from torch import tensor as tt


decode = lambda b: {1:"blue",2:"red",3:"yellow",4:"white",5:"orange",6:"green"}[b]

class Face:

    def __init__(self,upF,initcolor):
        self.upF = upF
        self.colors = torch.randint(4,(3,3))
        

    def __call__(self,dir):
        dir *= -1
        self.colors = torch.rot90(self.colors,dir,[0,1])

class Cube:

    def __call__(self,alg):
        moves = []
        for move in alg:
            if move == "'":
                moves[-1] += "'"
            else:
                moves.append(move)
        # print(moves)


B = Cube()
B("ULDDD'ULDR'")
C = Face("blue","red")

print(decode(3))

print(C.colors)
C(1)
print(C.colors)