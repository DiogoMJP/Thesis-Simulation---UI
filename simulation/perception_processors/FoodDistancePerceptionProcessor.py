from math import atan2, degrees, sqrt
from random import random



class FoodDistancePerceptionProcessor(object):
	def __init__(self):
		pass
	

	def process_input(self, state, food_list, agent_list):
		x = state["x"]; y = state["y"]
		closest_x = None; closest_y = None; dist = None; closest = None
		
		for food in food_list:
			if food.alive:
				if dist == None:
					dist = (x-food.x)**2 + (y-food.y)**2
					closest_x = food.x; closest_y = food.y
					closest = food
				else:
					d = (x-food.x)**2 + (y-food.y)**2
					if d < dist:
						dist = d
						closest_x = food.x; closest_y = food.y
						closest = food
		
		if dist != None and sqrt(dist) < food.detection_radius:
			angle = degrees(atan2(closest_y - y, closest_x - x))
			return (angle - state["angle"], sqrt(dist), closest)
		else:
			return (None, None, None)