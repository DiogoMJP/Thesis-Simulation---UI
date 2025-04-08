import json
from pathlib import Path
import pickle

from simulation.Agent import Agent
from simulation.Food import Food



class SimulationLoader(object):
    def __init__(self, path="saved_data/simulations/"):
        self.path = path
        self.training = None
        self.main_loop_thread = None

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

        self.brain = None
        self.agents = []
        self.food = []


    def set_agents(self, agent_list):
        for a in agent_list:
            agent = Agent(self.brain, self.width, self.height, self.agents_lifespan_min,
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
            food.x = f["x"]
            food.y = f["y"]
            self.food += [food]
    

    def get_list_data(self):
        return (self.name, self.finished)
    

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
        self.name = data["name"]
        self.training = data["training"]
        self.n_agents = data["n-agents"]
        self.agents_lifespan_min = data["agents-lifespan-min"]
        self.agents_lifespan_range = data["agents-lifespan-range"]
        self.width = data["width"]
        self.height = data["height"]
        self.food_spawn_rate = data["food-spawn-rate"]
        self.food_lifespan_min = data["food-lifespan-min"]
        self.food_lifespan_range = data["food-lifespan-range"]
        self.food_detection_radius = data["food-detection-radius"]
        self.eating_number = data["eating-number"]
        self.max_time_steps = data["max-time-steps"]
        self.time_step = data["time-step"]
        self.finished = data["finished"]
        self.last_time_step = data["last-time-step"]
    

    def save(self):
        pickle.dump(self, open(self.path + self.name + ".pkl", "wb+"))
    def delete(self):
        Path(self.path + self.name + ".pkl").unlink(missing_ok=True)