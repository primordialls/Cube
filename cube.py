import torch
from torch import tensor as tt

colorscheme = ["blue","white","red","green","yellow","orange"]
opposites = {colorscheme[i]:colorscheme[(i+3)%len(colorscheme)] for i in range(len(colorscheme))}
print(opposites)
colordict = {i+1:s for i,s in enumerate(colorscheme)}
decode = lambda b: colordict[b]
encode = lambda b: {s:i for i,s in colordict.items()}[b]

class Face:

    def __init__(self,initcolor):
        self.centercolor = encode(initcolor)
        self.colors = torch.ones(3,3)*encode(initcolor)
        self.upF = None
        self.leftF = None
        self.rightF = None
        self.downF = None
        self.parity = None

    def __call__(self,dir):
        self.faceOrder = [self.upF,self.rightF,self.downF,self.leftF]
        dir *= -1
        pardir = dir*self.parity
        if dir == -1:
            self.faceOrder = [self.faceOrder[0]] + [self.faceOrder[3-i] for i in range(len(self.faceOrder)-1)]
        self.colors = torch.rot90(self.colors,dir,[0,1])

        buffer = torch.clone(self.upF.colors[:,1-self.parity]).view(-1,1)

        self.upF.colors[:,[1-self.parity]] = torch.rot90(self.faceOrder[1].colors[1-pardir,:].view(1,-1),dir,[0,1])
        self.faceOrder[1].colors[[1-pardir],:] = torch.rot90(self.downF.colors[:,1-self.parity].view(-1,1),-dir,[0,1])
        self.downF.colors[:,[1-self.parity]] = torch.rot90(self.faceOrder[3].colors[1+pardir,:].view(1,-1),-dir,[0,1])
        self.faceOrder[-1].colors[[1+pardir],:] = torch.rot90(buffer,dir,[0,1])
class Cube:

    def __init__(self):
        self.faces = {"blue":Face("blue"),"white":Face("white"),"red":Face("red"),"green":Face("green"),"yellow":Face("yellow"),"orange":Face("orange")}
        faceList = [c for _,c in list(enumerate(self.faces.values()))]
        for i in range(len(faceList)):
            faceList[i].upF = faceList[(i+1)%len(faceList)]
            faceList[i].downF = faceList[(i-2)%len(faceList)]
            if i%2 == 0:
                faceList[i].parity = 1
                faceList[i].leftF = faceList[(i+2)%len(faceList)]
                faceList[i].rightF = faceList[(i-1)%len(faceList)]
            else:
                faceList[i].parity = -1
                faceList[i].leftF = faceList[(i-1)%len(faceList)]
                faceList[i].rightF = faceList[(i+2)%len(faceList)]
        self.orient("blue","white")

    def __call__(self,alg):
        moves = []
        alg = alg.replace(" ","")
        for move in alg:
            if move == "'" or move == "2":
                moves[-1] += move
            else:
                moves.append(move)
        for move in moves:
            reps = 1
            dir = 1
            if len(move) == 2:
                if move[1] == "2":
                    reps = 2
                else:
                    dir = -1
            if move[0] in ["U","D","L","R","F","B"]:
                for _ in range(reps):
                    self.faces[self.orientation[move[0]]](dir)
            elif move[0] in ["M","E","S"]:
                print("not yet")

            else:
                print("not yet")

    def orient(self,front,top):
        assert opposites[front] != top, "Impossible orientation"
        dummy = colorscheme
        dummy.remove(front)
        dummy.remove(opposites[front])
        self.orientation = {"U":top,"F":front,"R":dummy[dummy.index(top)-1],"D":opposites[top],"B":opposites[front]}
        self.orientation["L"] = opposites[self.orientation["R"]]

    def checksolved(self):
        for face in list(self.faces.values()):
            if face.colors.var() != 0:
                return False
        return True


B = Cube()
print(B.checksolved())
B("R' U' F' R U R' U' R' F R2 U' R' U' R U R' U R")
#B("RU")
for face in list(B.faces.values()):
    print(decode(face.centercolor))
    print(face.colors)