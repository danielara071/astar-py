from mesa import Agent, Model
from mesa.space import MultiGrid
import mesa

class WallE(mesa.Agent):
    def __init__(self, model):
        super().__init__(model)

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


    def step(self):
        print(self.pos)
        self.move_right()
        

class Grid(mesa.Model):
    def __init__(self, seed=None):
        super().__init__(seed=None)
        #create 5 by 5 grid 
        self.grid = mesa.space.MultiGrid(5, 5, torus=False)

        wall_E = WallE(self)
        self.agents.add(wall_E)
        #way of making the agents "act"
        self.grid.place_agent(wall_E, (0,0))


    
    def print_grid(self):
        for y in reversed(range(self.grid.height)):
            row = ""
            for x in range(self.grid.width):
                cell = self.grid.get_cell_list_contents((x, y))
                if cell:
                    #if wall-e here print special indicator
                    row += "[W]"
                else:
                    row += "[ ]"
            print(row)
        print("\n")

    def step(self):
        self.print_grid()
        self.agents.shuffle_do("step")

#run model with agent 
model = Grid()
for i in range(5):
    model.step()
