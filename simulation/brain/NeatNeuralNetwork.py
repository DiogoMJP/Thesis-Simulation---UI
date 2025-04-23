from scipy.special import expit as sigmoid
from neat.nn import FeedForwardNetwork


class NeatNeuralNetwork(object):
	def __init__(self, inputs, outputs, node_evals):
		self.inputs = inputs
		self.outputs = outputs
		self.node_evals = [(n, b, r, l) for n, _, _, b, r, l in node_evals]
		self.values = dict((key, 0.0) for key in inputs + outputs)
	

	def sum(self, lst):
		return sum(lst)

	def sigmoid(self, x):
		return sigmoid(x)

	def activate(self, inputs):
		if len(self.inputs) != len(inputs):
			raise RuntimeError("Expected {0:n} inputs, got {1:n}".format(len(self.inputs), len(inputs)))

		for k, v in zip(self.inputs, inputs):
			self.values[k] = v

		for node, bias, response, links in self.node_evals:
			node_inputs = []
			for i, w in links:
				node_inputs.append(self.values[i] * w)
			s = self.sum(node_inputs)
			self.values[node] = self.sigmoid(bias + response * s)

		return [self.values[i] for i in self.outputs]

	
	def to_dict(self):
		return {
			"type"			: "neat-neural-network",
			"inputs"		: self.inputs,
			"outputs"		: self.outputs,
			"node-evals"	: self.node_evals
		}

	@staticmethod
	def create_from_neat_nn(nn : FeedForwardNetwork):
		return NeatNeuralNetwork(nn.input_nodes, nn.output_nodes, nn.node_evals)
	
	@staticmethod
	def load_from_data(data):
		return NeatNeuralNetwork(data["inputs"], data["outputs"], data["node-evals"])