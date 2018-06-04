"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Philippe M. Noël
Principal Component Analysis (Covariance Matrix Method) -- Python 3
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import matplotlib
import numpy as np
import scipy as scipy
import matplotlib.pyplot as plt
from numpy import linalg

def PCA_covariance(F, N, tp):
    """ Performs PCA Analysis using the Covariance Matrix Method for a Dataset
        F with a 200 Points Visualization """
    # display a small sample of the data
    print('Sample Data'); print(F[:,0:8])

    # plot data
    matplotlib.rcParams.update({'font.size': 18}) # default font size
    plt.figure(1); plt.clf();
    hl1 = plt.plot(tp, F[0,tp], 'r-', linewidth=2);
    hl2 = plt.plot(tp, F[1,tp], 'g-', linewidth=2);
    hl3 = plt.plot(tp, F[2,tp], 'b-', linewidth=2);
    hl4 = plt.plot(tp, F[3,tp], 'c-', linewidth=2);
    plt.legend([hl1,hl2,hl3,hl4], ['F1','F2','F3','F4']);
    plt.xlabel('Day'); plt.ylabel('Price'); plt.title('Stock Prices');
    plt.show()

    # calculating the covariance matrix & the principal components (PCs)
    C = (F @ F.T) / N
    D, U = np.linalg.eig(C)
    # sort eigenvalue & eigenvector pairs by increasing order of absolute value
    idx = np.abs(D).argsort(); idx = idx[::-1]
    D = D[idx]; U = U[:,idx]

    # display the PCs, eigenvalues and time series
    print('PCs: '); print(U)
    print('Eigenvalues: ', end=""); print(D)
    V1 = U.T @ F # time series
    print('Time Series of the PCs: '); print(V1[:,:7])

    # plot the time expansion coefficients
    plt.figure(2); plt.clf()
    hl1 = plt.plot(tp, V1[0,tp], 'm-', linewidth=2);
    hl2 = plt.plot(tp, V1[1,tp], 'c-', linewidth=2);
    hl3 = plt.plot(tp, V1[2,tp], 'b-', linewidth=2);
    hl4 = plt.plot(tp, V1[3,tp], 'k--', linewidth=2);
    plt.legend([hl1,hl2,hl3,hl4], ['v1','v2','v3','v4']); # cols of V
    plt.xlabel('Time'); plt.ylabel('$v_i(t)$');
    plt.title('Expansion Coefficients $v_{ni}$:'); plt.show()

    # display explained variance
    exlained_variance = D / sum(D); print(explained_variance)
    return explained_variance


# test driver & making data
# data (ex: time series of 4 stocks)
N = 100000 # number of data points
M = 4 # number of points for a given time
Np = 200 # portion of data to plot & visualize
V1 = np.array([0., 1.5, 0., -1.]); V2 = np.array([0.5, 0., 1.5, 0.])
V1.shape = (4, 1); V2.shape = (4, 1)
t = np.arange(1, N); tp = np.arange(1, Np)
F = 3 * V1 * np.cos(t / 3) + V2 * np.cos(t / 5)
# test driver
PCA_covariance(F, N, tp)
