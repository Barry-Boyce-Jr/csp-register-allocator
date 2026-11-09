# Barry Boyce Jr
# CPSC 447
# Fall 2026
# 11/8/2026
# project4
# benchmark.py

import csv
import subprocess
import sys
import time

#the max seconds one run can take, can be changed, higher time limit increases time for benchmark.py to finish running
TIME_LIMIT = 10

# Function Name: run_test
# Description:   runs one search algorithm on a test graph with a register budget,
#                stopping it once it runs longer than TIME_LIMIT seconds
# Parameters:    algorithm - "backtrack-naive" or "backtrack-mac"
#                test_file - test graph file name
#                budget - number of physical registers K
# Return Value:  algorithm, nodes visited, backtracks, ac3 revisions, solve status,
#                seconds, or "limit" for each if the search was stopped
def run_test(algorithm, test_file, budget):
    start = time.perf_counter()

    #if stopped early from time then return limit
    try:
        run = subprocess.run([sys.executable, "main.py", algorithm, f"testing/{test_file}",
                              "last_output.txt", "last_result.csv", str(budget)],
                             capture_output=True, text=True, timeout=TIME_LIMIT)
    except subprocess.TimeoutExpired:
        return algorithm, "limit", "limit", "limit", "limit", "limit"

    seconds = round(time.perf_counter() - start, 4)

    #if the solver crashed there is no result file
    if run.returncode != 0:
        return algorithm, "failed", "failed", "failed", "failed", seconds

    #reads the metrics main.py wrote to the result file
    with open("last_result.csv", "r") as file:
        metrics = file.read().strip().split(",")
    return metrics[0], metrics[1], metrics[2], metrics[3], metrics[4], seconds

# Function Name: main
# Description:   runs every test graph at every budget with both algorithms and
#                writes the summary and results csv files
# Parameters:    none
# Return Value:  none
def main():
    # all combinations of test files
    # (density, graph count)
    conditions = [("sparse", 4), ("medium", 4), ("dense", 4)]
    budgets = [2, 4, 8]
    algorithms = ["backtrack-naive", "backtrack-mac"]

    # loops through all test files & outputs results
    with open("benchmark_summary.csv", "w", newline="") as summary_file, \
         open("benchmark_results.csv", "w", newline="") as results_file:
        #summary file uses the exact header from the assignment
        summary = csv.writer(summary_file)
        summary.writerow(["algorithm", "nodes_visited", "backtracks", "ac3_revisions", "solve_status"])
        #results file adds which graph and budget each row is for
        results = csv.writer(results_file)
        results.writerow(["algorithm", "nodes_visited", "backtracks", "ac3_revisions", "solve_status",
                          "test_file", "density", "budget", "time_seconds"])

        for density, count in conditions:
            for test_number in range(1, count + 1):
                test_file = f"{density}_{test_number}.txt"
                for budget in budgets:
                    for algorithm in algorithms:
                        agent, nodes_visited, backtracks, revisions, status, seconds = run_test(algorithm, test_file, budget)
                        summary.writerow([agent, nodes_visited, backtracks, revisions, status])
                        results.writerow([agent, nodes_visited, backtracks, revisions, status,
                                          test_file, density, budget, seconds])
                        print(f"{algorithm} K={budget} search for {test_file} complete")     # progress

#only runs when benchmark.py is run directly, not when imported
if __name__ == "__main__":
    main()