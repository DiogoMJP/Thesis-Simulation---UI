from math import atan2, degrees, sqrt
from random import random



class FoodAgentDistancePerceptionProcessor(object):
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
			f_angle = degrees(atan2(closest_y - y, closest_x - x))
			f_dist = sqrt(dist)
			f_closest = closest
		else:
			f_angle = None
			f_dist = None
			f_closest = None
		
		for agent in agent_list:
			if agent.alive:
				if dist == None:
					dist = (x-agent.get_from_state("x"))**2 + (y-agent.get_from_state("x"))**2
					closest_x = agent.get_from_state("x"); closest_y = agent.get_from_state("y")
				else:
					d = (x-agent.get_from_state("x"))**2 + (y-agent.get_from_state("y"))**2
					if d < dist:
						dist = d
						closest_x = agent.get_from_state("x"); closest_y = agent.get_from_state("y")

		if dist != None and sqrt(dist) < 50:
			a_angle = degrees(atan2(closest_y - y, closest_x - x))
			a_dist = sqrt(dist)
		else:
			a_angle = None
			a_dist = None

		return (f_angle, f_dist, f_closest, a_angle, a_dist)