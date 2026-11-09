Barry Boyce Jr\
CPSC 447\
Fall 2026\
Project 4\
11/8/2026\
purpose: gives instructions how to run code, gives credit, and explains designs choices and results

## REQUIREMENTS
Python 3

## HOW TO RUN
1. navigate to constraint directory `constraint`
2. enter CLA `python main.py <backtrack-naive|backtrack-mac> <input_file> <output_file> <result_file> [budget]`
    - (only 4 args are required, budget is optional. budget must be 0 or higher if entered)
    - (this can be recreated with any file from testing dir, for example `python main.py backtrack-mac testing/sample.txt output.txt result.csv`)
    - (output_file shows which physical register each virtual register got, it's empty if there's no answer)
    - (the metrics row algorithm,nodes_visited,backtracks,ac3_revisions,solve_status is written to result_file)
    - (on Linux/Mac use `python3`)
3. enter CLA `python benchmark.py`
    - (benchmark_summary.csv and benchmark_results.csv will be recreated each run, located in constraint dir)
    - (this runs backtrack-naive and backtrack-mac with budgets 2, 4, and 8 against all 12 test graphs in testing)
    - (main.py is run as a subprocess and the result file it writes is read and written to benchmark_summary.csv, which starts with the header from the assignment, and to benchmark_results.csv along with the test file, density, budget, and time in seconds)
    - (any run that takes longer than TIME_LIMIT = 10 seconds is stopped and recorded as limit, this can be changed by changing the value of TIME_LIMIT in benchmark.py. This will result in longer times)

## CREDIT
Chapter 5 Lecture notes used as guide for the CSP formulation (state.py, parser.py), backtracking search (naive.py, mac.py), the MRV, degree, and LCV heuristics (mac.py), arc consistency and AC-3 (ac3.py, mac.py)

AIMA algorithms textbook (shown in class) used to check MAC and putting removed registers back when backing up (mac.py, ac3.py)

project 3 used as the starting structure for main.py, parser.py, state.py, benchmark.py, and the algorithms folder

sample.txt in testing is the example input file from the assignment (testing/sample.txt)

Claude AI assisted with reviewing code against the assignment, rubric, and lecture notes, drafting design options for mac.py, the undo list, the register budget, and with README table layouts/ theoretical concepts as well as assistance with wording of comments and readme file.

Claude AI assisted in drafting the heuristics in mac.py and benchmark.py.

Claude AI fully wrote the benchmark test graphs found in `constraint\testing` (sparse, medium, and dense 1-4).

## CSP FORMULATION & HEURISTIC DESIGN
Formally the CSP is X = {v0, v1, ...} (the virtual registers), D(v) = the physical registers listed for v, and C = {v_i ≠ v_j for every interference (v_i, v_j)}. Each virtual register is a variable, the physical registers it's allowed to use are its domain (only the ones also listed on the PHYSICAL_REGISTERS line), and every interference is a rule that the two virtual registers can't use the same physical register (v_i ≠ v_j). This means the constraint graph is the same as the interference graph. If every virtual register can be given a physical register without breaking any of these rules the graph is SAT, and if not it's UNSAT. For the benchmark, the budget K means only R0 up to R(K-1) can be used, so budget_filter takes every other register out of each virtual register's list before the search starts.

Both searches follow the Chapter 5 Backtracking-Search. Each call gives one virtual register a physical register and moves on to the next one, and if no register works it backs up and tries something else for the one before it. nodes_visited counts every call, backtracks counts every time it had to back up, and ac3_revisions counts every arc AC-3 checks, which is always 0 for naive since it never runs AC-3.

AC-3 follows the Arc consistency algorithm slide. It starts with every arc in a queue (two for each interference, one each way), checks them one at a time, and whenever a virtual register loses a register, the arcs pointing at it get checked again. For a normal constraint, checking an arc means comparing every register of one virtual register against every register of the other one, which is O(d^2). With "can't be the same" constraints it's a lot simpler, a register only has to be removed when the neighbor has nothing left except that exact register, since any other register the neighbor has is different from it. So revise_arc only removes a register when the neighbor is down to its last one. This makes each check O(d), and an arc can't remove anything while the neighbor still has 2 or more registers, so the queue only actually removes something once a virtual register is down to one register.

