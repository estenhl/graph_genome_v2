from parser import *
from graph import *
import sys

def command_loop(graph):
	cmd = True
	while (True):
		cmd = input('Command ("help" for help):').split(" ")
		if (cmd[0] == 'help'):
			print_help()
		elif (cmd[0] == 'add'):
			if (len(cmd) < 2):
				print('add needs an argument')
				continue

			parse_VCF_variants(graph, cmd[1])
		elif (cmd[0] == 'print'):
			if (len(cmd) < 2):
				print('print needs an argument')
				continue

			graph.print_DOT_representation(cmd[1])
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
			break

def print_help():
	print('Available commands:')
	print('help\t\t\t\tPrints help menu')
	print('add <file>\t\t\tAdds VCF variants from file to graph')
	print('print <file>\t\t\tPrints dot representation to file')
	print('analyze <index1> <index2>\tFind the distance between two nodes with given indexes')

if __name__ == '__main__':
	sys.setrecursionlimit(10000)
	graph = parse_reference_genome(sys.argv[1])
	command_loop(graph)
