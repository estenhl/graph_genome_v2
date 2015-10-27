from graph import *
from params import *

def path_to_str(path):
	s = ""
	for node in path:
		s += node.value

	return s

def generate_graph_from_alignment(alignment, name, graph):
	path = []

	prev = None
	for i in range(0, len(alignment)):
		if (alignment[i] == '-'):
			path.append(None)
		else:
			curr = Node(alignment[i], graph.current_index)
			graph.current_index += 1
			if (prev):
				prev.add_neighbour(curr, name)
			prev = curr
			path.append(prev)

	return path

def find_critical(graph, mappings, sequence):
	detailed_mappings = []
	for i in range(0, len(mappings)):
		detailed_mappings.append([])
		for mapping in mappings[i]:
			score = mapping[1]
			index = mapping[0]
			if (graph.get_node_by_index(index).value == sequence[i]):
				score = score + CORRECT_MAPPING_SCORE
			critical = False
			if (graph.is_critical(index)):
				critical = True
			detailed_mappings[i].append({'index': index, 'score': score, 'critical': critical})

	return detailed_mappings

def find_distinct(mappings):
	print(str(mappings))
	distinct_mappings = []
	for i in range(0, len(mappings)):
		if (len(mappings[i]) == 1 and mappings[i][0]['critical']):
			distinct_mappings.append(mappings[i][0])
		else:
			distinct_mappings.append(None)

	return distinct_mappings


