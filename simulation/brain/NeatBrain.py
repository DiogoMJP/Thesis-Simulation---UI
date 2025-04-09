from random import random

from simulation.perception_processors.PerceptionProcessor import PerceptionProcessor



class NeatBrain(object):
	def __init__(self, neat_net):
		self.neat_net = neat_net
		
		self.n_input = 2
		self.n_output = 3

		self.perception_processor = PerceptionProcessor()

	
	def get_action(self, state, food_list, agent_list):
		angle, dist, food = self.perception_processor.process_input(state, food_list, agent_list)
		
		input = [angle, dist] if angle != None else [500, 500]
		
		output = self.neat_net.activate(input)
		l_rot = 1 if output[0] >= 0.5 else 0
		r_rot = 1 if output[1] >= 0.5 else 0
		speed = 1 if output[2] >= 0.5 else 0
		
		return l_rot, r_rot, speed, dist, food
	

	def to_dict(self):
		return {"type" : "neatbrain"}