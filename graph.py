HEAD_VALUE = 'Head'
TAIL_VALUE = 'Tail'
HEAD_INDEX = 0
TAIL_INDEX = -1
REFERENCE_PATH_INDEX = 'REF'

class Graph:
	def __init__(self, id, description, species):
		self.id = id
		self.description = description
		self.species = species
		self.head = Node(HEAD_VALUE, HEAD_INDEX)
		self.tail = Node(TAIL_VALUE, TAIL_INDEX)
		self.current_path = REFERENCE_PATH_INDEX
		self.current_index = 0

	def get_node_by_index(self, index):
		return self.head.recursive_search(index)[0]

	def get_reference_genome_representation(self):
		s = ""
		current = self.head.get_neighbour_by_path(REFERENCE_PATH_INDEX)

		while (current and current.index != TAIL_INDEX):
			s += current.value
			current = current.get_neighbour_by_path(REFERENCE_PATH_INDEX)

		return s

	def add_SNP(self, value, index, path):
		new = Node(value, self.current_index)
		self.current_index += 1
		prev = self.get_node_by_index(index - 1)
		next = prev.get_neighbour_by_path(REFERENCE_PATH_INDEX).get_neighbour_by_path(REFERENCE_PATH_INDEX)

		prev.add_neighbour(new, path)
		new.add_neighbour(next, path)

	def add_deletion(self, length, index, path):
		prev = self.get_node_by_index(index)

		next = prev
		for i in range(0, length):
			next = next.get_neighbour_by_path(REFERENCE_PATH_INDEX)

		prev.add_neighbour(next, path)

	def add_insertion(self, value, index, path):
		prev = self.get_node_by_index(index)
		next = prev.get_neighbour_by_path(REFERENCE_PATH_INDEX)
		self.generate_insertion(prev, next, value, path)

	def add_short_insertion(self, original, value, index, path):
		prev = self.get_node_by_index(index)
		next = prev
		for i in range(1, len(original) + 1):
			next = next.get_neighbour_by_path(REFERENCE_PATH_INDEX)
		self.generate_insertion(prev, next, value, path)

	def generate_insertion(self, prev, next, value, path):
		first = Node(value[1], self.current_index)
		self.current_index += 1
		last = first
		for i in range(2, len(value)):
			new = Node(value[i], self.current_index)
			self.current_index += 1
			last.add_neighbour(new, path)
			last = new

		prev.add_neighbour(first, path)
		last.add_neighbour(next, path)

	def find_shortest_distance(self, start, end):
		source = self.get_node_by_index(start)
		return source.recursive_search(end)[1]

	def print_DOT_representation(self, filename):
		printer = DOTPrinter()
		printer.search(self.head)
		printer.write(filename)

	def is_critical(self, index):
		return self.head.is_critical(index)



class Node:
	def __init__(self, value, index):
		self.value = value
		self.index = index
		self.neighbours = []
		self.incoming = []

	def get_neighbours(self):
		neighbours = []
		for edge in self.neighbours:
			neighbours.append(edge.dest)

		return neighbours

	def get_neighbour_by_path(self, path_index):
		for neighbour in self.neighbours:
			if path_index in neighbour.paths:
				return neighbour.dest

		return False

	def get_neighbour_by_index(self, index):
		if (index < len(self.neighbours)):
			return self.neighbours[index].dest

		return False

	def add_neighbour(self, neighbour, path=REFERENCE_PATH_INDEX):
		edge = Edge(self, neighbour, path)
		self.neighbours.append(edge)
		neighbour.incoming.append(edge)

	def recursive_search(self, index, iterations=0):
		if (index == self.index):
			return self, iterations

		else:
			for neighbour in self.get_neighbours():
				node, length = neighbour.recursive_search(index, iterations + 1)
				if node:
					return node, length

			return False, float('inf')

	def is_critical(self, index):
		if (self.index == index):
			return True
		elif (self.index == TAIL_INDEX):
			return False

		for neighbour in self.get_neighbours():
			if not neighbour.is_critical(index):
				return False

		return True

class Edge:
	def __init__(self, src, dest, path):
		self.src = src
		self.dest = dest
		self.paths = [path]

class DOTPrinter:
	def __init__(self):
		self.vertices = {}
		self.edges = []

	def search(self, head):
		self.vertices = {}
		self.edges = []
		self.vertices[HEAD_INDEX] = HEAD_VALUE

		queue = [head]
		while (len(queue) > 0):
			curr = queue.pop(0)
			neighbours = curr.neighbours
			for neighbour in neighbours:
				if not (neighbour.dest.index in self.vertices.keys()):
					self.vertices[neighbour.dest.index] = str(neighbour.dest.value)
					queue.append(neighbour.dest)
				self.edges.append([curr.index, neighbour.dest.index, str(neighbour.paths)])

	def write(self, filename):
		file = open(filename, 'w')
		file.write('digraph {\n')
		file.write('graph [rankdir=LR, fontname=fixed, splines=true overlap=false]\n\n')

		file.write('\t// Vertices\n')
		for key in self.vertices.keys():
			file.write('\t' + str(key) + ' [label="' + self.vertices[key] + '", xlabel="' + str(key) + '"];\n')

		file.write('\n\t//Edges\n')
		for edge in self.edges:
			file.write('\t' + str(edge[0]) + ' -> ' + str(edge[1]) + ' [label="' + edge[2] +'"];\n')

		file.write('}')
		file.close()

		