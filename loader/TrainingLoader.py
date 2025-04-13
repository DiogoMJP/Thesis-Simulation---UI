import json
import neat
import os
from pathlib import Path
import pickle
import random
from string import Template
import threading

from simulation.brain.NeatBrain import NeatBrain
from loader.SimulationLoader import SimulationLoader


class TrainingLoader(object):
	def __init__(self):
		self.path = "saved_data/training/"

		self.no_fitness_termination = False
		self.fitness_threshold = None
		self.pop_size = None
		self.reset_on_extinction = None
		self.num_inputs = None
		self.num_outputs = None
		self.n_generations = None

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
		self.finished = True

		self.simulations = {}
		self.generation = 0

	
	def get_list_data(self):
		return (self.name, self.finished)
	
	def get_gens_data(self):
		return [
			(gen, all([sim.finished for sim in sims.values()]))
			for gen, sims in self.simulations.items()
		]
	
	def get_gen_data(self, generation):
		return [(sim.name, sim.finished) for sim in self.simulations[generation].values()]
	
	def get_simulation(self, generation, simulation):
		if generation in self.simulations:
			if simulation in self.simulations[generation]:
				return self.simulations[generation][simulation]
			else: return None
		else: return None
	

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
            "max-time-steps" : self.max_time_steps,
            "time-step" : self.time_step,
            "finished" : self.finished,
			"no_fitness_termination" : self.no_fitness_termination,
			"fitness_threshold" : self.fitness_threshold,
			"pop_size" : self.pop_size,
			"reset_on_extinction" : self.reset_on_extinction,
			"num_inputs" : self.num_inputs,
			"num_outputs" : self.num_outputs,
			"n_generations" : self.n_generations
        }
	def from_dict(self, data):
		self.name = data["name"]
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
		self.no_fitness_termination = data["no_fitness_termination"]
		self.fitness_threshold = data["fitness_threshold"]
		self.pop_size = data["pop_size"]
		self.reset_on_extinction = data["reset_on_extinction"]
		self.num_inputs = data["num_inputs"]
		self.num_outputs = data["num_outputs"]
		self.n_generations = data["n_generations"]
	

	def save(self):
		pickle.dump(self, open(self.path + self.name + ".pkl", "wb+"))
	def delete(self):
		Path(self.path + self.name + ".pkl").unlink(missing_ok=True)