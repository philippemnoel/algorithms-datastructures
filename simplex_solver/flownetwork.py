"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Harvard CS124 - Spring 2018
Philippe Noël - Pset 8 - Flownetwork
Python version of Flownetwork
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import random

""" Beginning of Subroutine Simplex LP Solver Algorithm """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# A modified version of the simplex implementation from the MIT ACM ICPC team
# notebook at http://web.mit.edu/~ecprice/acm/notebook.pdf, used with
# permission from former team member Eric Price.

# This is a simple simplex solver.  It solves:
# Maximize obj[0] + obj[1]*x*1 + ... + obj[n]*x_n
# Subject to x_1 >= 0, ..., x_n >= 0
# for each i, c[i][0] + c[i][1]*x_1 + ... + c[i][n]*x_n >= 0
# DO NOT TRY TO REUSE LP OBJECTS!!!!!  (INFEASIBLE corrupts them.)

# START SIMPLEX CODE
class LP:
    def __init__(self, nvars, ncons):
        self.nvars = nvars
        self.ncons = ncons
        self.cols = nvars + 1
        self.obj = [0.0 for i in range(1 + nvars)]
        self.c = [[0.0 for j in range(self.cols)] for i in range(ncons)]
        self.nonbasic_orig = [i for i in range(nvars)]
        self.basic_orig = [i + nvars for i in range(ncons)]
        self.assignments = []

    def perturb(self):
        for i in range(self.ncons):
            self.c[i][0] += 1e-10 * random.random()

    def pivot(self, col, row):
        # enforce that the old col remains nonnegative
        val = 1.0 / self.c[row][col]
        for i in range(self.cols):
            self.c[row][i] *= -val
        self.c[row][col] = val

        # subtract the extra stuff the pivot row brings along
        for i in range(self.ncons):
            if i == row:
                continue
            coeff = self.c[i][col]
            self.c[i][col] = 0.0
            if coeff != 0.0:
                for j in range(self.cols):
                    self.c[i][j] += coeff * self.c[row][j]

        coeff = self.obj[col]
        self.obj[col] = 0.0
        for j in range(self.cols):
            self.obj[j] += coeff * self.c[row][j]

        # swap; update maps to original indices
        temp = self.nonbasic_orig[col - 1]
        self.nonbasic_orig[col - 1] = self.basic_orig[row]
        self.basic_orig[row] = temp

    def simplex(self):
        # Bland's rule: pick an arbitrary column and do the pivot
        # that will change it the least
        while(True):
            # pick a random nonbasic column to pivot
            offset = random.randrange(32767) % (self.cols - 1)
            col = -1
            for i in range(self.cols - 1):
                c = (offset + i) % (self.cols - 1) + 1
                if self.obj[c] > 1e-8:
                    col = c
                    break
            if col == -1:
                break # this basis is optimal

            # find the row that will hit zero first
            min_change = 1e100
            best_row = -1
            for row in range(self.ncons):
                if self.c[row][col] >= -1e-8:
                    continue
                change = -self.c[row][0] / self.c[row][col]
                if change < min_change:
                    min_change = change
                    best_row = row

            if best_row == -1: # unbounded
                return False

            self.pivot(col, best_row)

        # produce output
        self.objval = self.obj[0]
        self.assignments = [0.0 for i in range(self.ncons + self.nvars)]
        for i in range(self.ncons):
            self.assignments[self.basic_orig[i]] = self.c[i][0]
        for i in range(self.nvars):
            self.assignments[self.nonbasic_orig[i]] = 0.0
        return True

    def phase1(self):
        # find equation with minimum b
        worst_row = 0
        for i in range(self.ncons):
            if self.c[i][0] < self.c[worst_row][0]:
                worst_row = i

        if self.c[worst_row][0] >= -1e-8:
            return "FEASIBLE"

        # add a new variable epsilon, which we minimize
        for i in range(self.ncons):
            self.c[i].append(1.0)
        orig_obj = self.obj[:]
        self.obj = [0.0 for i in range(self.cols)]
        self.obj.append(-1.0)
        eps_var = self.nvars + self.ncons
        self.nonbasic_orig.append(eps_var)
        self.nvars += 1
        self.cols += 1

        # we started out infeasible, so pivot epsilon in to the basis
        self.pivot(self.cols - 1, worst_row)
        if not self.simplex():
            return "FAILED" # unbounded phase 1 here is bad
        if self.objval < -1e-9:
            return "INFEASIBLE" # epsilon must be nonpositive

        # force epsilon out of the basis
        # (it's zero anyway within our precision)
        for i in range(self.ncons):
            if self.basic_orig[i] == eps_var:
                self.pivot(1, i)
                break

        # find epsilon's column
        eps_col = -1
        for i in range(self.nvars):
            if self.nonbasic_orig[i] == eps_var:
                eps_col = i + 1

        # epsilon is nonbasic and thus zero, so we can remove it
        for i in range(self.ncons):
            self.c[i][eps_col] = self.c[i][self.cols - 1]
            del self.c[i][-1]

        self.nonbasic_orig[eps_col - 1] = self.nonbasic_orig[-1]
        del self.nonbasic_orig[-1]
        self.cols -= 1
        self.nvars -= 1

        # restore the original objective
        self.obj = [0.0 for i in range(self.cols)]
        self.obj[0] = orig_obj[0]
        for i in range(self.nvars):
            if self.nonbasic_orig[i] < self.nvars:
                self.obj[i+1] = orig_obj[self.nonbasic_orig[i] + 1]

        for i in range(self.ncons):
            if self.basic_orig[i] < self.nvars:
                for j in range(self.cols):
                    self.obj[j] += (orig_obj[self.basic_orig[i] + 1] *
                                    self.c[i][j])

        return "FEASIBLE"

    def solve(self):
        self.perturb()
        p1_res = self.phase1()
        if p1_res != "FEASIBLE":
            return p1_res
        self.assignments = []
        if not self.simplex():
            return "UNBOUNDED"
        return "OPTIMAL"

    # end
    def checkedSolve(self):
        solve_result = self.solve()
        if solve_result == "OPTIMAL" or solve_result == "UNBOUNDED":
            for i in range(self.ncons):
                assert(self.c[i][0] >= -1e-8)
        return solve_result

    # start
    def printState(self):
        print('{0:.6f}'.format(self.objval))
        for i in range(self.nvars):
            print(' x{0} = {1:.6f}'.format(i, self.assignments[i]))
        for i in range(self.ncons):
            print(' r{0} = {1:.6f}'.format(i, self.assignments[self.nvars+i]))
