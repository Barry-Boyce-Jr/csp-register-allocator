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
# Description:   picks the virtual register with the fewest physical registers
#                left. ties go to the most unassigned neighbors 
# Parameters:    variables - sorted list of virtual registers
#                assignment - dict of each virtual register given a physical
#                             register so far
#                csp - csp dict
#                domains - dict of each virtual register and the physical
#                          registers it can still use
# Return Value:  next virtual register to assign
def select_unassigned_variable(variables, assignment, csp, domains):
    best_variable = None
    best_remaining = None
    best_degree = None

    #goes through the virtual registers in lexicographic order
    for variable in variables:
        if variable not in assignment:
            remaining = len(domains[variable])

            # tracks how many neighbors dont have a register
            degree = 0
            for neighbor in get_neighbors(csp, variable):
                if neighbor not in assignment:
                    degree = degree + 1

            #saves the virtual register if it has fewer physical registers
            if (best_variable is None or remaining < best_remaining
                    or (remaining == best_remaining and degree > best_degree)):
                best_variable = variable
                best_remaining = remaining
                best_degree = degree
    return best_variable
            

# Function Name: order_domain_values
# Description:   orders physical registers by how few neighbors would lose that
#                physical register
# Parameters:    variable - virtual register being assigned
#                assignment - dict of each virtual register given a physical
#                             register so far
#                csp - csp dict
#                domains - dict of each virtual register and the physical
#                          registers it can still use
# Return Value:  ordered list of physical registers
def order_domain_values(variable, assignment, csp, domains):
    choices = []
    position = 0
    #goes through the physical registers left in numerical order
    for value in sorted_domain(csp, domains, variable):
        
        count = 0
        for neighbor in get_neighbors(csp, variable):
            if neighbor not in assignment and value in domains[neighbor]:
                count = count + 1

        #saves the count, the numerical position, and the physical register
        choices.append((count, position, value))
        position = position + 1

    #sorts by fewest neighbors losing a register
    choices.sort()

    #takes the physical registers out in order
    ordered = []
    for count, position, value in choices:
        ordered.append(value)
    return ordered

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
    variable = select_unassigned_variable(csp[VARIABLES], assignment, csp, domains)
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