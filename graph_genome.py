import sys

from parser import *
from graph import *
from utils import *
from index import *

valid_commands = ['build', 'quit', 'help', 'add-variant', 'dot', 'print', 'add-global-alignment', 'add-global-alignments', 'critical', 'most-probable', 'analyze', 'index', 'map', 'load-test', 'load-hla', 'regions']
valid_flags = ['--fasta', '--vcf', '--lr', '--save', '--load']

def parse_command(args):
	if (len(args) < 0):
		print('Invalid command: ' + str(args))
		return False, [], []

	command = args[0]
	if not command in valid_commands:
		print('Invalid command: ' + str(args))
		return False, [], []
	flags = []
	params = []

	for arg in args[1:]:
		if arg in valid_flags:
			flags.append(arg)
		else:
			params.append(arg)

	return command, flags, params

def handle_build(graph, index, params, flags):
	if graph:
		print('Graph already built')
		confirm = input('Overwrite (y/N): ')
		if confirm != 'y':
			return
	if ('--fasta' in flags):
		if (len(params) == 1):
			try:
				print('Building graph from fasta file ' + params[0])
				graph = parse_reference_genome(params[0])
				print('Graph built')
				return graph
			except FileNotFoundError:
				print(params[0] + ' is not a file')
		else:
			print('"build --fasta <filename>" takes exactly one argument, the filename of a fasta file')
	else:
		print('Not implemented, use "build --fasta <filename>"')

def handle_load_test(graph, index, params, flags):
	graph = parse_reference_genome('data/test.fasta')

	parse_VCF_variants(graph, 'data/test.vcf')

	name, alignment1, alignment2 = parse_global_alignment('data/alignment.txt')
	alignment = generate_graph_from_alignment(alignment2, name, graph)
	graph.insert_global_alignment(alignment1, alignment, name)

	index = generate_left_right_index(graph)

	return graph, index

def handle_load_hla(graph, index, params, flags):
	graph = parse_reference_genome('data/hla_b27/sequences/ref.fasta')

	name, alignment1, alignment2 = parse_global_alignment('data/hla_b27/alignments/ref-02.alignment')
	alignment = generate_graph_from_alignment(alignment2, name, graph)
	graph.insert_global_alignment(alignment1, alignment, name)

	name, alignment1, alignment2 = parse_global_alignment('data/hla_b27/alignments/ref-03.alignment')
	alignment = generate_graph_from_alignment(alignment2, name, graph)
	graph.insert_global_alignment(alignment1, alignment, name)

	name, alignment1, alignment2 = parse_global_alignment('data/hla_b27/alignments/ref-04.alignment')
	alignment = generate_graph_from_alignment(alignment2, name, graph)
	graph.insert_global_alignment(alignment1, alignment, name)

	name, alignment1, alignment2 = parse_global_alignment('data/hla_b27/alignments/ref-06.alignment')
	alignment = generate_graph_from_alignment(alignment2, name, graph)
	graph.insert_global_alignment(alignment1, alignment, name)

	name, alignment1, alignment2 = parse_global_alignment('data/hla_b27/alignments/ref-09.alignment')
	alignment = generate_graph_from_alignment(alignment2, name, graph)
	graph.insert_global_alignment(alignment1, alignment, name)

	return graph, index

def handle_quit(graph, index, params, flags):
	print('Shutting down')
	exit()

def handle_help(graph, index, params, flags):
	print('Available commands:')
	print('help\t\t\t\tPrints help menu')
	print('build [--fasta] <file/sequence>\t\t\tBuilds a graph from a fasta file')
	print('print\t\t\t\tPrints the reference genome the graph is based on')
	print('add-variant [--vcf] <file>\t\t\tAdds VCF from file to graph')
	print('add-global-alignment <file>\t\tAdds a path from an alignment')
	print('add-global-alignments <file1><file2>...\tAdds paths from several alignments')
	print('analyze <index1> <index2>\tFind the distance between two nodes with given indexes')
	print('most-probable\t\t\tPrints the most probable path through the graph')
	print('critical\t\t\t\tPrints critical regions of graph')
	print('dot <file>\t\t\tPrints dot representation to file')
	print('index\t\t\t\t\tCreates a left-right index of the graph usable by map')
	print('map <sequence>\t\t\t\tMaps the given sequence against the graph')
	print('q\t\t\t\t\tQuits the program')

