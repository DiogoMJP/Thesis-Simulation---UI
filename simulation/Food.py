class Food(object):
	def __init__(self, width, height, eating_number, first_time_step, life_expectancy):
		self.width = width
		self.height = height
		self.eating_number = eating_number
		self.first_time_step = first_time_step
		self.life_expectancy = life_expectancy
		self.eaten = []
		self.state = {"x" : None, "y" : None, "alive" : True}
		self.detection_radius = None
		self.last_time_step = None
		self.history = []


	def get_from_state(self, key):
		return self.state[key]
	def get_from_history(self, time_step, key):
		return self.history[time_step - self.first_time_step][key]

	def set_in_state(self, key, value):
		self.state[key] = value
	def set_history(self, history):
		for state in history:
			self.history += [{"x" : state[0], "y": state[1], "alive": state[2]}]
	def save_state(self):
		self.history += [{
			"x" : self.get_from_state("x"),
			"y" : self.get_from_state("y"),
			"alive" : self.get_from_state("alive")
		}]


	def simulate(self, time_step):
		if self.get_from_state("alive"):
			if time_step - self.first_time_step >= self.life_expectancy or len(self.eaten) >= self.eating_number:
				if len(self.eaten) >= self.eating_number:
					for agent in self.eaten:
						agent.prolong_life_expectancy()
				self.set_in_state("alive", False)
				self.last_time_step = time_step
			self.save_state()
			self.eaten = []


	def to_dict(self):
		return {
			"first_time_step" : self.first_time_step,
			"last_time_step" : self.last_time_step,
			"life_expectancy" : self.life_expectancy,
			"history" : [(state["x"], state["y"], state["alive"]) for state in self.history]
		}