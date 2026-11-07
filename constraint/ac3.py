# Barry Boyce Jr
# CPSC 447
# Fall 2026
# 11/6/2026
# project4
# ac3.py

from collections import deque
from state import VARIABLES, get_neighbors
from metrics import AC3_REVISIONS

# Function Name: make_arcs
# Description:   makes the starting queue for ac-3
# Parameters:    csp - csp dict
# Return Value:  list of (variable, neighbor) arcs
def make_arcs(csp):
    arcs = []
    #goes through every virtual register
    for variable in csp[VARIABLES]:
        #makes an arc to each register it interferes with
        for neighbor in get_neighbors(csp, variable):
            arcs.append((variable, neighbor))
    return arcs

# Function Name: revise_arc
# Description:   deletes every register of a variable that cant work with any
#                register its neighbor has
# Parameters:    domains - dict of each virtual register and the physical registers it can use
#                variable - virtual register whose registers are checked
#                neighbor - virtual register it interferes with
#                metrics - metrics dict
# Return Value:  true if a register was deleted from the variable, otherwise false
def revise_arc(domains, variable, neighbor, metrics):
    #adds one to the ac-3 revision count
    metrics[AC3_REVISIONS] = metrics[AC3_REVISIONS] + 1
    removed = False

    #goes through each register the variable can still use
    for value in list(domains[variable]):
    #interfering registers cant match, so this register is removed only if
    #the neighbor has nothing else left
        if domains[neighbor] == {value}:
            domains[variable].discard(value)
            removed = True
    return removed

# Function Name: ac3
# Description:   keeps removing registers that can't work with any of a neighbors
#                registers until nothing else can be removed
# Parameters:    csp - csp dict
#                domains - dict of each virtual register and the physical registers
#                          it can use
#                metrics - metrics dict that also counts revisions
#                arcs - arcs to start the queue with
# Return Value:  false if a virtual register has no registers left
def ac3(csp, domains, metrics, arcs=None):
    #if no arcs were given, starts with every arc in the csp
    if arcs is None:
        arcs = make_arcs(csp)
    queue = deque(arcs)

    #keeps track of arcs already waiting
    in_queue = set(arcs)

    #keeps going until there are no arcs left to check
    while queue:
        #takes the next arc off the front of the queue
        variable, neighbor = queue.popleft()
        in_queue.discard((variable, neighbor))

        #only does more work if the check removed a register
        if revise_arc(domains, variable, neighbor, metrics):
            if not domains[variable]:
                return False
            #if a variable loses a value, its neighbors need to be rechecked
            for other_neighbor in get_neighbors(csp, variable):
                arc = (other_neighbor, variable)
                if arc not in in_queue:
                    queue.append(arc)
                    in_queue.add(arc)
    return True