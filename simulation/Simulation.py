import json
from pathlib import Path
from random import random
import threading
import time

from simulation.Agent import Agent
from simulation.Food import Food



class Simulation(object):
    def __init__(self, data_manager, path="saved_data/simulations/"):
        self.data_manager = data_manager
        self.path = path

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
        self.n_alive_agents = None
        self.last_time_step = None

        self.time_step = 0
        self.finished = False

        self.agents = []
        self.food = []
    

    def get_n_alive_agents(self):
        return len([1 for agent in self.agents if agent.alive])

    def increase_time_step(self):
        self.time_step += 1

    def set_agents(self, agent_list):
        for a in agent_list:
            agent = Agent(self.width, self.height, self.agents_lifespan_min,
                        self.agents_lifespan_range, a["life_expectancy"])
            agent.last_time_step = a["last_time_step"]
            agent.set_history(a["history"])
            agent.set_in_state("x", a["history"][-1][0])
            agent.set_in_state("y", a["history"][-1][1])
            agent.set_in_state("angle", a["history"][-1][2])
            agent.set_in_state("alive", a["history"][-1][3])
            self.agents += [agent]
    def set_food(self, food_list):
        for f in food_list:
            food = Food(self.width, self.height, self.eating_number, f["first_time_step"], f["life_expectancy"])
            food.detection_radius = self.food_detection_radius
            food.last_time_step = f["last_time_step"]
            food.x = f["history"][-1][0]
            food.y = f["history"][-1][1]
            self.food += [food]
    

    def create_agents(self):
        for _ in range(self.n_agents):
            agent = Agent(self.width, self.height, self.agents_lifespan_min, self.agents_lifespan_range,
                        int(self.agents_lifespan_min + self.agents_lifespan_range * random()))
            agent.set_in_state("x", int(random()*self.width))
            agent.set_in_state("y", int(random()*self.height))
            agent.set_in_state("angle", int(random()*360))
            agent.save_state()
            self.agents += [agent]
    

    def start_loop(self):
        if not self.finished:
            self.main_loop_thread = threading.Thread(target=self.main_loop, name="name", args=[])
            self.main_loop_thread.start()

    def main_loop(self):
        while not self.finished:
            if self.time_step >= self.max_time_steps or len([1 for a in self.agents if a.get_from_state("alive")]) == 0:
                self.finished = not self.finished
                self.last_time_step = self.time_step
            for food in self.food:
                food.simulate(self.time_step)
            for agent in self.agents:
                agent.simulate(self.time_step, self.food, self.agents)
            if random() < self.food_spawn_rate:
                food = Food(self.width, self.height, self.eating_number, self.time_step,
                            int(self.food_lifespan_min + self.food_lifespan_range * random()))
                food.x = int(random()*self.width)
                food.y = int(random()*self.height)
                food.detection_radius = self.food_detection_radius
                self.food += [food]
            self.increase_time_step()
        for agent in self.agents:
            if agent.last_time_step == None: agent.last_time_step = self.time_step
        for food in self.food:
            if food.last_time_step == None: food.last_time_step = self.time_step
        self.save()
    

    def get_list_data(self):
        return (self.name, self.finished)
    

    def get_update_data(self):
        update_data = {
            "time_step" : self.time_step,
            "finished" : self.finished
        }
        
        update_data["background"] = {
            "x" : 0, "y" : 0,
            "width" : self.width,
            "height" : self.height
        }

        update_data["food"] = []
        for food in self.food:
            if food.alive:
                update_data["food"] += [{
                    "x" : food.x,
                    "y" : food.x,
                    "detection_radius" : food.detection_radius
                }]

        update_data["agents"] = []
        for agent in self.agents:
            if agent.get_from_state("alive"):
                update_data["agents"] += [{
                    "x" : agent.get_from_state("x"),
                    "y" : agent.get_from_state("y")
                }]

        return update_data
    

    def get_update_data_from_time_step(self, time_step):
        update_data = {
            "time_step" : time_step,
            "last_time_step" : self.last_time_step
        }
        
        update_data["background"] = {
            "x" : 0, "y" : 0,
            "width" : self.width,
            "height" : self.height
        }

        update_data["food"] = []
        for food in self.food:
            if time_step >= food.first_time_step and time_step < food.last_time_step:
                update_data["food"] += [{
                    "x" : food.x,
                    "y" : food.y,
                    "detection_radius" : food.detection_radius
                }]

        update_data["agents"] = []
        for agent in self.agents:
            if time_step < agent.last_time_step:
                update_data["agents"] += [{
                    "x" : agent.get_from_history(time_step, "x"),
                    "y" : agent.get_from_history(time_step, "y")
                }]

        return update_data
    

    def to_dict(self):
        return {
            "name" : self.name, 
            "n-agents" : self.n_agents,
            "agents-lifespan-min" : self.agents_lifespan_min,
            "agents-lifespan-range" : self.agents_lifespan_range,
            "width" : self.width,
            "height" : self.height,
            "food-spawn-rate" : self.food_spawn_rate,
            "food-lifespan-min" : self.food_lifespan_min,
            "food-lifespan-range" : self.food_lifespan_range,
            "food-detection-radius" : self.food_detection_radius,
            "eating-number" : self.eating_number,
            "max_time-steps" : self.max_time_steps,
            "time-step" : self.time_step,
            "finished" : self.finished,
            "last-time-step" : self.last_time_step
        }
    
    def from_dict(self, data):
        if "name" in data: self.name = data["name"]
        if "n-agents" in data: self.n_agents = data["n-agents"]
        if "agents-lifespan-min" in data: self.agents_lifespan_min = data["agents-lifespan-min"]
        if "agents-lifespan-range" in data: self.agents_lifespan_range = data["agents-lifespan-range"]
        if "width" in data: self.width = data["width"]
        if "height" in data: self.height = data["height"]
        if "food-spawn-rate" in data: self.food_spawn_rate = data["food-spawn-rate"]
        if "food-lifespan-min" in data: self.food_lifespan_min = data["food-lifespan-min"]
        if "food-lifespan-range" in data: self.food_lifespan_range = data["food-lifespan-range"]
        if "food-detection-radius" in data: self.food_detection_radius = data["food-detection-radius"]
        if "eating-number" in data: self.eating_number = data["eating-number"]
        if "max-time-steps" in data: self.max_time_steps = data["max-time-steps"]
        if "time-step" in data: self.time_step = data["time-step"]
        if "finished" in data: self.finished = data["finished"]
        if "last-time-step" in data: self.last_time_step = data["last-time-step"]
    

    def save(self):
        Path(self.path + self.name).mkdir(parents=True, exist_ok=True)
        with open(self.path + self.name + "/simulation.json", "w+") as simulation_json:
            json.dump(self.to_dict(), simulation_json)
        with open(self.path + self.name + "/agents.json", "w+") as agents_json:
            json.dump([agent.to_dict() for agent in self.agents], agents_json)
        with open(self.path + self.name + "/food.json", "w+") as food_json:
            json.dump([food.to_dict() for food in self.food], food_json)

    def load(self, name):
        with open(self.path + name + "/simulation.json", "r") as simulation_json:
            self.from_dict(json.load(simulation_json))
        with open(self.path + name + "/agents.json", "r") as agents_json:
            self.set_agents(json.load(agents_json))
        with open(self.path + name + "/food.json", "r") as food_json:
            self.set_food(json.load(food_json))
    

    def delete(self):
        Path(self.path + self.name + "/agents.json").unlink()
        Path(self.path + self.name + "/food.json").unlink()
        Path(self.path + self.name + "/simulation.json").unlink()
        Path(self.path + self.name).rmdir()