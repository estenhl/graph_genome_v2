from constants import *

# TUNABLE PARAMETERS FOR MAPPING PROCEDURE
MAX_ERRORS = 1 # Max errors in fuzzy search
ERROR_MULTIPLIER = 1 # Multiplier for max_errors - actual_errors
LENGTH_MULTIPLIER = 0.5 # Multiplier for length of match
CONTEXT_MAPPING_SCORE_THRESHOLD = 0.5 # Threshold for keepings scores after context mapping
SCORING_MATRIX = {'A': {'A': 4, 'C': 0, 'G': 0, 'T': 0}, 
	'C': {'A': 0, 'C': 4, 'G': 0, 'T': 0}, 
	'G': {'A': 0, 'C': 0, 'G': 4, 'T': 0}, 
	'T': {'A': 0, 'C': 0, 'G': 0, 'T': 4},
	HEAD_VALUE: {'A': 0, 'C': 0, 'G': 0, 'T': 0},
	TAIL_VALUE: {'A': 0, 'C': 0, 'G': 0, 'T': 0}}
SCORING_MULTIPLIER = 0.5 # Multiplier for equal base scores