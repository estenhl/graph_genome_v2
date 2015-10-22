from graph import *
from suffix_tree import *
from params import *

class LeftRightIndex:
	def __init__(self):
		self.left_contexts = []
		self.right_contexts = []
		self.left_suffix_tree = SuffixTree()
		self.right_suffix_tree = SuffixTree()

	def map_left_context(self, context):
		return self.left_suffix_tree.lookup(context)
	def map_right_context(self, context):
		return self.right_suffix_tree.lookup(context)

	## Deprecated?
	def map_context_from_list(self, context, contexts, start, end):
		curr = int(start + (end - start) / 2)
		if (abs(start - end) <= 1):
			if (start != end and longest_common_substring(context, contexts[start]['context']) < longest_common_substring(context, contexts[end]['context'])):
				start = end
			common = longest_common_substring(context, contexts[start]['context'])
			indexes = []

			i = start
			while (i >= 0 and longest_common_substring(context, contexts[i]['context']) == common):
				indexes.append(contexts[i]['index'])
				i -= 1

			i = start + 1
			while (i < len(contexts) and longest_common_substring(context, contexts[i]['context']) == common):
				indexes.append(contexts[i]['index'])
				i += 1

			return indexes
		elif (context > contexts[curr]['context']):
			return self.map_context(context, contexts, curr, end)
		else:
			return self.map_context(context, contexts, start, curr)

	def map_node(self, left_context, right_context):
		left_mapping = self.map_left_context(left_context)
		right_mapping = self.map_right_context(right_context)

		for (index, score) in left_mapping.items():
			if index in right_mapping:
				right_mapping[index] = right_mapping[index] + score
			else:
				right_mapping[index] = score
		mappings = sorted(right_mapping.items(), key=lambda k: k[1], reverse=True)

		equal = 0
		i = 1
		while (i < len(mappings) and mappings[i - 1][1] - mappings[i][1] < CONTEXT_MAPPING_SCORE_THRESHOLD):
			i += 1

		return mappings[:i]

	def map_sequence(self, sequence):
		mappings = []
		sequence = END_SYMBOL + sequence + END_SYMBOL
		for i in range(1, len(sequence) - 1):
			mappings.append(self.map_node(sequence[0:i][::-1], sequence[i + 1:]))

		return mappings

def generate_left_right_index(graph):
	left_contexts, right_contexts = graph.generate_left_right_contexts()

	sorted_left = sorted(left_contexts, key=lambda k: k['context']) 
	sorted_right = sorted(right_contexts, key=lambda k: k['context'])
	minimized_left = minimize_context_index(sorted_left)
	minimized_right = minimize_context_index(sorted_right)

	index = LeftRightIndex()
	index.left_contexts = minimized_left
	index.right_contexts = minimized_right
	for pair in minimized_left:
		index.left_suffix_tree.add_word(pair['context'], pair['index'])
	for pair in minimized_right:
		index.right_suffix_tree.add_word(pair['context'], pair['index'])

	return index

def longest_common_substring(s1, s2):
	i = 0
	while (i < len(s1) and i < len(s2)):
		if not (s1[i] == s2[i]):
			return i
		i += 1
	return i

def minimize_context_index(index):
	minimized = []

	common = longest_common_substring(index[0]['context'], index[1]['context'])
	if (len(index[0]['context']) > common):
		minimized.append({'context': index[0]['context'][:common + 1], 'index': index[0]['index']})

	for i in range(1, len(index) - 1):
		prev_common = longest_common_substring(index[i - 1]['context'], index[i]['context'])
		next_common = longest_common_substring(index[i]['context'], index[i + 1]['context'])

		if (prev_common > next_common):
			minimized.append({'context': index[i]['context'][:prev_common + 1], 'index': index[i]['index']})
		else:
			minimized.append({'context': index[i]['context'][:next_common + 1], 'index': index[i]['index']})

	common = longest_common_substring(index[-1]['context'], index[-2]['context'])
	if (len(index[-1]['context']) > common):
		minimized.append({'context': index[-1]['context'][:common + 1], 'index': index[-1]['index']})

	return minimized

			