import neat
import os
import pickle
import random


class Training(object):
	def __init__(self, data_manager):
		self.data_manager = data_manager
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

		self.simulations = {}
		self.generation = 0

		local_dir = os.path.dirname(__file__)
		config_path = os.path.join(local_dir, 'config-feedforward')
	

	def eval_genomes(self, genomes, config):
		self.simulations[self.generation] = []
		for _, genome in genomes:
			pass

		self.generation += 1



def eval_genomes(genomes, config):
	random.shuffle(genomes)
	pairs = [(genomes[i][1], genomes[i+1][1]) if i < len(genomes) - 1 else (genomes[i][1], genomes[0][1]) for i in range(0, len(genomes), 2)]
	
	for pair in pairs:
		sim = Pong(left_cpu=neat.nn.FeedForwardNetwork.create(pair[0], config),
					right_cpu=neat.nn.FeedForwardNetwork.create(pair[1], config),
					display=False, config=config)
		pair[0].fitness, pair[1].fitness = sim.get_fitness()


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())

    # Run for up to 30 generations.
    winner = p.run(eval_genomes, 50)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    pickle.dump(winner_net, open("winner_net.pkl", "wb"))

    # Show output of the most fit genome against training data.
    Pong(left_cpu=winner_net, right_cpu=winner_net, display=True, config=config)



if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    # run(config_path)
    net = pickle.load(open("winner_net.pkl", "rb"))
    Pong(right_cpu=net, display=True)

