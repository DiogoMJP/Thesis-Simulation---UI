from pathlib import Path
import pickle
from random import random
import threading
import time

from simulation.brain.HardCodedBrain import HardCodedBrain
from simulation.brain.NeatBrain import NeatBrain
from simulation.Agent import Agent
from simulation.Food import Food
from loader.SimulationLoader import SimulationLoader



class Simulation(object):
    def __init__(self, data_manager, path="saved_data/simulations/", training = False):
        self.data_manager = data_manager
        self.path = path
        self.training = training
        self.main_loop_thread = None
        self.replay = None

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
        self.saved = False
        self.deleted = False

        self.agents = []
        self.food = []
    

    def get_n_alive_agents(self):
        return len([1 for agent in self.agents if agent.alive])

    def increase_time_step(self):
        self.time_step += 1
    

    def create_brain(self, brain):
        if brain["type"] == "neatbrain":
            self.brain = NeatBrain(pickle.load(open("net.pkl", "rb")))
        elif brain["type"] == "hardcodedbrain":
            self.brain = HardCodedBrain()
    def create_agents(self):
        for _ in range(self.n_agents):
            agent = Agent(self.brain, self.width, self.height, self.agents_lifespan_min, self.agents_lifespan_range,
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
            time.sleep(0.01)
            if self.time_step >= self.max_time_steps or len([1 for a in self.agents if a.alive]) == 0:
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
        if not self.training:
            self.save_replay()


    def get_list_data(self):
        return (self.name, self.finished)
    

    def get_live_data(self):
        update_data = {
            "time_step" : self.time_step,
            "finished" : self.finished,
            "n_agents" : self.get_n_alive_agents()
        }

        return update_data
    
    def get_full_update_data(self):
        update_data = {
            "last_time_step" : self.last_time_step,
            "detection_radius" : self.food_detection_radius
        }
        update_data["background"] = {
            "x" : 0, "y" : 0,
            "width" : self.width,
            "height" : self.height
        }
        update_data["food"] = [food.to_dict() for food in self.food]
        update_data["agents"] = [agent.to_dict() for agent in self.agents]

        return update_data
    

    def to_dict(self):
        return {
            "name" : self.name,
            "training" : self.training,
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
            "max-time-steps" : self.max_time_steps,
            "time-step" : self.time_step,
            "finished" : self.finished,
            "last-time-step" : self.last_time_step,
            "brain" : self.brain.to_dict()
        }
    def from_dict(self, data):
        if "name" in data: self.name = data["name"]
        if "training" in data: self.training = data["training"]
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
        if "brain" in data: self.create_brain(data["brain"])
    

    def get_replay(self):
        replay = SimulationLoader(self.path)
        replay.from_dict(self.to_dict())
        replay.set_agents([agent.to_dict() for agent in self.agents])
        replay.set_food([food.to_dict() for food in self.food])
        replay.brain = self.brain
        return replay
    def save_replay(self):
        replay = self.get_replay()
        replay.save()
        self.saved = True
    def delete(self):
        self.deleted = True
        Path(self.path + self.name + ".pkl").unlink(missing_ok=True)
    

    def save_replay(self):
        self.replay = SimulationLoader(self.path)
        self.replay.from_dict(self.to_dict())
        self.replay.set_agents([agent.to_dict() for agent in self.agents])
        self.replay.set_food([food.to_dict() for food in self.food])
        self.replay.brain = self.brain
        self.replay.save()