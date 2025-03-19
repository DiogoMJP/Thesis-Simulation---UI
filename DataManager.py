import json


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
					sim["name"] : SimulationTemplate(
						sim["name"], sim["n_agents"], sim["agents_lifespan_min"], sim["agents_lifespan_range"], sim["width"],
						sim["height"], sim["food_spawn_rate"], sim["food_lifespan_min"], sim["food_lifespan_range"],
						sim["food_detection_radius"], sim["eating_number"], sim["max_time_steps"]
					)
					for sim in templates_save.values()
				}
		except:
			self.templates = {}

	def load_simulations(self):
		try:
			with open("saved_data/simulations.json", "r") as simulations_json:
				simulations_save = json.load(simulations_json)
				self.simulations = {}
				for sim in simulations_save.values():
					self.simulations[sim["name"]] = Simulation()
					self.simulations[sim["name"]].set_data_manager(self)
					self.simulations[sim["name"]].set_name(sim["name"])
					self.simulations[sim["name"]].set_n_agents(sim["n_agents"])
					self.simulations[sim["name"]].set_agents_lifespan_min(sim["agents_lifespan_min"])
					self.simulations[sim["name"]].set_agents_lifespan_range(sim["agents_lifespan_range"])
					self.simulations[sim["name"]].set_width(sim["width"])
					self.simulations[sim["name"]].set_height(sim["height"])
					self.simulations[sim["name"]].set_food_spawn_rate(sim["food_spawn_rate"])
					self.simulations[sim["name"]].set_food_lifespan_min(sim["food_lifespan_min"])
					self.simulations[sim["name"]].set_food_lifespan_range(sim["food_lifespan_range"])
					self.simulations[sim["name"]].set_food_detection_radius(sim["food_detection_radius"])
					self.simulations[sim["name"]].set_eating_number(sim["eating_number"])
					self.simulations[sim["name"]].set_max_time_steps(sim["max_time_steps"])
					self.simulations[sim["name"]].set_time_step(sim["time_step"])
					self.simulations[sim["name"]].set_finished(sim["finished"])
					self.simulations[sim["name"]].set_agents(sim["agents"])
					self.simulations[sim["name"]].set_food(sim["food"])
					self.simulations[sim["name"]].set_last_time_step(sim["last_time_step"])
					self.simulations[sim["name"]].start_loop()
		except:
			self.simulations = {}
	

	def get_templates(self):
		return self.templates

	def get_simulations(self):
		return self.simulations

	
	def create_template(self, template):
		self.templates[template.get_name()] = template
		self.save_templates()
	
	def create_simulation(self, simulation):
		self.simulations[simulation.get_name()] = simulation
		self.save_simulations()
	

	def delete_template(self, template_name):
		self.templates.pop(template_name)
		self.save_templates()
	
	def delete_simulation(self, simulation_name):
		self.simulations.pop(simulation_name)
		self.save_simulations()

	
	def save_templates(self):
		with open("saved_data/simulation_templates.json", "w") as templates_json:
			json.dump({temp[0] : temp[1].to_dict() for temp in self.get_templates().items()}, templates_json)
		
	def save_simulations(self):
		with open("saved_data/simulations.json", "w") as simulations_json:
			json.dump({sim[0] : sim[1].to_dict() for sim in self.get_simulations().items()}, simulations_json)