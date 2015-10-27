
class Region:
	def __init__(self, index, start):
		self.index = index
		self.start = start
		self.nodes = {start.index: start}

	def set_end(self, end):
		self.end = end

	def add_node(self, node):
		self.nodes[node.index] = node

	def contains(self, index):
		return index in self.nodes

	def get(self, index):
		return self.nodes[index]

	def __repr__(self):
		return 'Region[' + str(self.index) + ']: ' + str([key for key in sorted(self.nodes)])