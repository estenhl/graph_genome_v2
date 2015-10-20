from graph import *

class LeftRightIndex:
	def __init__(self, left_contexts, right_contexts):
		self.left_contexts = left_contexts
		self.right_contexts = right_contexts

	def map_left_context(self, context):
		return self.map_context(context, self.left_contexts, 0, len(self.left_contexts))
	def map_right_context(self, context):
		return self.map_context(context, self.right_contexts, 0, len(self.right_contexts) - 1)

	def map_context(self, context, contexts, start, end):
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

		return list(set(left_mapping) & set(right_mapping))

	def map_sequence(self, sequence):
		mappings = []
		for i in range(0, len(sequence) - 1):
			mappings.append(self.map_node(sequence[0:i][::-1], sequence[i + 1:]))

		return mappings

def generate_left_right_index(graph):
	left_contexts, right_contexts = graph.generate_left_right_contexts()

	sorted_left = sorted(left_contexts, key=lambda k: k['context']) 
	sorted_right = sorted(right_contexts, key=lambda k: k['context'])
	minimized_left = minimize_context_index(sorted_left)
	minimized_right = minimize_context_index(sorted_right)

	return LeftRightIndex(minimized_left, minimized_right)

def longest_common_substring(s1, s2):
	i = 0
	while (i < len(s1) and i < len(s2)):
		if not (s1[i] == s2[i]):
			return i
		i += 1
	return i

def minimize_context_index(index):
	minimized = []
	operations = 2

	common = longest_common_substring(index[0]['context'], index[1]['context'])
	if (len(index[0]['context']) > common):
		minimized.append({'context': index[0]['context'][:common + 1], 'index': index[0]['index']})

	for i in range(1, len(index) - 1):
		prev_common = longest_common_substring(index[i - 1]['context'], index[i]['context'])
		next_common = longest_common_substring(index[i]['context'], index[i + 1]['context'])
		operations += 1

		
		if (prev_common > next_common):
			minimized.append({'context': index[i]['context'][:prev_common + 1], 'index': index[i]['index']})
		else:
			minimized.append({'context': index[i]['context'][:next_common + 1], 'index': index[i]['index']})

	common = longest_common_substring(index[-1]['context'], index[-2]['context'])
	if (len(index[-1]['context']) > common):
		minimized.append({'context': index[-1]['context'][:common + 1], 'index': index[-1]['index']})
	print('Operations in minimize: ' + str(operations))

	return minimized

			