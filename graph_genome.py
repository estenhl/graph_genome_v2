from parser import *
from graph import *
from utils import *
import sys

valid_commands = ['build', 'quit', 'dot', 'print', 'add-global-alignment', 'add-global-alignments', 'help', 'add-vcf', 'critical', 'analyze', 'most-probable']
valid_flags = ['--fasta']

def parse_command(args):
	if (len(args) < 0):
		print('Invalid command: ' + args)
		return False, [], []

	command = args[0]
	if not command in valid_commands:
		print('Invalid command: ' + args)
		return False, [], []
	flags = []
	params = []

	for arg in args[1:]:
		if arg in valid_flags:
			flags.append(arg)
		else:
			params.append(arg)

	return command, flags, params

def command_loop():
	cmd = True
	graph = None

	while (True):
		cmd, flags, params = parse_command(input('Command ("help" for help):').split(" "))
		print(cmd)
		print(flags)
		print(params)
		if not cmd:
			print('Type "help" for help')
			continue

		if (cmd == 'build'):
			if graph:
				print('Graph already built')
				confirm = input('Overwrite (y/N): ')
				if confirm != 'y':
					continue
			if (len(params) == 1):
				if '--fasta' in flags:
					try:
						graph = parse_reference_genome(params[0])
					except FileNotFoundError:
						print(params[0] + ' is not a file')
				else:
					print('Not implented yet')
			else:
				print('build takes exactly on argument and an optional flag --fasta')
				continue

		elif (cmd == 'quit'):
			print('Shutting down')
			exit()
		elif not graph:
			print('Execute ">build <filename>" first to build a graph')
			continue
		elif (cmd == 'help'):
			print_help()
		elif (cmd == 'add-vcf'):
			if (len(params) == 1 and len(flags) == 0):
				try:
					parse_VCF_variants(graph, params[0])
				except FileNotFoundError:
					print(params[0] + ' is not a file')
			else:
				print('add-vcf takes exactly one argument, a filename of a vcf file')
		elif (cmd == 'dot'):
			if (len(params) == 1 and len(flags) == 0):
				graph.print_DOT_representation(params[0])
			else:
				print('dot takes exactly one argument, the name of the output file')
		elif (cmd == 'print'):
			if (len(params) == 0 and len(flags) == 0):
				print(graph.get_reference_genome_representation())
			else:
				print('print takes no arguments')
		elif (cmd == 'add-global-alignment'):
				if (len(params) == 1):
					try:
						name, alignment1, alignment2 = parse_global_alignment(params[0])
					except FileNotFoundError:
						print(params[0] + ' is not a file')
						continue

					alignment = generate_graph_from_alignment(alignment2, name, graph)
					graph.insert_global_alignment(alignment1, alignment, name)
				else:
					print('build takes exactly on argument and an optional flag --fasta')
					continue
				

				alignment = generate_graph_from_alignment(alignment2, name, graph)
				graph.insert_global_alignment(alignment1, alignment, name)
		elif (cmd == 'add-global-alignments'):
			if (len(params) == 0):
				print('add-global-alignments takes atleast one argument and optional flag --fasta')
			else:
				if ('--fasta' in flags):
					for i in range(0, len(params)):
						try:
							name, alignment1, alignment2 = parse_global_alignment(params[i])
						except FileNotFoundError:
							print(params[i] + ' is not a file')
							continue

						alignment = generate_graph_from_alignment(alignment2, name, graph)
						graph.insert_global_alignment(alignment1, alignment, name)

		elif (cmd == 'critical'):
			if (len(params) == 0 and len(flags) == 0):
				critical = graph.find_critical_regions()
				print('sorted: ' + str(critical))
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
			else:
				print('critical takes no arguments or flags')

		elif (cmd == 'most-probable'):
			if (len(params) == 0 and len(flags) == 0):
				path, probability = graph.find_most_probable_path()
				print('Probability: ' + str(probability))
				print('Path:')
				print(path_to_str(path))
			else:
				print('most-probable takes no arguments or flags')

		elif (cmd == 'analyze'):
			if (len(params) != 2):
				print('analyze takes exactly two arguments')
				continue

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

def print_help():
	print('Available commands:')
	print('help\t\t\t\tPrints help menu')
	print('build <file>\t\t\tBuilds a graph from a fasta file')
	print('print\t\t\t\tPrints the reference genome the graph is based on')
	print('add-vcf <file>\t\t\tAdds VCF variants from file to graph')
	print('add-global-alignment <file>\t\tAdds a path from an alignment')
	print('add-global-alignments <file1><file2>...\tAdds paths from several alignments')
	print('analyze <index1> <index2>\tFind the distance between two nodes with given indexes')
	print('most-probable\t\t\tPrints the most probable path through the graph')
	print('critical\t\t\t\tPrints critical regions of graph')
	print('dot <file>\t\t\tPrints dot representation to file')
	print('q\t\t\t\t\tQuits the program')

if __name__ == '__main__':
	sys.setrecursionlimit(10000)
	command_loop()
