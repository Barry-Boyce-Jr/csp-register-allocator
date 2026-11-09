# Barry Boyce Jr
# CPSC 447
# Fall 2026
# 11/4/2026
# project4
# main.py

import sys
from parser import parse
from metrics import SAT, NODES_VISITED, BACKTRACKS, AC3_REVISIONS, SOLVE_STATUS, ASSIGNMENT
from state import budget_filter
from algorithms.naive import naive
from algorithms.mac import mac

REQUIRED_ARGS = 5

# Function Name: main
# Description:   checks the command line arguments, runs the chosen search, and
#                writes the assignment and metrics to their files
# Parameters:    none
# Return Value:  none
def main():
    #error if usage incorrect
    if len(sys.argv) < REQUIRED_ARGS:
        print("Usage: python main.py <backtrack-naive|backtrack-mac> <input_file> <output_file> <result_file> [budget]",
              file=sys.stderr)
        sys.exit(1)

    #saves cla
    algorithm = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    result_file = sys.argv[4]

    #error for algorithm cla
    if algorithm != "backtrack-naive" and algorithm != "backtrack-mac":
        print("algorithm must be 'backtrack-naive' or 'backtrack-mac'", file=sys.stderr)
        sys.exit(1)   

    #saves optional budget cla
    budget = None
    if len(sys.argv) > REQUIRED_ARGS:
        #error if the budget isn't a number
        if not sys.argv[REQUIRED_ARGS].isdigit():
            print("budget must be a number of registers", file=sys.stderr)
            sys.exit(1)
        budget = int(sys.argv[REQUIRED_ARGS])

    #builds the csp from the input file
    csp = parse(input_file)

    #filters registers to budget if budget is given
    if budget is not None:
        csp = budget_filter(csp, budget)

    #all searches
    if algorithm == "backtrack-naive":
        result = naive(csp)
    elif algorithm == "backtrack-mac":
        result = mac(csp)

    #writes assignment to output file
    with open(output_file, "w") as file:
        if result[SOLVE_STATUS] == SAT:
            assignment = result[ASSIGNMENT]
            for variable in sorted(assignment):
                file.write(f"{variable} {assignment[variable]}\n")

    #writes metrics to result file
    with open(result_file, "w") as file:
        file.write(f"{algorithm},{result[NODES_VISITED]},{result[BACKTRACKS]},"
                   f"{result[AC3_REVISIONS]},{result[SOLVE_STATUS]}\n")

#only runs when main.py is run directly, not when imported
if __name__ == "__main__":
    main()