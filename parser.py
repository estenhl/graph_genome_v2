from graph import Graph, Node, REFERENCE_PATH_INDEX
import re

def parse_reference_genome(filename):
	lines = open(filename, 'r').readlines()
	header = lines[0];
	id, description, species = parse_FASTA_header(header)
	graph = Graph(id, description, species)
	parse_FASTA_lines(graph, lines[1:])

	return graph

def parse_FASTA_header(header):
	tokens = header.split(" ")
	id = tokens[0][1:]

	description = 'Unknown description'
	species = 'Unknown species'
	description = header[len(id) + 2:].strip()
	try:
		species = description.split('[')[1][:-1]
	except:
		print('Unable to parse entire fasta header')

	return id, description, species

def parse_FASTA_lines(graph, lines):
	curr = graph.head
	index = 1
	for line in lines:
		for character in line:
			if character != '\n':
				next = Node(character, index)
				curr.add_neighbour(Node(character, index))
				index += 1
				curr = curr.get_neighbour_by_index(0)
	curr.add_neighbour(graph.tail, REFERENCE_PATH_INDEX)
	graph.current_index = index

	return graph

def parse_VCF_variants(graph, filename):
	lines = open(filename, 'r').readlines()
	headers, data = split_VCF(lines)
	for line in data:
		parse_VCF_variant(graph, line)

def split_VCF(lines):
	headers = []
	data = []
	for line in lines:
		if (line[0] == "#"):
			headers.append(line)
		else:
			data.append(line)

	return headers, data

def parse_VCF_variant(graph, line):
	if (line[0] == '#'):
		return

	tokens = re.split(r'\s+', line)
	index = int(tokens[1])
	path = tokens[2]
	original = tokens[3]
	variants = tokens[4]

	for variant in variants.split(","):
		handle_variant(graph, original, variant, index, path)

def handle_variant(graph, original, value, index, path):
	print('Handling variant ' + original + ' -> ' + value + ' on index ' + str(index))
	type = get_variant_type(original, value)
	if (type == VARIANT_TYPE_SNP):
		graph.add_SNP(value, index, path)
	elif (type == VARIANT_TYPE_INSERTION):
		graph.add_insertion(value, index, path)
	elif (type == VARIANT_TYPE_DELETION):
		graph.add_deletion(len(original) - len(value), index, path)
	elif (type == VARIANT_TYPE_COMPLEX):
		graph.add_short_insertion(original, value, index, path)
	else:
		print('Not implemented variant handling on the form ' + original + ', ' + value)

VARIANT_TYPE_SNP = 0
VARIANT_TYPE_INVALID = 1
VARIANT_TYPE_DELETION = 2
VARIANT_TYPE_INSERTION = 3
VARIANT_TYPE_COMPLEX = 4
VARIANT_TYPE_OTHER = 5

def get_variant_type(original, value):
	if (len(original) == 1 and len(value) == 1):
		return VARIANT_TYPE_SNP
	elif (len(original) < 1 or len(value) < 1):
		return VARIANT_TYPE_INVALID
	elif (len(original) > len(value)):
		if (original[0:len(value)] == value):
			return VARIANT_TYPE_DELETION
		else:
			return VARIANT_TYPE_COMPLEX
	elif (len(value) > len(original)):
		if (value[0:len(original)] == original):
			return VARIANT_TYPE_INSERTION
		else:
			return VARIANT_TYPE_COMPLEX
	else:
		return VARIANT_TYPE_OTHER

def parse_global_alignment(filename):
	lines = open(filename, 'r').readlines()
	pairs = []

	i = 2
	while (i < len(lines)):
		if (len(lines[i].split()) == 0):
			pairs.append([lines[i - 2].split()[2], None])
			i += 3
		else:
			pairs.append([lines[i - 2].split()[2], lines[i].split()[2]])
			i += 4

	alignment1 = ''
	alignment2 = ''
	start = True
	for pair in pairs:
		print(pair)
		alignment1 += pair[0]
		if not pair[1]:
			for i in range(0, len(pair[0])):
				alignment2 += '-'
		elif len(pair[0]) > len(pair[1]):
			if start:
				for i in range(0, len(pair[0]) - len(pair[1])):
					alignment2 += '-'
				alignment2 += pair[1]
				start = False
			else:
				alignment2 += pair[1]
				for i in range(0, len(pair[0]) - len(pair[1])):
					alignment2 += '-'
		else:
			alignment2 += pair[1]
			start = False

	name = filename
	if (len(name.split('/')) > 1):
		name = name.split('/')[-1]
	return filename, alignment1, alignment2

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
