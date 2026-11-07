# Barry Boyce Jr
# CPSC 447
# Fall 2026
# 11/06/2026
# project4
# metrics.py

#solve statuses
SAT = "SAT"
UNSAT = "UNSAT"

#metric names
NODES_VISITED = "nodes_visited"
BACKTRACKS = "backtracks"
AC3_REVISIONS = "ac3_revisions"
SOLVE_STATUS = "solve_status"
ASSIGNMENT = "assignment"

# Function Name: make_metrics
# Description:   makes a new metrics dict with all counts starting at 0
# Parameters:    none
# Return Value:  dict of metric name to be counted
def make_metrics():
    return {
        NODES_VISITED: 0,
        BACKTRACKS: 0,
        AC3_REVISIONS: 0,
    }

# Function Name: make_result
# Description:   builds the result of a search from its assignment and metrics
# Parameters:    assignment - dict of each virtual register and the physical register
#                             it was given, or none if the graph cant be solved
#                metrics - metrics dict from the search
# Return Value:  dict with the assignment, solve status, and every metric
def make_result(assignment, metrics):
    if assignment is None:
        status = UNSAT
    else:
        status = SAT
    return {
        NODES_VISITED: metrics[NODES_VISITED],
        BACKTRACKS: metrics[BACKTRACKS],
        AC3_REVISIONS: metrics[AC3_REVISIONS],
        SOLVE_STATUS: status,
        ASSIGNMENT: assignment,
    }


