class Region:
	def __init__(self, head, tail, linear):
		self.ready = False
		self.head = head
		self.tail = tail
		self.linear = linear
		self.shortest = float('inf')
		self.longest = float('inf')
		self.find_distance(head, 0)

	def find_distance(self, curr, dist):
		if (curr == self.tail):
			if (dist < self.shortest):
				self.shortest = dist
			if (dist > self.longest):
				self.longest = dist
			return

		for neighbour in curr.get_neighbours():
			find_distance(self, neighbour, dist + 1)

	
