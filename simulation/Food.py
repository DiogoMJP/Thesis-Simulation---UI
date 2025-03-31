class Food(object):
	def __init__(self, width, height, eating_number, first_time_step, life_expectancy):
		self.width = width
		self.height = height
		self.eating_number = eating_number
		self.first_time_step = first_time_step
		self.life_expectancy = life_expectancy
		self.eaten = []
		self.alive = True
		self.x = None
		self.y = None
		self.detection_radius = None
		self.last_time_step = None
		self.history = []


	def simulate(self, time_step):
		if self.alive:
			if time_step - self.first_time_step >= self.life_expectancy or len(self.eaten) >= self.eating_number:
				if len(self.eaten) >= self.eating_number:
					for agent in self.eaten:
						agent.prolong_life_expectancy()
				self.alive = False
				self.last_time_step = time_step
			self.eaten = []


	def to_dict(self):
		return {
			"first_time_step" : self.first_time_step,
			"last_time_step" : self.last_time_step,
			"life_expectancy" : self.life_expectancy,
			"x" : self.x,
			"y" : self.y
		}