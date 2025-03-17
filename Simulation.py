from math import atan2, degrees, sqrt
from random import random
import threading
import time

from Agent import Agent
from Food import Food



class Simulation(object):
    def __init__(self):
        self.data_manager = None
        self.name = None
        self.n_agents = None
        self.width = None
        self.height = None
        self.food_spawn_rate = None
        self.food_detection_radius = None
        self.max_time_steps = None
        self.n_alive_agents = None

        self.agents = []
        self.food = []

        self.time_step = 0
        self.finished = False

        self.last_time_step = None
    

    def get_data_manager(self):
        return self.data_manager
    def get_name(self):
        return self.name
    def get_n_agents(self):
        return self.n_agents
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def get_food_spawn_rate(self):
        return self.food_spawn_rate
    def get_food_detection_radius(self):
        return self.food_detection_radius
    def get_max_time_steps(self):
        return self.max_time_steps
    def get_time_step(self):
        return self.time_step
    def get_n_alive_agents(self):
        return len([1 for agent in self.get_agents() if agent.get_alive()])
    def get_finished(self):
        return self.finished
    def get_agents(self):
        return self.agents
    def get_food(self):
        return self.food
    def get_last_time_step(self):
        return self.last_time_step

    def set_data_manager(self, data_manager):
        self.data_manager = data_manager
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
    def set_time_step(self, time_step):
        self.time_step = time_step
    def increase_time_step(self):
        self.time_step += 1
    def set_finished(self, finished):
        self.finished = finished
    def set_last_time_step(self, last_time_step):
        self.last_time_step = last_time_step

    def set_agents(self, agent_list):
        for a in agent_list:
            agent = Agent(self.get_width(), self.get_height(), a["life_expectancy"])
            agent.set_last_time_step(a["last_time_step"])
            agent.set_history(a["history"])
            agent.set_in_state("x", a["history"][-1][0])
            agent.set_in_state("y", a["history"][-1][1])
            agent.set_in_state("angle", a["history"][-1][2])
            agent.set_in_state("alive", a["history"][-1][3])
            self.agents += [agent]
    def set_food(self, food_list):
        for f in food_list:
            food = Food(self.get_width(), self.get_height(), f["first_time_step"], f["life_expectancy"])
            food.set_detection_radius(self.get_food_detection_radius())
            food.set_last_time_step(f["last_time_step"])
            food.set_history(f["history"])
            food.set_in_state("x", f["history"][-1][0])
            food.set_in_state("y", f["history"][-1][1])
            food.set_in_state("alive", f["history"][-1][2])
            self.food += [food]
    

    def create_agents(self):
        for _ in range(self.get_n_agents()):
            agent = Agent(self.get_width(), self.get_height(), int(100 + 100 * random()))
            agent.set_in_state("x", int(random()*self.get_width()))
            agent.set_in_state("y", int(random()*self.get_height()))
            agent.set_in_state("angle", int(random()*360))
            agent.save_state()
            self.agents += [agent]
    

    def start_loop(self):
        if not self.finished:
            self.main_loop_thread = threading.Thread(target=self.main_loop, name="name", args=[])
            self.main_loop_thread.start()

    def main_loop(self):
        while not self.get_finished():
            if self.get_time_step() >= self.get_max_time_steps() or len([1 for a in self.get_agents() if a.get_from_state("alive")]) == 0:
                self.set_finished(not self.get_finished())
                self.set_last_time_step(self.get_time_step())
            for food in self.get_food():
                food.simulate(self.get_time_step())
            for agent in self.get_agents():
                if len(self.get_food()) != 0:
                    x = agent.get_from_state("x"); y = agent.get_from_state("y")
                    closest_x = None; closest_y = None; dist = None; closest = None
                    for food in self.get_food():
                        if food.get_from_state("alive"):
                            if dist == None:
                                dist = (x-food.get_from_state("x"))**2 + (y-food.get_from_state("y"))**2
                                closest_x = food.get_from_state("x"); closest_y = food.get_from_state("y")
                                closest = food
                            else:
                                d = (x-food.get_from_state("x"))**2 + (y-food.get_from_state("y"))**2
                                if d < dist:
                                    dist = d
                                    closest_x = food.get_from_state("x"); closest_y = food.get_from_state("y")
                                    closest = food
                    if dist != None and sqrt(dist) < self.get_food_detection_radius():
                        angle = degrees(atan2(closest_y - y, closest_x - x))
                        agent.simulate(self.get_time_step(), angle, sqrt(dist), closest)
                    else:
                        agent.simulate(self.get_time_step(), None, None, None)
                else:
                    agent.simulate(self.get_time_step(), None, None, None)
            if random() < self.get_food_spawn_rate():
                food = Food(self.get_width(), self.get_height(), self.get_time_step(), int(25 + 25 * random()))
                food.set_in_state("x", int(random()*self.get_width()))
                food.set_in_state("y", int(random()*self.get_height()))
                food.set_detection_radius(self.get_food_detection_radius())
                self.food += [food]
            self.increase_time_step()
        for agent in self.get_agents():
            if agent.get_last_time_step() == None: agent.set_last_time_step(self.get_time_step())
        for food in self.get_food():
            if food.get_last_time_step() == None: food.set_last_time_step(self.get_time_step())
        self.data_manager.save_simulations()
    

    def get_list_data(self):
        return (self.get_name(), self.get_finished())
    

    def get_update_data(self):
        update_data = {
            "time_step" : self.get_time_step(),
            "finished" : self.get_finished()
        }
        
        update_data["background"] = {
            "x" : 0, "y" : 0,
            "width" : self.get_width(),
            "height" : self.get_height()
        }

        update_data["food"] = []
        for food in self.get_food():
            if food.get_from_state("alive"):
                update_data["food"] += [{
                    "x" : food.get_from_state("x"),
                    "y" : food.get_from_state("y"),
                    "detection_radius" : food.get_detection_radius()
                }]

        update_data["agents"] = []
        for agent in self.get_agents():
            if agent.get_from_state("alive"):
                update_data["agents"] += [{
                    "x" : agent.get_from_state("x"),
                    "y" : agent.get_from_state("y")
                }]

        return update_data
    

    def get_update_data_from_time_step(self, time_step):
        update_data = {
            "time_step" : time_step,
            "last_time_step" : self.get_last_time_step()
        }
        
        update_data["background"] = {
            "x" : 0, "y" : 0,
            "width" : self.get_width(),
            "height" : self.get_height()
        }

        update_data["food"] = []
        for food in self.get_food():
            if time_step >= food.get_first_time_step() and time_step < food.get_last_time_step():
                update_data["food"] += [{
                    "x" : food.get_from_history(time_step, "x"),
                    "y" : food.get_from_history(time_step, "y"),
                    "detection_radius" : food.get_detection_radius()
                }]

        update_data["agents"] = []
        for agent in self.get_agents():
            if time_step < agent.get_last_time_step():
                update_data["agents"] += [{
                    "x" : agent.get_from_history(time_step, "x"),
                    "y" : agent.get_from_history(time_step, "y")
                }]

        return update_data
    

    def to_dict(self):
        return {
            "name" : self.get_name(), 
            "n_agents" : self.get_n_agents(),
            "width" : self.get_width(),
            "height" : self.get_height(),
            "food_spawn_rate" : self.get_food_spawn_rate(),
            "food_detection_radius" : self.get_food_detection_radius(),
            "max_time_steps" : self.get_max_time_steps(),
            "time_step" : self.get_time_step(),
            "finished" : self.get_finished(),
            "agents" : [agent.to_dict() for agent in self.get_agents()],
            "food" : [food.to_dict() for food in self.get_food()],
            "last_time_step" : self.get_last_time_step()
        }