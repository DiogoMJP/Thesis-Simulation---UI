import neat
from pathlib import Path
from string import Template
import threading

from loader.TrainingLoader import TrainingLoader
from simulation.brain.NeatBrain import NeatBrain
from simulation.Simulation import Simulation


class Training(object):
	def __init__(self, data_manager):
		self.data_manager = data_manager
		self.path = "saved_data/training/"

		self.no_fitness_termination = False
		self.fitness_threshold = 10000
		self.pop_size = 50
		self.reset_on_extinction = True
		self.num_inputs = 4
		self.num_outputs = 3
		self.n_generations = 50

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
		self.deleted = False

		self.simulations = {}
		self.generation = 0
	

	def set_config_file(self):
		config_data = {
			"no_fitness_termination": self.no_fitness_termination,
			"fitness_threshold": self.fitness_threshold,
			"pop_size": self.pop_size,
			"reset_on_extinction": self.reset_on_extinction,
			"num_inputs": self.num_inputs,
			"num_outputs": self.num_outputs
		}
		with open("templates/config-template", 'r') as template_file:
			src = Template(template_file.read())
			with open(self.path+self.name+"-config", 'w+') as config_file:
				config_file.write(src.substitute(config_data))

	
	def start_training(self):
		self.training_thread = threading.Thread(target=self.training, name="name", args=[])
		self.training_thread.start()

	def training(self):
		# Load configuration.
		config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
							neat.DefaultSpeciesSet, neat.DefaultStagnation,
							self.path + self.name + "-config")

		# Create the population, which is the top-level object for a NEAT run.
		pop = neat.Population(config)

		# Run for up to 30 generations.
		winner = pop.run(self.eval_genomes, self.n_generations)

		winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

		self.brain = NeatBrain(winner_net)

		if not self.deleted:
			self.save_replay()
		self.finished = True
	
	def eval_genomes(self, genomes, config):
		self.simulations[str(self.generation)] = {}
		for id, genome in genomes:
			network = neat.nn.FeedForwardNetwork.create(genome, config)
			brain = NeatBrain(network)
			data = {
				"name" : str(id),
				"training" : True,
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
				"max-time-steps" : self.max_time_steps
			}
			sim = Simulation(self.data_manager, path="saved_data/training/"+self.name+"/simulations/"+str(self.generation)+"/", training=True)
			sim.from_dict(data)
			sim.brain = brain
			sim.create_agents()
			sim.start_loop()
			sim.brain = brain
			self.simulations[str(self.generation)][str(id)] = (sim, genome)
		while not all([sim.finished for sim, _ in self.simulations[str(self.generation)].values()]):
			pass
		for id, pair in self.simulations[str(self.generation)].items():
			pair[1].fitness = pair[0].last_time_step / pair[0].max_time_steps

		self.generation += 1
	

	def get_list_data(self):
		return (self.name, self.finished)
	
	def get_gens_data(self):
		return [
			(gen, all([sim.finished for sim, _ in sims.values()]))
			for gen, sims in self.simulations.items()
		]
	
	def get_gen_data(self, generation):
		return [(sim.name, sim.finished) for sim, _ in self.simulations[generation].values()]
	
	def get_simulation(self, generation, simulation):
		if generation in self.simulations:
			if simulation in self.simulations[generation]:
				return self.simulations[generation][simulation][0]
			else: return None
		else: return None
	
	def get_live_page_data(self, generation, simulation):
		return {
			"training" : self.name,
			"generation" : generation,
            "name" : simulation.name,
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
            "finished" : simulation.finished,
            "brain" : self.brain.to_dict()
        }
	
	def get_finished_page_data(self, generation, simulation):
		return {
			"training" : self.name,
			"generation" : generation,
            "name" : simulation.name,
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
            "last-time-step" : simulation.last_time_step,
			"food" : [food.to_dict() for food in simulation.food],
			"agents" : [agent.to_dict() for agent in simulation.agents]
        }
	

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
			"no-fitness-termination" : self.no_fitness_termination,
			"fitness-threshold" : self.fitness_threshold,
			"pop-size" : self.pop_size,
			"reset-on-extinction" : self.reset_on_extinction,
			"num-inputs" : self.num_inputs,
			"num-outputs" : self.num_outputs,
			"n-generations" : self.n_generations
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
		if "no-fitness-termination" in data: self.no_fitness_termination = data["no-fitness-termination"]
		if "fitness-threshold" in data: self.fitness_threshold = data["fitness-threshold"]
		if "pop-size" in data: self.pop_size = data["pop-size"]
		if "reset-on-extinction" in data: self.reset_on_extinction = data["reset-on-extinction"]
		if "num-inputs" in data: self.num_inputs = data["num-inputs"]
		if "num-outputs" in data: self.num_outputs = data["num-outputs"]
		if "n-generations" in data: self.n_generations = data["n-generations"]
	

	def save_replay(self):
		self.replay = TrainingLoader()
		self.replay.from_dict(self.to_dict())
		simulations = {
			gen : {id : sim[0].get_replay() for id, sim in sims.items()}
			for gen, sims in self.simulations.items()
		}
		self.replay.simulations = simulations
		self.replay.save()
		print("saved!")
		Path(self.path + self.name + "-config").unlink(missing_ok=True)
		self.saved = True
	def delete(self):
		self.deleted = True
		Path(self.path + self.name + "-config").unlink(missing_ok=True)
		Path(self.path + self.name + ".pkl").unlink(missing_ok=True)
	

	def get_url(self):
		return f"/training/{self.name}"