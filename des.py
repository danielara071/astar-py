import json

dataSize = "save path de n x m aqui"
dataObstacles = "save path de obstacles aqui"
dataStartGoal = "save path de start y goal aqui"
class GridSize:
    def __init__(self, n, m):
        self.n = n 
        self.m = m
    
dataSize = json.load(dataSize)
dataObstacles = json.load(dataObstacles)
dataStartGoal = json.load(dataStartGoal)
n = dataSize["n"]
m = dataSize["m"]
size = GridSize(n, m)
obstacles = []
start = (dataStartGoal["start"]["x"],dataStartGoal["start"]["y"])
goal = (dataStartGoal["goal"]["x"], dataStartGoal["goal"]["y"])

for o in dataObstacles["obstacles"]:
    x = o["x"]
    y = o["y"]
    obstacles.append((x, y))
