from mesa import Agent, Model
from mesa.space import MultiGrid
import mesa
import des
import search
import json



class Obstacle(mesa.Agent):
    def __init__(self, model):
        super().__init__(model)

class WallE(mesa.Agent):
    def __init__(self, model):
        super().__init__(model)
        self.path = None
        self.path_len = None
        self.it = 0

    def at_destination(self):
        return self.pos[0] == 4  

    def move_right(self):
        #check if at destination, if not just move it 
        if not self.at_destination():
            x, y = self.pos
            new_pos = (x + 1, y)
            self.model.grid.move_agent(self, new_pos)
        else:
            print("Reached Destination!!!")

    def a_star(self, start, dest):
        self.path = search.find_path(start, dest)
        self.path_len = len(self.path) 

    
    def move(self, i):
        if self.it > self.path_len -1 :
            return
        x, y = self.path[i][0], self.path[i][1]
        new_pos = (x, y)
        self.model.grid.move_agent(self, new_pos)
        self.it += 1

    def step(self):
        self.move(self.it)


class Grid(mesa.Model):
    def __init__(self, seed=None):
        super().__init__(seed=None)
        #create grid
        self.size = des.size
        self.grid = mesa.space.MultiGrid(self.size.n, self.size.m, torus=False)
        for o in des.obstacles:
            obstacle = Obstacle(self)
            self.agents.add(obstacle)
            self.grid.place_agent(obstacle,(o[0], o[1]))

        wall_E = WallE(self)
        self.agents.add(wall_E)
        #way of making the agents "act"
        self.grid.place_agent(wall_E, (0,0))

        wall_E.a_star(des.start, des.goal)
        self.steps = wall_E.path_len + 1
        self.path = wall_E.path

    
    def print_grid(self):
        for y in reversed(range(self.grid.height)):
            row = ""
            for x in range(self.grid.width):
                cell = self.grid.get_cell_list_contents((x, y))
                if not cell:
                    row += "[ ]"
                elif isinstance(cell[-1], WallE):
                    #if wall-e here print special indicator
                    row += "[W]"
                elif isinstance(cell[-1], Obstacle):
                    row += "[O]"
                
            print(row)
        print("\n")

    def step(self):
        self.print_grid()
        self.agents.shuffle_do("step")

#run model with agent 
model = Grid()
solution = model.path       

json_ready = [{"x": x, "y": y} for x, y in solution]

json_out = json.dumps(json_ready, indent=4)

savePath = "save path aqui"

with open(savePath, "w") as f:
    f.write(json_out)


for i in range(model.steps):
    model.step()



