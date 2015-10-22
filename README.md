A graph-based reference genome

## Commands
- build [--fasta] \<filename\>  
  Builds a graph from a single reference genome. Has to be run first. See data/test.fasta for format
- add-variant [--vcf] \<filename\>  
  Adds variants from a vcf-file. See data/test.vcf for format
- add-global-alignment \<filename\>  
  Adds a new path from a global alignment, see data/alignment.txt for format
- add-global-alignments \<filename1\>\<filename2\>...
  Same as above but for several files
- dot \<filename\>  
  Prints the graph to a file compatible in the dot-format to be opened with dotty or similar
- print  
  Prints the single reference sequence used to build the graph to console
- critical  
  Prints a summary of all critical nodes in the graph, i.e. nodes traversed by all paths, to console
- analyze \<1\> \<2\>  
  Prints some information about nodes 1 and 2 (denoted by index) and the relation between them
- most-probable
  Prints the most probable sequence from the path
- index [--lr] [--save/--load]
  Builds an index of the graph. Currently only left-right context based index available. Save/load not fully implemented
- map \<sequence\>
  (NOT FINISHED) Maps a sequence against the graph

## Alignment procedure:
### 1. Build (index, score)-list for each character in input sequence
  Build a suffix-tree for left and right contexts of all nodes in the graph
  Do a fuzzy search against the suffix-tree, returning pairs of possible matches and their score
    Tunable parameters:
    - Maximum errors allowed
    - Scoring ratio for max_errors - actual_erorrs
    - Length of match before max_errors is increased
    - Scoring ratio for length of match
  Update each pair if the character from the sequence matches graph[index]
    Tunable parameters:
    - Scoring ratio for match (can be variant)

  TODO:
  Optimize building of index
  Check for matches in the last step

### 2. Use list of (index, score)-pairs to map against graph
  Possibilities:
    - Maximize probability(path in graph)*score(path through (index, score)-list)
    - Map "locked" regions of the input sequence against critical region of the graph
    - ???

