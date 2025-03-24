import json
import os

from simulation.SimulationTemplate import SimulationTemplate
from simulation.Simulation import Simulation


class DataManager(object):
	def __init__(self):
		self.templates = None
		self.simulations = None
		self.load_templates()
		self.load_simulations()

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

	def load_simulations(self):
		self.simulations = {}
		for dir in os.listdir("saved_data/simulations"):
			self.simulations[dir] = Simulation(self)
			self.simulations[dir].load(dir)
	

	def get_templates(self):
		return self.templates

	def get_simulations(self):
		return self.simulations

	
	def create_template(self, template):
		self.templates[template.get_name()] = template
		self.save_templates()
	
	def create_simulation(self, simulation):
		self.simulations[simulation.get_name()] = simulation
	

	def delete_template(self, template_name):
		self.templates.pop(template_name)
		self.save_templates()
	
	def delete_simulation(self, simulation_name):
		self.simulations[simulation_name].delete()
		self.simulations.pop(simulation_name)

	
	def save_templates(self):
		with open("saved_data/simulation_templates.json", "w") as templates_json:
			json.dump({temp[0] : temp[1].to_dict() for temp in self.get_templates().items()}, templates_json)