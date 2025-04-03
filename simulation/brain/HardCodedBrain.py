from random import random

from simulation.PerceptionProcessor import PerceptionProcessor



class HardCodedBrain(object):
	def __init__(self):
		self.perception_processor = PerceptionProcessor()

	
	def get_action(self, state, food_list, agent_list):
		angle, dist, food = self.perception_processor.process_input(state, food_list, agent_list)
		l_rot = 0; r_rot = 0; speed = 0; eat = 0
		if angle == None:
			if random() >= 0.2:
				if random() < 0.5: l_rot = 1
				else: r_rot = 1
			speed = 1
		else:
			if angle > 180: l_rot = 1; speed = 0
			elif angle < -180: r_rot = 1; speed = 0
			elif angle < -5: l_rot = 1; speed = 0
			elif angle > 5: r_rot = 1; speed = 0
			else: speed = 1
			if dist < 5: speed = 0
		
		return l_rot, r_rot, speed, dist, food


	def to_dict(self):
		return {"type" : "hardcodedbrain"}