backtrack-mac runs AC-3 on every arc before the search starts and again after every assignment, which are the two ways the Arc consistency slide says it can be used. After a virtual register gets a register, AC-3 only starts with the arcs from its neighbors that don't have a register yet, since that's the only virtual register that just changed. Every register AC-3 removes is saved in removed_list, so if that choice turns out to be a dead end they can all be put back instead of having to copy every list at every step.

MAC also uses the three heuristics from the Chapter 5 slides. MRV ("choose the variable with the fewest legal values") picks the virtual register with the fewest registers left, since it's the most likely to run out. Degree is the "tie-breaker among MRV variables", so if two are tied the one with more neighbors without a register goes first. Giving a register to the virtual register with the most unassigned neighbors first takes options away from the most other virtual registers early, so later choices have fewer options to try. LCV ("the one that rules out the fewest values in the remaining variables") tries the register that the fewest neighbors could also use first, so it takes away the least options from them. If there's still a full tie the lowest id and R0, R1, R2 order are used like the assignment requires. For example, on sample.txt v1 can only use R0, so AC-3 takes R0 away from v0 and v2 before the search even starts, MRV picks v1 first, and MAC finishes with backtrack-mac,5,0,17,SAT without backing up once, while naive tries R0 for v0 first and has to back up (backtrack-naive,6,1,0,SAT).

## SEARCH PERFORMANCE ANALYSIS
The 12 test graphs cover the sizes from the assignment (N = 10, 25, 50, 100) at 3 densities, where each possible interference was added with a 10% (sparse), 30% (medium), or 50% (dense) chance. Every graph has R0-R7 so K = 2, 4, and 8 all work, and about 10% of the virtual registers have a restricted domain to model the hardware conventions in the assignment. These results are from one run of benchmark.py with TIME_LIMIT = 10 seconds.

Table 1. Test Graphs

| Graph    | N   | Interferences | Density | Interferences / N |
|----------|-----|---------------|---------|-------------------|
| sparse_1 | 10  | 3             | 0.067   | 0.30              |
| sparse_2 | 25  | 35            | 0.117   | 1.40              |
| sparse_3 | 50  | 122           | 0.100   | 2.44              |
| sparse_4 | 100 | 495           | 0.100   | 4.95              |
| medium_1 | 10  | 8             | 0.178   | 0.80              |
| medium_2 | 25  | 87            | 0.290   | 3.48              |
| medium_3 | 50  | 364           | 0.297   | 7.28              |
| medium_4 | 100 | 1,494         | 0.302   | 14.94             |
| dense_1  | 10  | 25            | 0.556   | 2.50              |
| dense_2  | 25  | 168           | 0.560   | 6.72              |
| dense_3  | 50  | 627           | 0.512   | 12.54             |
| dense_4  | 100 | 2,470         | 0.499   | 24.70             |

Table 2. Nodes Visited — Naive vs. MAC

| Graph    | Naive K=2 | MAC K=2 | Naive K=4 | MAC K=4 | Naive K=8 | MAC K=8 |
|----------|-----------|---------|-----------|---------|-----------|---------|
| sparse_1 | 11        | 11      | 11        | 11      | 11        | 11      |
| sparse_2 | 112       | 0       | 120,310   | 1       | 26        | 26      |
| sparse_3 | 127       | 0       | limit     | 51      | 51        | 51      |
| sparse_4 | 511       | 0       | limit     | 324     | 101       | 101     |
| medium_1 | 95        | 1       | 11        | 11      | 11        | 11      |
| medium_2 | 7         | 1       | 2,513     | 29      | 26        | 26      |
| medium_3 | 93        | 0       | 648,417   | 0       | 28,406    | 51      |
| medium_4 | 21        | 0       | 479,685   | 1       | limit     | limit   |
| dense_1  | 19        | 1       | 11        | 11      | 11        | 11      |
| dense_2  | 13        | 0       | 1,241     | 7       | 7,045     | 26      |
| dense_3  | 19        | 0       | 4,965     | 1       | limit     | limit   |
| dense_4  | 7         | 0       | 2,117     | 0       | limit     | 882     |

Table 3. Backtracks — Naive vs. MAC

