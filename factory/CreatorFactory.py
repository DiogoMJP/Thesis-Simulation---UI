from simulation.brain.HardCodedBrain import HardCodedBrain
from simulation.Simulation import Simulation
from simulation.Training import Training


class CreatorFactory(object):
	def __init__(self, data_manager):
		self.data_manager = data_manager
		self.type_to_func = {
			"simulation" : self.create_simulation,
			"training" : self.create_training
		}
	
	def create(self, data: dict):
		data["n-agents"] = int(data["n-agents"])
		data["agents-lifespan-min"] = int(data["agents-lifespan-min"])
		data["agents-lifespan-range"] = int(data["agents-lifespan-range"])
		data["width"] = int(data["width"])
		data["height"] = int(data["height"])
		data["food-spawn-rate"] = float(data["food-spawn-rate"])
		data["food-lifespan-min"] = int(data["food-lifespan-min"])
		data["food-lifespan-range"] = int(data["food-lifespan-range"])
		data["food-detection-radius"] = float(data["food-detection-radius"])
		data["eating-number"] = int(data["eating-number"])
		data["max-time-steps"] = int(data["max-time-steps"])
		
		if "created-type" in data:
			if data["created-type"] == "simulation":
				return self.create_simulation(data)
			elif data["created-type"] == "training":
				return self.create_training(data)
			else:
				raise Exception("Attempted to create unavailable type.")
		else:
			raise Exception("Attempted to create without providing a 'created-type'")

	def create_simulation(self, data):
		if data["name"] not in self.data_manager.get_simulations():
			simulation = Simulation(self.data_manager)
			simulation.from_dict(data)
			simulation.brain = HardCodedBrain()
			simulation.create_agents()
			simulation.start_loop()
			self.data_manager.create_simulation(simulation)
			return simulation
		else:
			raise Exception("Attempted to create an already existing simulation")

	def create_training(self, data):
		if data["name"] not in self.data_manager.get_trainings():
			data["no-fitness-termination"] = data["no-fitness-termination"] == "True"
			data["pop-size"] = int(data["pop-size"])
			data["reset-on-extinction"] = data["reset-on-extinction"] == "True"
			data["n-generations"] = int(data["n-generations"])
			data["no-fitness-termination"] = data["no-fitness-termination"] == "True"
			data["no-fitness-termination"] = data["no-fitness-termination"] == "True"
			training = Training(self.data_manager)
			training.from_dict(data)
			training.set_config_file()
			training.start_training()
			self.data_manager.create_training(training)
			return training
		else:
			raise Exception("Attempted to create an already existing training")