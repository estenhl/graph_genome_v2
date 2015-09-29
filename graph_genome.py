from parser import *
from graph import *
import sys

def command_loop():
	cmd = True
	graph = None

	while (True):
		cmd = input('Command ("help" for help):').split(" ")
		if (cmd[0] == 'build'):
			if graph:
				print('Graph already built')
				confirm = input('Overwrite (y/n): ')
				if confirm != 'y':
					continue
			if (len(cmd) < 2):
				print('build needs an argument')
				continue

			try:
				graph = parse_reference_genome(cmd[1])
			except FileNotFoundError:
				print(cmd[1] + ' is not a file')
		elif not (cmd[0] == 'q' or cmd[0] == 'quit'):
			if not graph:
				print('Execute ">build <filename>" first to build a graph')
				continue
			elif (cmd[0] == 'help'):
				print_help()
			elif (cmd[0] == 'add-vcf'):
				if (len(cmd) < 2):
					print('add needs an argument')
					continue
				try:
					parse_VCF_variants(graph, cmd[1])
				except FileNotFoundError:
					print(cmd[1] + ' is not a file')
			elif (cmd[0] == 'dot'):
				if (len(cmd) < 2):
					print('dot needs an argument')
					continue

				graph.print_DOT_representation(cmd[1])
			elif (cmd[0] == 'print'):
				print(graph.get_reference_genome_representation())
			elif (cmd[0] == 'add-global-alignment'):
				if (len(cmd) < 2):
					print('add-global-alignment needs an argument')
					continue
				try:
					name, alignment1, alignment2 = parse_global_alignment(cmd[1])
				except FileNotFoundError:
					print(cmd[1] + ' is not a file')
					continue

				alignment = generate_graph_from_alignment(alignment2, name, graph)
				graph.insert_global_alignment(alignment1, alignment, name)
			elif (cmd[0] == 'add-global-alignments'):
				if (len(cmd) < 2):
					print('add-global-alignments needs an argument')
					continue

				for i in range(2, len(cmd)):
					try:
						name, alignment1, alignment2 = parse_global_alignment(cmd[i])
					except FileNotFoundError:
						print(cmd[i] + ' is not a file')
						continue

					alignment = generate_graph_from_alignment(alignment2, name, graph)
					graph.insert_global_alignment(alignment1, alignment, name)

			elif (cmd[0] == 'critical'):
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

			elif (cmd[0] == 'index'):
				critical = graph.find_critical_regions()
				print(critical)
				breakpoints = []

				i = 0
				while (i < len(critical)):
					breakpoints.append(critical[i])
					iterated = False
					while (i + 1 < len(critical) and (critical[i] == critical[i + 1] - 1)):
						i += 1
						iterated = True
					if iterated:
						breakpoints.append(critical[i])
					i += 1

				print(breakpoints)

				for i in range(1, len(breakpoints)):
					regions.append(Region(graph.get_node_by_index(breakpoints[i - 1], graph.get_node_by_index(breakpoints[i]))))



			elif (cmd[0] == 'analyze'):
				if (len(cmd) < 3):
					print('analyze needs two arguments')
					continue

				index1 = int(cmd[1])
				index2 = int(cmd[2])
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
				print(cmd[0] + ' is an invalid command')
		elif (cmd[0] == 'q' or cmd[0] == 'quit'):
				exit()

def print_help():
	print('Available commands:')
	print('help\t\t\t\tPrints help menu')
	print('build <file>\t\t\tBuilds a graph from a fasta file')
	print('print\t\t\t\tPrints the reference genome the graph is based on')
	print('add-vcf <file>\t\t\tAdds VCF variants from file to graph')
	print('add-alignment <file>\t\tAdds a path from an alignment')
	print('analyze <index1> <index2>\tFind the distance between two nodes with given indexes')
	print('critical\t\t\t\tPrints critical regions of graph')
	print('dot <file>\t\t\tPrints dot representation to file')

if __name__ == '__main__':
	sys.setrecursionlimit(10000)
	command_loop()