def handle_add_variant(graph, index, params, flags):
	if not graph:
		print('Needs to build a graph first. See "help"')
		return

	if ('--vcf' in flags):
		if (len(params) == 1):
			try:
				print('Reading variants from vcf file ' + params[0])
				parse_VCF_variants(graph, params[0])
				print('Variants added')
				neighbours = graph.get_node_by_index(5).neighbours
				for neighbour in neighbours:
					print(neighbour.paths)
			except FileNotFoundError:
				print(params[0] + ' is not a file')
		else:
			print('"add-variant --vcf <filename>" takes exactly one argument, the filename of the vcf file')
	else:
		print('Not implemented, use "add-variant --vcf <filename>')

def handle_dot(graph, index, params, flags):
	if not graph:
		print('Needs to build a graph first. See "help"')
		return

	if (len(params) == 1 and len(flags) == 0):
		graph.print_DOT_representation(params[0])
	else:
		print('"dot <filename>" takes exactly one argument, the name of the output file')

def handle_print(graph, index, params, flags):
	if not graph:
		print('Needs to build a graph first. See "help"')
		return

	print(graph.get_reference_genome_representation())

def handle_add_global_alignment(graph, index, params, flags):
	if not graph:
		print('Needs to build a graph first. See "help"')
		return

	if (len(params) == 1):
		try:
			name, alignment1, alignment2 = parse_global_alignment(params[0])
		except FileNotFoundError:
			print(params[0] + ' is not a file')
			return

		alignment = generate_graph_from_alignment(alignment2, name, graph)
		graph.insert_global_alignment(alignment1, alignment, name)
	else:
		print('"add-global-alignment" takes exactly on argument, the filename of a fasta file')

def handle_add_multiple_global_alignments(graph, index, params, flags):
	if not graph:
		print('Needs to build a graph first. See "help"')
		return

	if (len(params) > 0):
		for i in range(0, len(params)):
			try:
				name, alignment1, alignment2 = parse_global_alignment(params[i])
			except FileNotFoundError:
				print(params[i] + ' is not a file')
				return

			alignment = generate_graph_from_alignment(alignment2, name, graph)
			graph.insert_global_alignment(alignment1, alignment, name)
	else:
		print('"add-global-alignments" takes atleast one argument, the filename of one or multiple alignment files files')

def handle_critical(graph, index, params, flags):
	if not graph:
		print('Needs to build a graph first. See "help"')
		return

	critical = graph.find_critical_regions()
	regions = []

	i = 0
	while i < len(critical):
		start = critical[i]
		while (i + 1 < len(critical) and critical[i + 1] == critical[i] + 1):
			i += 1
		end = critical[i]
		if start != end:
			regions.append(str(start) + '-' + str(end))
		else:
			regions.append(str(start))
		i += 1

	print('Critical regions: ' + str(regions[:-1]))

def handle_most_probable(graph, index, params, flags):
	if not graph:
		print('Needs to build a graph first. See "help"')
		return

	path, probability = graph.find_most_probable_path()
	print('Probability: ' + str(probability))
	print('Path:')
	print(path_to_str(path))

def handle_analyze(graph, index, params, flags):
	if not graph:
		print('Needs to build a graph first. See "help"')
		return

	if (len(params) == 2):
		index1 = int(params[0])
		index2 = int(params[1])
		dist = graph.find_shortest_distance(index1, index2)
		dist_backward = graph.find_shortest_distance(index2, index1)
		critical1 = graph.is_critical(index1)
		critical2 = graph.is_critical(index2)

		if (dist > dist_backward):
			dist = dist_backward
		if (dist == float('inf')):
			print('Nodes ' + str(index1) + ' and ' + str(index2) + ' is overlapping')
		else:
			print('Nodes ' + str(index1) + ' and ' + str(index2) + ' is not overlapping. Naive distance: ' + str(dist))
			if (critical1 and critical2):
				print('All paths through the graph goes through both nodes')
			elif (critical1):
				print('All paths must go through ' + str(index1) + ' but not ' + str(index2))
			elif (critical2):
				print('All paths must go through ' + str(index2) + ' but not ' + str(index1))
			else:
				print('There exists paths which does not go through either ' + str(index1) + ' or ' + str(index2))
	else:
		print('"analyze <index> <index>" takes exactly two arguments, indexes of vertices in the graph')

