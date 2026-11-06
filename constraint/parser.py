# Barry Boyce Jr
# CPSC 447
# Fall 2026
# 11/4/2026
# project4
# parser.py

from state import make_csp

#header names 
PHYSICAL_HEADER = "PHYSICAL_REGISTERS"
VIRTUAL_HEADER = "VIRTUAL_REGISTERS"
INTERFERENCE_HEADER = "INTERFERENCES"

#first value on a line
FIRST = 0

# Function Name: parse
# Description:   Reads the input file line by line, and sorts each line into the
#                physical registers, a virtual registers domain or an
#                interference 
# Parameters:    file_path - path to the input file
# Return Value:  csp dict:
#                physical_registers - sorted list of physical registers,
#                variables - sorted list of virtual registers,
#                domains - physical registers each virtual register can use,
#                neighbors - sorted list of virtual registers each one interferes with
def parse(file_path):
    physical_registers = []
    domains = {}
    neighbors = {}
    section = None

    with open(file_path, "r") as file:
        for line in file:
            line_data = line.split()

            #skips blank lines
            if not line_data:
                continue

            #removes the section header
            if line_data[FIRST] == PHYSICAL_HEADER:
                section = line_data.pop(FIRST)
                physical_registers = line_data
            #the other section headers have data under them, not on the same
            elif line_data[FIRST] == VIRTUAL_HEADER or line_data[FIRST] == INTERFERENCE_HEADER:
                section = line_data[FIRST]

            #pops and save virtual register
            elif section == VIRTUAL_HEADER:
                variable = line_data.pop(FIRST)
                #saves physical registers that the virtual register can use
                allowed = set()
                for register in line_data:
                    if register in physical_registers:
                        allowed.add(register)
                domains[variable] = allowed

                neighbors[variable] = set()

            #saves two virtual registers that have interference
            elif section == INTERFERENCE_HEADER:
                first = line_data.pop(FIRST)
                second = line_data.pop(FIRST)

                #error if the line uses a virtual register that was never listed
                if first not in domains or second not in domains:
                    raise ValueError(f"virtual register for interference {first} {second} is not found")
                #checks to make sure interference is not between same variables
                if first == second:
                    continue

                #saves that these two registers interfere with each other
                neighbors[first].add(second)
                neighbors[second].add(first)

    #builds csp
    return make_csp(physical_registers, domains, neighbors)