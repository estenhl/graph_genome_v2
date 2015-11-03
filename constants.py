LEGAL_CHARACTERS = ['A', 'C', 'T', 'G']

# Graph constants
HEAD_VALUE = 'Head'
TAIL_VALUE = 'Tail'
HEAD_INDEX = 0
TAIL_INDEX = float('inf')
REFERENCE_PATH_INDEX = 'REF'

# Mapping constants
INDEL = '-'
END_SYMBOL = '$'
MAX_SUFFIX_LENGTH = 10

# TUNABLE PARAMETERS FOR MAPPING PROCEDURE
MAX_ERRORS = 3 # Max errors in fuzzy search
ERROR_MULTIPLIER = 1 # Multiplier for max_errors - actual_errors
LENGTH_MULTIPLIER = 0.5 # Multiplier for length of match
CONTEXT_MAPPING_SCORE_THRESHOLD = 1.5 # Threshold for keepings scores after context mapping
SCORING_MATRIX = {'A': {'A': 4, 'C': 0, 'G': 0, 'T': 0}, 
	'C': {'A': 0, 'C': 4, 'G': 0, 'T': 0}, 
	'G': {'A': 0, 'C': 0, 'G': 4, 'T': 0}, 
	'T': {'A': 0, 'C': 0, 'G': 0, 'T': 4},
	HEAD_VALUE: {'A': 0, 'C': 0, 'G': 0, 'T': 0},
	TAIL_VALUE: {'A': 0, 'C': 0, 'G': 0, 'T': 0}}
CORRECT_BASE_SCORE = 1