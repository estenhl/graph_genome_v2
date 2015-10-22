MAX_ERRORS = 3

class SuffixTree:
	def __init__(self):
		self.root = SuffixTreeNode()

	def add_word(self, word, index):
		curr = self.root

		for char in word:
			if (char in curr.children):
				curr = curr.children[char]
			else:
				curr.children[char] = SuffixTreeNode()
				curr = curr.children[char]

		curr.indexes.append(index)

	def lookup(self, word):
		return self.root.recursive_search(word, 0)

	def __str__(self):
		return self.root.pretty_print(0)

class SuffixTreeNode:
	def __init__(self):
		self.indexes = []
		self.children = {}

	def recursive_search(self, s, errors):
		if (errors > MAX_ERRORS):
			return {}
		elif (len(s) == 0):
			matches = {}
			if (len(self.indexes) > 0):
				for index in self.indexes:
					matches[index] = errors

			for child in self.children:
				for (index, score) in self.children[child].recursive_search('', errors).items():
					if not index in matches or score < matches[index]:
						matches[index] = score

			return matches
		else:
			# Continues down the correct path
			matches = {}
			if (s[0] in self.children):
				matches = self.children[s[0]].recursive_search(s[1:], errors)

			for child in self.children:
				if not (child == s[0]):
					# INDEL
					for (index, score) in self.children[child].recursive_search(s[1:], errors + 1).items():
						if not index in matches or score < matches[index]:
							matches[index] = score

					# Gap in indexed sequences
					for (index, score) in self.children[child].recursive_search(s, errors + 1).items():
						if not index in matches or score < matches[index]:
							matches[index] = score

			# Gap in given sequence
			for (index, score) in self.recursive_search(s[1:], errors + 1).items():
				if not index in matches or score < matches[index]:
					matches[index] = score

			return matches

	def pretty_print(self, tabs):
		s = '\n'
		for child in self.children:
			for i in range(0, tabs):
				s += '\t'
			s += child + ': ' + self.children[child].pretty_print(tabs + 1)

		return s


