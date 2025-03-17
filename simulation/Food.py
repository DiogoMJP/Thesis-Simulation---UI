class Food(object):
	def __init__(self, width, height, first_time_step, life_expectancy):
		self.width = width
		self.height = height
		self.first_time_step = first_time_step
		self.life_expectancy = life_expectancy
		self.eaten = 0
		self.state = {"x" : None, "y" : None, "alive" : True}
		self.detection_radius = None
		self.last_time_step = None
		self.history = []


	def get_width(self):
		return self.width
	def get_height(self):
		return self.height
	def get_first_time_step(self):
		return self.first_time_step
	def get_life_expectancy(self):
		return self.life_expectancy
	def get_eaten(self):
		return self.eaten
	def get_from_state(self, key):
		return self.state[key]
	def get_from_history(self, time_step, key):
		return self.history[time_step - self.get_first_time_step()][key]
	def get_detection_radius(self):
		return self.detection_radius
	def get_last_time_step(self):
		return self.last_time_step
	def get_history(self):
		return self.history

	def set_width(self, width):
		self.width = width
	def set_height(self, height):
		self.height = height
	def set_eaten(self, eaten):
		self.eaten = eaten
	def set_in_state(self, key, value):
		self.state[key] = value
	def set_detection_radius(self, detection_radius):
		self.detection_radius = detection_radius
	def set_last_time_step(self, last_time_step):
		self.last_time_step = last_time_step
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
			if (time_step - self.get_first_time_step() >= self.get_life_expectancy() or self.get_eaten() >= 3):
				self.set_in_state("alive", False)
				self.set_last_time_step(time_step)
			self.save_state()
			self.set_eaten(0)


	def to_dict(self):
		return {
			"first_time_step" : self.get_first_time_step(),
			"last_time_step" : self.get_last_time_step(),
			"life_expectancy" : self.get_life_expectancy(),
			"history" : [(state["x"], state["y"], state["alive"]) for state in self.get_history()]
		}