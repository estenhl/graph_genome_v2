A graph-based reference genome

## Commands
- build <filename>
  Builds a graph from a single reference genome. Has to be run first. See data/test.fasta for format
- add-vcf <filename>
  Adds variants from a vcf-file. See data/test.vcf for format
- add-global-alignment
  Adds a new path from a global alignment, see data/alignment.txt for format
- dot <filename>
  Prints the graph to a file compatible in the dot-format to be opened with dotty or similar
- print
  Prints the single reference sequence used to build the graph to console
- critical
  Prints a summary of all critical nodes in the graph, i.e. nodes traversed by all paths, to console
- analyze <1> <2>
  Prints some information about nodes 1 and 2 (denoted by index) and the relation between them