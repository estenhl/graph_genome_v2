from graph import *

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