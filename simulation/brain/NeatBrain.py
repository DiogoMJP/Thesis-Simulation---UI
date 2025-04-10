from random import random

from simulation.perception_processors.FoodAgentDistancePerceptionProcessor import FoodAgentDistancePerceptionProcessor



class NeatBrain(object):
	def __init__(self, neat_net):
		self.neat_net = neat_net
		
		self.n_input = 4
		self.n_output = 3

		self.perception_processor = FoodAgentDistancePerceptionProcessor()

	
	def get_action(self, state, food_list, agent_list):
		f_angle, f_dist, food, a_angle, a_dist = self.perception_processor.process_input(state, food_list, agent_list)
		
		input = ([f_angle, f_dist] if f_angle != None else [500, 500]) + ([a_angle, a_dist] if a_angle != None else [500, 500])
		
		output = self.neat_net.activate(input)
		l_rot = 1 if output[0] >= 0.5 else 0
		r_rot = 1 if output[1] >= 0.5 else 0
		speed = 1 if output[2] >= 0.5 else 0
		
		return l_rot, r_rot, speed, f_dist, food
	

	def to_dict(self):
		return {"type" : "neatbrain"}