def handle_index(graph, index, params, flags):
	if not graph:
		print('Needs to build a graph first. See "help"')
		return

	if ('--lr' in flags):
		if (len(flags) == 1):
			print('Building index')
			index = generate_left_right_index(graph)
			print('Done building index')
			return index
		elif (len(flags) == 2):
			if ('--save' in flags):
				if (len(params) == 1):
					if index:
						write_left_right_index_to_file(index, params[0])
					else:
						print('Needs to build an index before writing, see "index" without parameters')
				else:
					print('"index --save" takes exactly one argument, the filename of the file to write to')
			elif ('--load' in flags):
				print('Load is not implemented yet')
			else:
				print('"index --lr [optional]" only runs with two optional options, --save and --load')
		else:
			print('Maximum one flag is allowed with --lr, such as "index --lr --save"')
	else:
		print('Only left-right indexing currently supported, use "index --lr"')

	return index


def handle_map(graph, index, params, flags):
	if not index:
		print('Needs to build an index first! See "index"')
		return

	if ('--fasta' in flags):
		print('Not implemented yet, use "map <sequence>"')
	elif (len(params) == 1):
		sequence = params[0]
		mappings = index.map_sequence(sequence)
		expanded_mappings = expand_mappings(graph, mappings, sequence)
		for distinct in expanded_mappings:
			print(distinct)
	else:
		print('"map" takes exactly one argument, a sequence to be mapped')

def handle_regions(graph, index, params, flags):
	if not graph:
		print('Needs to build a graph first. See "help"')
		return

	regions = graph.get_regions()
	print(str(regions))


def command_loop():
	cmd = True
	graph = None
	index = None

	while not (cmd == 'quit' or cmd == 'q'):
		cmd, flags, params = parse_command(input('Command ("help" for help):').split(" "))
		if not cmd:
			print('Type "help" for help')
			continue

		if (cmd == 'build'):
			graph = handle_build(graph, index, params, flags)
		elif (cmd == 'load-test'):
			graph, index = handle_load_test(graph, index, params, flags)
		elif (cmd == 'load-hla'):
			graph, index = handle_load_hla(graph, index, params, flags)
		elif (cmd == 'quit'):
			handle_quit(graph, index, params, flags)
		elif not graph:
			print('Execute "build <filename>" first to build a graph')
		elif (cmd == 'help'):
			handle_help(graph, index, params, flags)
		elif (cmd == 'add-variant'):
			handle_add_variant(graph, index, params, flags)
		elif (cmd == 'dot'):
			handle_dot(graph, index, params, flags)
		elif (cmd == 'print'):
			handle_print(graph, index, params, flags)
		elif (cmd == 'add-global-alignment'):
			handle_add_global_alignment(graph, index, params, flags)
		elif (cmd == 'add-global-alignments'):
			handle_add_multiple_global_alignments(graph, index, params, flags)
		elif (cmd == 'critical'):
			handle_critical(graph, index, params, flags)
		elif (cmd == 'most-probable'):
			handle_most_probable(graph, index, params, flags)
		elif (cmd == 'analyze'):
			handle_analyze(graph, index, params, flags)
		elif (cmd == 'index'):
			index = handle_index(graph, index, params, flags)
		elif (cmd == 'map'):
			handle_map(graph, index, params, flags)
		elif (cmd == 'regions'):
			handle_regions(graph, index, params, flags)


if __name__ == '__main__':
	sys.setrecursionlimit(10000)
	command_loop()
