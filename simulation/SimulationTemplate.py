from random import random
import threading
import time

from simulation.Agent import Agent



class SimulationTemplate(object):
    def __init__(self, name, n_agents, agents_lifespan_min, agents_lifespan_range, width, height, food_spawn_rate,
                 food_lifespan_min, food_lifespan_range, food_detection_radius, eating_number, max_time_steps):
        self.name = name
        self.n_agents = n_agents
        self.agents_lifespan_min = agents_lifespan_min
        self.agents_lifespan_range = agents_lifespan_range
        self.width = width
        self.height = height
        self.food_spawn_rate = food_spawn_rate
        self.food_lifespan_min = food_lifespan_min
        self.food_lifespan_range = food_lifespan_range
        self.food_detection_radius = food_detection_radius
        self.eating_number = eating_number
        self.max_time_steps = max_time_steps
    

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
    def set_width(self, width):
        self.width = width
    def set_height(self, height):
        self.height = height
    def set_food_spawn_rate(self, food_spawn_rate):
        self.food_spawn_rate = food_spawn_rate
    def set_food_detection_radius(self, food_detection_radius):
        self.food_detection_radius = food_detection_radius
    def set_max_time_steps(self, max_time_steps):
        self.max_time_steps = max_time_steps
    

    def to_dict(self):
        return {
            "name" : self.get_name(), 
            "n_agents" : self.get_n_agents(),
            "agents_lifespan_min" : self.get_agents_lifespan_min(),
            "agents_lifespan_range" : self.get_agents_lifespan_range(),
            "width" : self.get_width(),
            "height" : self.get_height(),
            "food_spawn_rate" : self.get_food_spawn_rate(),
            "food_lifespan_min" : self.get_food_lifespan_min(),
            "food_lifespan_range" : self.get_food_lifespan_range(),
            "food_detection_radius" : self.get_food_detection_radius(),
            "eating_number" : self.get_eating_number(),
            "max_time_steps" : self.get_max_time_steps()
        }