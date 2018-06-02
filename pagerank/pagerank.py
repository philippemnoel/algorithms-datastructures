"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Philippe M. Noël
PageRank Algorithm -- Python 3
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import numpy as np
import scipy as scipy
import matplotlib
from numpy import linalg
from scipy.sparse.linalg import eigs
import matplotlib.pyplot as plt

def PageRank(Q, alpha):
    """ Takes an N by N 2D array representing a network and a teleportation
        factor and returns the ranking of the N pages of the network """
    # get first eigenvector & eigenvalue pair
    D, V = scipy.sparse.linalg.eigs(Q.T, k=1)
    V = abs(V) # get rid of + 0i imaginary terms

    # fix nodes w/out ougoing links
    N = len(Q) # number of nodes
    for i in range(N):
        # the row (node) only has zeroes
        if np.count_nonzero(Q[i]) == 0:
            Q[i] = np.full((1, N), 1/N)

    # add teleportation factor
    Q = alpha * Q + (1 - alpha) * (1/N) * np.ones((N, N))

    # initial guess
    x = np.full((1, N), 1/N); print(x)

    # power method iteration to find the ranking, we arbitrarily decide 20 iters
    # we print after every iteration to see convergence
    for i in range(20):
        x = x @ Q; print(x)

    # normalize and compare to eigenvalue, checking for error
    x = x / np.linalg.norm(x); print(x)
    print(V.T) # basically the same, so x is about unit length

    # render success
    return x


# driver test
Q=np.array([[1/6, 1/6, 1/6, 1/6, 1/6, 1/6],
            [1/2, 0,   1/2, 0,   0,   0],
            [1/3, 1/3, 0,   1/3, 0,   0],
            [0,   0,   1/3, 0,   1/3, 1/3],
            [0,   0,   0,   1/2, 0,   1/2],
            [0,   0,   0,   1,   0,   0]]);
PageRank(Q, 0.9)
