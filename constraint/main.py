# Barry Boyce Jr
# CPSC 447
# Fall 2026
# 11/4/2026
# project4
# main.py

import sys
from parser import parse
from metrics import SAT, NODES_VISITED, BACKTRACKS, AC3_REVISIONS, SOLVE_STATUS, ASSIGNMENT

REQUIRED_ARGS = 5

# Function Name: main
# Description:   checks the command line arguments, runs the chosen search, and
#                writes the assignment and metrics to their files
# Parameters:    none
# Return Value:  none
def main():
    #error if usage incorrect
    if len(sys.argv) < REQUIRED_ARGS:
        print("Usage: python main.py <backtrack-naive|backtrack-mac> <input_file> <output_file> <result_file>",
              file=sys.stderr)
        sys.exit(1)

    #saves cla
    algorithm = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    result_file = sys.argv[4]

#only runs when main.py is run directly, not when imported
if __name__ == "__main__":
    main()