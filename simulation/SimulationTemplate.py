from random import random
import threading
import time

from simulation.Agent import Agent



class SimulationTemplate(object):
    def __init__(self, data = None):
        self.name = None
        self.n_agents = None
        self.agents_lifespan_min = None
        self.agents_lifespan_range = None
        self.width = None
        self.height = None
        self.food_spawn_rate = None
        self.food_lifespan_min = None
        self.food_lifespan_range = None
        self.food_detection_radius = None
        self.eating_number = None
        self.max_time_steps = None

        if data != None:
            self.load(data)
    

    def get_name(self):
        return self.name
    def get_n_agents(self):
        return self.n_agents
    def get_agents_lifespan_min(self):
        return self.agents_lifespan_min
    def get_agents_lifespan_range(self):
        return self.agents_lifespan_range
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def get_food_spawn_rate(self):
        return self.food_spawn_rate
    def get_food_lifespan_min(self):
        return self.food_lifespan_min
    def get_food_lifespan_range(self):
        return self.food_lifespan_range
    def get_food_detection_radius(self):
        return self.food_detection_radius
    def get_eating_number(self):
        return self.eating_number
    def get_max_time_steps(self):
        return self.max_time_steps

    def set_name(self, name):
        self.name = name
    def set_n_agents(self, n_agents):
        self.n_agents = n_agents
    def set_agents_lifespan_min(self, agents_lifespan_min):
        self.agents_lifespan_min = agents_lifespan_min
    def set_agents_lifespan_range(self, agents_lifespan_range):
        self.agents_lifespan_range = agents_lifespan_range
    def set_width(self, width):
        self.width = width
    def set_height(self, height):
        self.height = height
    def set_food_spawn_rate(self, food_spawn_rate):
        self.food_spawn_rate = food_spawn_rate
    def set_food_lifespan_min(self, food_lifespan_min):
        self.food_lifespan_min = food_lifespan_min
    def set_food_lifespan_range(self, food_lifespan_range):
        self.food_lifespan_range = food_lifespan_range
    def set_food_detection_radius(self, food_detection_radius):
        self.food_detection_radius = food_detection_radius
    def set_eating_number(self, eating_number):
        self.eating_number = eating_number
    def set_max_time_steps(self, max_time_steps):
        self.max_time_steps = max_time_steps


    def to_dict(self):
        return {
            "name" : self.get_name(), 
            "n-agents" : self.get_n_agents(),
            "agents-lifespan-min" : self.get_agents_lifespan_min(),
            "agents-lifespan-range" : self.get_agents_lifespan_range(),
            "width" : self.get_width(),
            "height" : self.get_height(),
            "food-spawn-rate" : self.get_food_spawn_rate(),
            "food-lifespan-min" : self.get_food_lifespan_min(),
            "food-lifespan-range" : self.get_food_lifespan_range(),
            "food-detection-radius" : self.get_food_detection_radius(),
            "eating-number" : self.get_eating_number(),
            "max-time-steps" : self.get_max_time_steps()
        }

    def load(self, data):
        self.set_name(data["name"])
        self.set_n_agents(data["n-agents"])
        self.set_agents_lifespan_min(data["agents-lifespan-min"])
        self.set_agents_lifespan_range(data["agents-lifespan-range"])
        self.set_width(data["width"])
        self.set_height(data["height"])
        self.set_food_spawn_rate(data["food-spawn-rate"])
        self.set_food_lifespan_min(data["food-lifespan-min"])
        self.set_food_lifespan_range(data["food-lifespan-range"])
        self.set_food_detection_radius(data["food-detection-radius"])
        self.set_eating_number(data["eating-number"])
        self.set_max_time_steps(data["max-time-steps"])