# Barry Boyce Jr
# CPSC 447
# Fall 2026
# 11/4/2026
# project4
# state.py

#keys for the csp dict
PHYSICAL_REGISTERS = "physical_registers"
VARIABLES = "variables"
DOMAINS = "domains"
NEIGHBORS = "neighbors"

# Function Name: sort_registers
# Description:   sorts the physical registers in numerical order
# Parameters:    physical_registers - list of physical register names
# Return Value:  sorted list of physical registers
def sort_registers(physical_registers):
    #pairs each register with its name length, since the length of the name shows how many digits its number has
    length_pairs = []
    for register in physical_registers:
        length_pairs.append((len(register), register))
    #sorts by length first then by name, so R2 comes before R10
    length_pairs.sort()

    #takes the registers out of the pairs and into an ordered list
    ordered = []
    for length, register in length_pairs:
        ordered.append(register)
    return ordered

# Function Name: sort_neighbors
# Description:   turns each variables neighbors into a sorted list
# Parameters:    neighbors - dict of variable to set of interfering variables
# Return Value:  dict of variable to sorted list of neighbors
def sort_neighbors(neighbors):
    sorted_neighbors = {}
    for variable in neighbors:
        neighbor_list = []
        for neighbor in neighbors[variable]:
            neighbor_list.append(neighbor)
        neighbor_list.sort()
        sorted_neighbors[variable] = neighbor_list
    return sorted_neighbors

# Function Name: make_csp
# Description:   builds the csp
# Parameters:    physical_registers - list of physical register names
#                domains - dict of each virtual and physical registers it can use
#                neighbors - dict of virtual registers and virtual registers it conflicts with
# Return Value:  csp dict (physical registers, variables, domains, neighbors)
def make_csp(physical_registers, domains, neighbors):
    return {
        PHYSICAL_REGISTERS: sort_registers(physical_registers),
        VARIABLES: sorted(domains),
        DOMAINS: domains,
        NEIGHBORS: sort_neighbors(neighbors),
    }

# Function Name: get_neighbors
# Description:   gets the virtual registers that interfere with a virtual register
# Parameters:    csp - csp dict
#                variable - virtual register id
# Return Value:  sorted list of neighbors
def get_neighbors(csp, variable):
    return csp[NEIGHBORS][variable]

# Function Name: sorted_domain
# Description:   gets a variables registers in numerical order
# Parameters:    csp - csp dict
#                domains - dict of each virtual and physical registers it can use
#                variable - virtual register id
# Return Value:  sorted list of the variables registers
def sorted_domain(csp, domains, variable):
    ordered = []
    for register in csp[PHYSICAL_REGISTERS]:
        if register in domains[variable]:
            ordered.append(register)
    return ordered

# Function Name: no_conflict
# Description:   checks that none of a virtual register's neighbors already
#                have the physical register being tried
# Parameters:    csp - csp dict
#                assignment - dict of each virtual register given a physical
#                             register so far
#                variable - variable being assigned
#                value - register being tried
# Return Value:  true if no neighbor has the register, otherwise false
def no_conflict(csp, assignment, variable, value):
    for neighbor in get_neighbors(csp, variable):
        #interfering variables can't share a register
        if neighbor in assignment and assignment[neighbor] == value:
            return False
    #every neighbor was checked and none had the register
    return True

# Function Name: copy_domains
# Description:   copies every domain
# Parameters:    domains - dict of each virtual register and the physical
#                          registers it can still use
# Return Value:  new dict with a new set for each virtual register
def copy_domains(domains):
    copy = {}
    for variable in domains:
        #copies each register into a new set 
        registers = set()
        for register in domains[variable]:
            registers.add(register)
        copy[variable] = registers
    return copy

# Function Name: budget_filter
# Description:   cuts the physical registers down in order to test with register budgets
# Parameters:    csp - csp dict
#                budget - number of registers
# Return Value:  the csp with the smaller registers and domains
def budget_filter(csp, budget):
    #registers are already sorted R0, R1, R2, ... so the first K are the budget
    budget_registers = []
    for register in csp[PHYSICAL_REGISTERS]:
        if len(budget_registers) < budget:
            budget_registers.append(register)
    csp[PHYSICAL_REGISTERS] = budget_registers
    #each virtual register only keeps the registers that are in the budget
    for variable in csp[VARIABLES]:
        allowed = set()
        for register in csp[DOMAINS][variable]:
            if register in budget_registers:
                allowed.add(register)
        csp[DOMAINS][variable] = allowed
    return csp