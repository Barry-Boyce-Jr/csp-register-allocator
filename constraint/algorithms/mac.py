# Barry Boyce Jr
# CPSC 447
# Fall 2026
# 11/5/2026
# project4
# mac.py

from state import VARIABLES, DOMAINS, get_neighbors, sorted_domain, no_conflict
from ac3 import ac3
from metrics import make_metrics, make_result, NODES_VISITED, BACKTRACKS

# Function Name: select_unassigned_variable
# Description:   picks the first virtual register that isnt assigned
#                in lexicographic order
# Parameters:    variables - sorted list of virtual registers
#                assignment - dict of each virtual register given a physical
#                             register so far
#                csp - csp dict
# Return Value:  next virtual register to assign
def select_unassigned_variable(variables, assignment, csp):
    #goes through the virtual registers in lexicographic order
    for variable in variables:
        if variable not in assignment:
            return variable

# Function Name: order_domain_values
# Description:   gets the physical registers a virtual register still has left
#                in numerical order
# Parameters:    variable - virtual register being assigned
#                assignment - dict of each virtual register given a physical
#                             register so far
#                csp - csp dict
#                domains - dict of each virtual register and the physical
#                          registers it can still use
# Return Value:  sorted list of physical registers
def order_domain_values(variable, assignment, csp, domains):
    return sorted_domain(csp, domains, variable)

# Function Name: recursive_backtracking
# Description:   assigns one virtual register per call, runs ac-3, and puts
#                back removed registers at a dead end
# Parameters:    assignment - dict of each virtual register given a physical
#                             register so far
#                csp - csp dict
#                metrics - metrics dict
#                domains - dict of each virtual register and the physical
#                          registers it can still use
# Return Value:  complete assignment
def recursive_backtracking(assignment, csp, metrics, domains):
    #keeps count
    metrics[NODES_VISITED] = metrics[NODES_VISITED] + 1

    if len(assignment) == len(csp[VARIABLES]):
        return assignment
    
    #picks the next virtual register and tries each register it has left
    variable = select_unassigned_variable(csp[VARIABLES], assignment, csp)
    for value in order_domain_values(variable, assignment, csp, domains):
        if no_conflict(csp, assignment, variable, value):
            assignment[variable] = value

            removed_list = []
            for other in list(domains[variable]):
                if other != value:
                    domains[variable].discard(other)
                    removed_list.append((variable, other))

            #runs ac-3 on neighbors without a register yet
            arcs = []
            for neighbor in get_neighbors(csp, variable):
                if neighbor not in assignment:
                    arcs.append((neighbor, variable))
            if ac3(csp, domains, metrics, arcs, removed_list):
                result = recursive_backtracking(assignment, csp, metrics, domains)
                if result is not None:
                    return result
            #adds previously removed registers back if dead end
            for removed_variable, removed_value in removed_list:
                domains[removed_variable].add(removed_value)
            assignment.pop(variable)
    #all registers failed 
    metrics[BACKTRACKS] = metrics[BACKTRACKS] + 1
    return None

# Function Name: mac
# Description:   backtracking search that runs ac-3 before starting and again
#                after every assignment
# Parameters:    csp - csp dict
# Return Value:  dict with nodes_visited, backtracks, ac3_revisions, solve_status,
#                and the assignment
def mac(csp):
    #resets metrics every search
    metrics = make_metrics()

     #copies the domains 
    domains = {}
    for variable in csp[DOMAINS]:
        domains[variable] = set(csp[DOMAINS][variable])

    #runs ac-3 on every arc and searches if nothing runs out of registers
    if ac3(csp, domains, metrics):
        assignment = recursive_backtracking({}, csp, metrics, domains)
    else:
        assignment = None
    return make_result(assignment, metrics)