# END SIMPLEX CODE
""" End of Subroutine Simplex LP Solver Algorithm """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""" Subroutine code for the Flownetwork Algorithm """
def flownetwork():
    # read T (network towers), K (pairs of towers)
    # T = number of variables, K = number of constraints in LP
    T, K = map(int, raw_input().split())
    # storing all the tower edges and their capacities
    towers = dict()
    # read all towers info
    for u in range(1, T + 1):
        # get all the info per tower and add it to our towers list
        capacities = list(map(int, raw_input().split()))
        for v in range(1, T + 1):
            towers[(u, v)] = capacities[v - 1]
    # storing all the tower pairs
    tower_pairs = dict()
    # read all pairs of towers
    for pair_number in range(1, K + 1):
        # get all the info per tower pair and add it to our pairs list
        s, t, d = list(map(int, raw_input().split()))
        tower_pairs[pair_number] = (s, t, d)
    """ Converting the data into a linear programming problem """
    # very basic hash function to have a different index for all of our
    # constraints
    hashes = dict()
    index = 0 # because first term is the constant
    # loop over all edges
    for u in range(1, T + 1):
        for v in range(1, T + 1):
            # loop over all the flows
            for i in range(1, K + 1):
                hashes[(u, v, i)] = index
                index += 1
    # initialize linear programming problem
    # maximize y in f_i >= y * d_i
    # K tower pairs constraints + need for all variable to be > 0 but
    # the LP class automatically includes the constraints that all variables
    # have to be nonnegative
    n = K * (T * T) + 1
    m = 2 * K * (T - 2) + T * T + K + 1
    pg = LP(n, m)
    # maximize y in f_i >= y * d_i
    # all non-specified variables are set to 0
    # arbitrarily define last variable to be y, index 0
    pg.obj[n] = 1; # maximize 1*y, everything else 0
    # keep track of which constraint number we are at
    cnum = 0
    # first constraint block: Sum over all edges flow <= capacity of edge
    # constraint number counter
    # loop over all edges
    for u in range(1, T + 1):
        for v in range(1, T + 1):
            pg.c[cnum][0] = towers[(u, v)]
            # loop over all the flows
            for i in range(1, K + 1):
                pg.c[cnum][hashes[(u, v, i)]] = -1
                # indent the constraint for this edge flow
            cnum += 1
    # second constraint block: All data flow entering an edge must be equal to
    # the data flow leaving the edge
    # loop over all edges
    for i in range(1, K + 1):
        # source and sink
        s = tower_pairs[i][0]
        t = tower_pairs[i][1]
        for v in range(1, T + 1):
            # source and sink don't have match inflow/outflow
            if v != s and v != t:
                for u in range(1, T + 1):
                    # need to add in both directions
                    pg.c[cnum][hashes[(u, v, i)]] += 1
                    pg.c[cnum][hashes[(v, u, i)]] += -1
                    pg.c[cnum + 1][hashes[(u, v, i)]] += -1
                    pg.c[cnum + 1][hashes[(v, u, i)]] += 1
                # incrementing constraint
                cnum += 2
    # third constraint block: flow out of source >= y * d_i
    for i in range(1, K + 1):
        # source
        s = tower_pairs[i][0]
        # demand for this flow
        d_i = tower_pairs[i][2]
        for v in range(1, T + 1):
            pg.c[cnum][hashes[(s, v, i)]] = 1
        pg.c[cnum][n] = -1 * d_i
        cnum += 1
    # fourth constraint block: no flow into a source from a f(s,t) or out of a
    # sink for a f(s,t)
    # just need to do a single negative summation since they all need to be 0
    # for it to be zero anyway so we can make it into one giant long equation
    # with only the negative
    # therefore we can actually do this with only 1 constraint
    for i in range(1, K + 1):
        # source and sink
        s = tower_pairs[i][0]
        t = tower_pairs[i][1]
        for u in range(1, T + 1):
            pg.c[cnum][hashes[(u, s, i)]] = -1
            pg.c[cnum][hashes[(t, u, i)]] = -1
    # unnecessary, but for testing & clarity
    cnum += 1
    # solve the linear flow network problem
    result = pg.solve()
    # cases for no solution
    if result == "UNBOUNDED":
        print("Can distribute infinite data flow!")
    elif result == "INFEASIBLE":
        print("Impossible to distribute all the data!")
    # case with solution, max data flow that can be distributed over the network
    else:
        print('{0:.3f}'.format(pg.objval))

""" Function call for testing """
flownetwork()
