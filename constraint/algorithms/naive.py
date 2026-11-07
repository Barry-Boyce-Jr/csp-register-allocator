# Barry Boyce Jr
# CPSC 447
# Fall 2026
# 11/5/2026
# project4
# naive.py

from state import VARIABLES, DOMAINS, sorted_domain, no_conflict
from metrics import make_metrics, make_result, NODES_VISITED, BACKTRACKS

# Function Name: select_unassigned_variable
# Description:   picks the first virtual register that isn't assigned
#                in lexicographic order
# Parameters:    variables - sorted list of virtual registers
#                assignment - dict of each virtual register given a physical
#                             register so far
#                csp - csp dict
# Return Value:  next virtual register to assign
def select_unassigned_variable(variables, assignment, csp):
    for variable in variables:
        if variable not in assignment:
            return variable

# Function Name: order_domain_values
# Description:   orders a virtual registers physical registers in numerical order
# Parameters:    variable - virtual register being assigned
#                assignment - dict of each virtual register given a physical
#                             register so far
#                csp - csp dict
# Return Value:  sorted list of physical registers
def order_domain_values(variable, assignment, csp):
    return sorted_domain(csp, csp[DOMAINS], variable)

# Function Name: recursive_backtracking
# Description:   gives one virtual register a physical register every call and moves
#                on if it works, it backs up if none work
# Parameters:    assignment - dict of each virtual register given a physical
#                             register so far
#                csp - csp dict
#                metrics - metrics dict
# Return Value:  complete assignment, or none if this branch fails
def recursive_backtracking(assignment, csp, metrics):
    #adds to count of nodes visited
    metrics[NODES_VISITED] = metrics[NODES_VISITED] + 1

    #every virtual register has a physical register, so the answer is found
    if len(assignment) == len(csp[VARIABLES]):
        return assignment
    
    #picks the next virtual register to give a physical register to
    variable = select_unassigned_variable(csp[VARIABLES], assignment, csp)

    #tries each physical register it can use
    for value in order_domain_values(variable, assignment, csp):
        if no_conflict(csp, assignment, variable, value):
            assignment[variable] = value
            result = recursive_backtracking(assignment, csp, metrics)
            if result is not None:
                return result
            del assignment[variable]

    #no register works
    metrics[BACKTRACKS] = metrics[BACKTRACKS] + 1
    return None

# Function Name: naive
# Description:   plain backtracking search, goes through virtual registers in
#                lexicographic order and physical registers in numerical order
# Parameters:    csp - csp dict
# Return Value:  dict with nodes_visited, backtracks, ac3_revisions, solve_status,
#                and the assignment
def naive(csp):
    #metrics reset every search
    metrics = make_metrics()
    assignment = recursive_backtracking({}, csp, metrics)
    return make_result(assignment, metrics)