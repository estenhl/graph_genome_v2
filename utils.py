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

def merge_colours(colours):
	r = 0
	g = 0
	b = 0

	for colour in colours:
		r += (colour & 0xFF0000) >> 16
		g += (colour & 0x00FF00) >> 8
		b += colour & 0x0000FF


	r = int(r / len(colours)) << 16
	g = int(g / len(colours)) << 8
	b = int(b / len(colours))

	return hex(r + g + b)

def scale_mapping(graph, mappings, sequence):
	scaled_mappings = []
	for i in range(0, len(sequence)):
		temp = []
		for (index, score) in mappings[i]:
			node = graph.get_node_by_index(index)
			mapping_score =  SCORING_MATRIX[node.value][sequence[i]]
			temp.append({'ref': node.value, 'seq': sequence[i], 'index': index, 'score': score + mapping_score * SCORING_MULTIPLIER})
		scaled_mappings.append(sorted(temp, key=lambda k: k['score'], reverse=True))

	return scaled_mappings