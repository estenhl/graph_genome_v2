from suffix_tree import *

def suffix_tree_test():
	tree = SuffixTree()
	tree.add_word('AAAA', 1)
	assert 1 == len(tree.lookup('AAAA'))
	assert 0 == tree.lookup('AAAA')[1]
	tree.add_word('AAAT', 2)
	assert 2 == len(tree.lookup('AAAA'))
	assert 1 == tree.lookup('AAAA')[2]
	assert 2 == len(tree.lookup('AAA'))
	assert 0 == tree.lookup('AAA')[1]
	assert 0 == tree.lookup('AAA')[2]
	tree.add_word('AAAC', 3)
	assert 3 == len(tree.lookup('AAAG'))
	assert 1 == tree.lookup('AAAG')[1]
	assert 1 == tree.lookup('AAAG')[2]
	assert 1 == tree.lookup('AAAG')[3]
	assert 0 == tree.lookup('AAAA')[1]
	assert 0 == len(tree.lookup('TTTTTTT'))
	assert 2 == len(tree.lookup('AAAATTT'))
	assert 3 == tree.lookup('AAAATTT')[1]
	assert 3 == len(tree.lookup('AGGG'))
	assert 3 == tree.lookup('AGGG')[1]
	assert 3 == tree.lookup('AGGG')[2]
	assert 3 == tree.lookup('AGGG')[3]
	assert 1 == tree.lookup('ATAAT')[2]

if __name__ == '__main__':
	suffix_tree_test()