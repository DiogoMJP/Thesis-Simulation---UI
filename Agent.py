from math import cos, sin, radians
from random import random



class Agent(object):
    def __init__(self, width, height, life_expectancy):
        self.width = width
        self.height = height
        self.life_expectancy = life_expectancy
        self.state = {"x" : None, "y" : None, "angle" : None, "alive" : True}
        self.last_time_step = None
        self.history = []


    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def get_life_expectancy(self):
        return self.life_expectancy
    def get_last_time_step(self):
        return self.last_time_step
    def get_from_state(self, key):
        return self.state[key]
    def get_from_history(self, time_step, key):
        return self.history[time_step][key]
    def get_history(self):
        return self.history
    
    def set_width(self, width):
        self.width = width
    def set_height(self, height):
        self.height = height
    def set_life_expectancy(self, life_expectancy):
        self.life_expectancy = life_expectancy
    def set_last_time_step(self, last_time_step):
        self.last_time_step = last_time_step
    def set_in_state(self, key, value):
        self.state[key] = value
    def set_history(self, history):
        for state in history:
            self.history += [{"x" : state[0], "y": state[1], "angle" : state[2], "alive": state[3]}]
    def save_state(self):
        self.history += [{
            "x" : self.get_from_state("x"),
            "y" : self.get_from_state("y"),
            "angle" : self.get_from_state("angle"),
            "alive" : self.get_from_state("alive")
        }]


    def simulate(self, time_step, angle, dist, food):
        if self.get_from_state("alive"):
            if (time_step >= self.get_life_expectancy()):
                self.set_in_state("alive", False)
                self.set_last_time_step(time_step)
            if angle == None:
                change = 0 if random() < 0.2 else -3 if random() < 0.5 else 3
                self.set_in_state("angle", self.get_from_state("angle") + change)
                self.set_in_state("angle", (self.get_from_state("angle") + 180) % 360 - 180)
            else:
                self.set_in_state("angle", angle)
                if dist < 10:
                    food.set_eaten(food.get_eaten() + 1)
                    self.set_life_expectancy(self.get_life_expectancy() + int(50 + 50 * random()))

            self.set_in_state("x", int((self.get_from_state("x") + cos(radians(self.get_from_state("angle"))) * 4) % self.get_width()))
            self.set_in_state("y", int((self.get_from_state("y") + sin(radians(self.get_from_state("angle"))) * 4) % self.get_height()))
            self.save_state()
    

    def to_dict(self):
        return {
            "life_expectancy" : self.get_life_expectancy(),
            "last_time_step" : self.get_last_time_step(),
            "history" : [(state["x"], state["y"], state["angle"], state["alive"]) for state in self.get_history()]
        }