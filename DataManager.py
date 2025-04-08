import json
import os

from loader.SimulationLoader import SimulationLoader
from loader.TrainingLoader import TrainingLoader
import pickle
from simulation.SimulationTemplate import SimulationTemplate


class DataManager(object):
	def __init__(self):
		self.templates = None
		self.simulations = None
		self.training = None
		self.load_templates()
		self.load_simulations()
		self.load_training()

	def load_templates(self):
		try:
			with open("saved_data/simulation_templates.json", "r") as templates_json:
				templates_save = json.load(templates_json)
				self.templates = {
					data["name"] : SimulationTemplate(data)
					for data in templates_save.values()
				}
		except:
			self.templates = {}
	def get_templates(self):
		return self.templates
	def get_template(self, template_name):
		return self.templates[template_name]
	def create_template(self, template):
		self.templates[template.name] = template
		self.save_templates()
	def delete_template(self, template_name):
		self.templates.pop(template_name)
		self.save_templates()
	
	def load_simulations(self):
		self.simulations = {}
		for file in os.listdir("saved_data/simulations"):
			self.simulations[file.split(".")[0]] = pickle.load(open("saved_data/simulations/" + file, "rb"))
	def get_simulations(self):
		return self.simulations
	def get_simulation(self, simulation_name):
		return self.simulations[simulation_name]
	def create_simulation(self, simulation):
		self.simulations[simulation.name] = simulation
	def delete_simulation(self, simulation_name):
		self.simulations[simulation_name].delete()
		self.simulations.pop(simulation_name)
	
	def load_training(self):
		self.training = {}
		for dir in os.listdir("saved_data/training"):
			self.training[dir] = TrainingLoader(self)
			self.training[dir].load(dir)
	def get_trainings(self):
		return self.training
	def get_training(self, training_name):
		return self.training[training_name]
	def create_training(self, training):
		self.training[training.name] = training
	def delete_training(self, training_name):
		self.training[training_name].delete()
		self.training.pop(training_name)

	
	def save_templates(self):
		with open("saved_data/simulation_templates.json", "w") as templates_json:
			json.dump({temp[0] : temp[1].to_dict() for temp in self.get_templates().items()}, templates_json)