| Graph    | Naive K=2 | MAC K=2 | Naive K=4 | MAC K=4 | Naive K=8 | MAC K=8 |
|----------|-----------|---------|-----------|---------|-----------|---------|
| sparse_1 | 0         | 0       | 0         | 0       | 0         | 0       |
| sparse_2 | 112       | 0       | 120,310   | 1       | 0         | 0       |
| sparse_3 | 127       | 0       | limit     | 0       | 0         | 0       |
| sparse_4 | 511       | 0       | limit     | 324     | 0         | 0       |
| medium_1 | 95        | 1       | 0         | 0       | 0         | 0       |
| medium_2 | 7         | 1       | 2,487     | 3       | 0         | 0       |
| medium_3 | 93        | 0       | 648,417   | 0       | 28,355    | 0       |
| medium_4 | 21        | 0       | 479,685   | 1       | limit     | limit   |
| dense_1  | 19        | 1       | 0         | 0       | 0         | 0       |
| dense_2  | 13        | 0       | 1,241     | 7       | 7,019     | 0       |
| dense_3  | 19        | 0       | 4,965     | 1       | limit     | limit   |
| dense_4  | 7         | 0       | 2,117     | 0       | limit     | 882     |

Table 4. Solve Status by Budget

| Graph    | K=2   | K=4   | K=8          |
|----------|-------|-------|--------------|
| sparse_1 | SAT   | SAT   | SAT          |
| sparse_2 | UNSAT | UNSAT | SAT          |
| sparse_3 | UNSAT | SAT   | SAT          |
| sparse_4 | UNSAT | UNSAT | SAT          |
| medium_1 | UNSAT | SAT   | SAT          |
| medium_2 | UNSAT | SAT   | SAT          |
| medium_3 | UNSAT | UNSAT | SAT          |
| medium_4 | UNSAT | UNSAT | limit (both) |
| dense_1  | UNSAT | SAT   | SAT          |
| dense_2  | UNSAT | UNSAT | SAT          |
| dense_3  | UNSAT | UNSAT | limit (both) |
| dense_4  | UNSAT | UNSAT | UNSAT        |

Table 5. Totals — Runs Where Both Searches Finished

| Group  | Runs | Naive Nodes | MAC Nodes | Fewer  | Naive Backtracks | MAC Backtracks |
|--------|------|-------------|-----------|--------|------------------|----------------|
| K = 2  | 12   | 1,035       | 14        | 98.6%  | 1,024            | 3              |
| K = 4  | 10   | 1,259,281   | 72        | 99.99% | 1,259,222        | 13             |
| K = 8  | 9    | 35,688      | 314       | 99.1%  | 35,374           | 0              |
| sparse | 10   | 121,271     | 212       | 99.8%  | 121,060          | 1              |
| medium | 11   | 1,159,285   | 131       | 99.99% | 1,159,160        | 6              |
| dense  | 10   | 15,448      | 57        | 99.6%  | 15,400           | 9              |
| all    | 31   | 1,296,004   | 400       | 99.97% | 1,295,620        | 16             |

From Tables 2 and 4 we can see that both searches always give the same answer, all 31 runs where both finished agree on SAT or UNSAT. MAC finished 3 runs naive couldn't in 10 seconds (sparse_3 and sparse_4 with K = 4 and dense_4 with K = 8), and neither finished medium_4 or dense_3 with K = 8. Table 5 shows that across the 31 runs where both finished, naive visited 1,296,004 nodes and MAC only 400 (about 99.97% fewer), and naive backed up 1,295,620 times while MAC only backed up 16 times.

Tables 2 and 3 also show that MAC only helps when there's something to prune. sparse_1 at every K and most of the K = 8 runs visit exactly n + 1 nodes with 0 backtracks for both searches, since the first register tried always works, so in those runs MAC only adds AC-3 revisions without saving any nodes. The harder the graph the bigger the difference. medium_3 with K = 8 is SAT but naive needs 28,406 nodes and 28,355 backtracks while MAC finds it in 51 nodes without backing up once, and medium_3 with K = 4 is UNSAT, which takes naive 648,417 nodes to prove while MAC's first AC-3 pass proves it before the search even starts.

