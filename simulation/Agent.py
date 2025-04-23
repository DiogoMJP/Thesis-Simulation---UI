from math import cos, sin, radians
from random import random



class Agent(object):
    def __init__(self, brain, width, height, lifespan_extension_min, lifespan_extension_range, life_expectancy):
        self.width = width
        self.height = height
        self.lifespan_extension_min = lifespan_extension_min
        self.lifespan_extension_range = lifespan_extension_range
        self.life_expectancy = life_expectancy
        self.state = {"x" : None, "y" : None, "angle" : None, "alive" : True}
        self.last_time_step = None
        self.history = []
        self.brain = brain
        self.alive = True


    def get_from_state(self, key):
        return self.state[key]
    def get_from_history(self, time_step, key):
        return self.history[time_step][key]
    
    def prolong_life_expectancy(self):
        self.life_expectancy += self.lifespan_extension_min + int(self.lifespan_extension_range * random())
    def set_in_state(self, key, value):
        self.state[key] = value
    def set_history(self, history):
        for state in history:
            self.history += [{"x" : state[0], "y": state[1], "angle" : state[2]}]
    def save_state(self):
        self.history += [{
            "x" : self.get_from_state("x"),
            "y" : self.get_from_state("y"),
            "angle" : self.get_from_state("angle")
        }]


    def simulate(self, time_step, food_list, agent_list):
        if self.alive:
            if (time_step >= self.life_expectancy):
                self.alive = False
                self.last_time_step = time_step
            
            else:
                l_rot, r_rot, speed, dist, food = self.brain.get_action(self.state, food_list, agent_list)
                change = -3 if l_rot else 3 if r_rot else 0
                self.set_in_state("angle", self.get_from_state("angle") + change)
                self.set_in_state("angle", (self.get_from_state("angle") + 180) % 360 - 180)
                if speed:
                    self.set_in_state("x", int((self.get_from_state("x") + cos(radians(self.get_from_state("angle"))) * 4) % self.width))
                    self.set_in_state("y", int((self.get_from_state("y") + sin(radians(self.get_from_state("angle"))) * 4) % self.height))
                if dist != None and dist < 15:
                    food.eaten += [self]
            self.save_state()
    

    def to_dict(self):
        return {
            "life-expectancy" : self.life_expectancy,
            "last-time-step" : self.last_time_step,
            "alive" : self.alive,
            "history" : [(state["x"], state["y"], state["angle"]) for state in self.history]
        }