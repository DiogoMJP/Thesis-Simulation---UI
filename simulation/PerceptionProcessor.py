from math import atan2, degrees, sqrt
from random import random



class PerceptionProcessor(object):
	def __init__(self):
		pass
	

	def process_input(self, state, food_list, agent_list):
		x = state["x"]; y = state["y"]
		closest_x = None; closest_y = None; dist = None; closest = None
		
		for food in food_list:
			if food.get_from_state("alive"):
				if dist == None:
					dist = (x-food.get_from_state("x"))**2 + (y-food.get_from_state("y"))**2
					closest_x = food.get_from_state("x"); closest_y = food.get_from_state("y")
					closest = food
				else:
					d = (x-food.get_from_state("x"))**2 + (y-food.get_from_state("y"))**2
					if d < dist:
						dist = d
						closest_x = food.get_from_state("x"); closest_y = food.get_from_state("y")
						closest = food
		
		if dist != None and sqrt(dist) < food.detection_radius:
			angle = degrees(atan2(closest_y - y, closest_x - x))
			return (angle - state["angle"], sqrt(dist), closest)
		else:
			return (None, None, None)