MAC visited 0 nodes on 10 runs, which means AC-3 alone proved the graph UNSAT, and 8 of those are K = 2, where a domain only has to lose one register to be down to its last one. MRV is the other big reason for the gap. sparse_2 with K = 4 has a virtual register whose domain is empty after the budget, so MRV picks it first (0 registers left), it fails right away, and MAC is done in 1 node. Naive only gets to it when the lexicographic order does, so it goes through 120,310 nodes of assignments to the virtual registers before it, which can never work. medium_4 (479,685 vs 1) and dense_3 (4,965 vs 1) with K = 4 are the same, each has 2 empty domains.

Table 4 shows that more registers make more graphs SAT, only sparse_1 is SAT with K = 2, 5 of the 12 are with K = 4, and 9 are with K = 8 (with 2 that never finished), and denser graphs need more registers, every sparse graph is SAT with K = 8 but dense_4 still isn't. Size makes the gap bigger too, with K = 4 naive goes from 11 nodes on sparse_1 (N = 10) to 120,310 on sparse_2 (N = 25) to hitting the time limit on sparse_3 and sparse_4 (N = 50 and 100), while MAC stays at 324 nodes or fewer on all of them. The hardest runs aren't the biggest or the densest ones though, they're the ones right where the graphs switch from SAT to UNSAT for that budget. MAC also pays for every node it saves with AC-3 revisions, dense_4 with K = 8 did 3,501,500 revisions to prove UNSAT in 882 nodes. Most runs take about 0.05 seconds, which is mostly the time it takes Python to start main.py, and the slowest runs that finished were naive on medium_3 and medium_4 with K = 4 (1.37 and 1.16 seconds) and MAC on dense_4 with K = 8 (3.10 seconds).

## THEORETICAL VS. EMPIRICAL COMPLEXITY
Register allocation is graph coloring, and checking if a graph can be colored with 3 or more colors is NP-complete, so no known algorithm can do it fast for every graph. The Chapter 5 lecture notes say CSPs include Boolean satisfiability, which is NP-complete, and that n variables with d possible values each have O(d^n) complete assignments. They also say that since the order of assignments doesn't matter, backtracking only assigns one variable per level, so the worst case is d^n leaves, where d is the budget K here.

Table 6. Worst Case vs. Naive Nodes Visited

| Run             | n   | d (K) | d^n          | Naive Nodes | Effective Branching Factor |
|-----------------|-----|-------|--------------|-------------|----------------------------|
| sparse_2, K = 4 | 25  | 4     | 1.13 x 10^15 | 120,310     | 1.60                       |
| medium_3, K = 4 | 50  | 4     | 1.27 x 10^30 | 648,417     | 1.31                       |
| medium_4, K = 4 | 100 | 4     | 1.61 x 10^60 | 479,685     | 1.14                       |

(the effective branching factor is nodes_visited^(1/n), how many branches each level would need on average to end up with that many nodes)

Naive is nowhere near the d^n worst case, since it checks each register against the neighbors that already have one, so most bad branches get cut off early and each level only branches 1.1 to 1.6 times on average instead of 4. It still grows exponentially though, which is why naive hit the 10 second limit 5 times, all on graphs with 50 or 100 virtual registers. MAC cuts this down even more, across the 31 runs both finished it visited 400 nodes compared to naive's 1,296,004, but it still couldn't finish dense_3 or medium_4 with K = 8, so the heuristics and AC-3 make the search a lot faster without changing the exponential worst case.

K = 2 is the one easy case for graph coloring, since 2-coloring is just checking if the graph can be split into two groups with no interferences inside a group, which takes linear time. Tables 2 and 3 match this, at K = 2 naive never needs more than 511 nodes and MAC never backs up more than once, because with only 2 registers giving one virtual register a register forces what every neighbor has to get.

The lecture notes give AC-3 as O(n^2 d^3), because there can be about n^2 arcs, each arc can be added back up to d times, and each check takes O(d^2). With "can't be the same" constraints each check is only O(d), so one AC-3 run on a graph with e interferences does at most 2e x (1 + d) checks (every arc once at the start, plus once more for each register its neighbor can lose). On dense_4 with K = 8, MAC did about 3,970 checks per node, while the most one AC-3 run could do on that graph is 44,460, and sparse_4 with K = 4 did about 281 per node out of a most of 4,950. So the AC-3 runs stay well under the worst case, since starting each run with only the arcs from the virtual register that just got a register means most arcs never need to be checked.