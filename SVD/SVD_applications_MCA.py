"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Philippe M. Noël
Singular Value Decomposition - Maximum Covariance Analysis -- Python 3
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import matplotlib
import numpy as np
import scipy as scipy
import matplotlib.pyplot as plt
from scipy.linalg import svd
from numpy import linalg

def MCA(X, Y):
    """ Performs the Maximum Covariance Analysis of Two Datasets, X & Y, using
        Singular Value Decomposition """
    # step 1: preparing the data
    M, N = np.shape(X)
    L, N = np.shape(Y)
    # adding noise for realism
    np.random.seed(3958); a = 1.5 # for reproducibility
    X = X + a * np.random.random((M, N))
    Y = Y + a * np.random.random((L, N))
    # removing time means
    for m in range(M):
        X[m,:] = X[m,:] - np.mean(X[m,:])
    for l in range(L):
        Y[l,:] = Y[l,:] - np.mean(Y[l,:])
    # final manipulation for better results in our example
    X[:2,:] = X[:2,:] * 3; Y[1,:] = Y[1,:] * 0.5; Y[2,:] = -1 * Y[2,:]

    # plot data for visualization
    plt.figure(0); plt.clf();
    hlX=plt.plot(np.arange(0, N), X[0,:],'-rx'
                ,np.arange(0, N), X[1,:],'-g+'
                ,np.arange(0, N), X[2,:],'-bo'
                ,np.arange(0, N), X[3,:],'-k')
    hlY=plt.plot(np.arange(0, N), Y[0, :],'--rx'
                ,np.arange(0, N), Y[1, :],'--g+'
                ,np.arange(0, N), Y[2, :],'--bo')
    plt.xlabel('Day'); plt.ylabel('Stock Prices')
    plt.title('Stock Prices: New York (Thick) & Tokyo (Thin)')
    plt.legend(['NY1', 'NY2', 'NY3', 'NY4', 'Tokyo1', 'Tokyo2', 'Tokyo3'])
    plt.show()

    # calculating the covariance matrix
    C = X @ Y.T / N
    print('Covariance Matrix: '); print(C)
    U, S, V = scipy.linalg.svd(C) # SVD

    # get singular values and important modes
    S = np.diag(S); V = V.T
    print('Singular Values: '); print(S)

    # based on the singular values, only the first SVD mode matters
    print('U[:,0]: '); print(U[:,0])
    print('V[:,0]: '); print(V[:,0])


# driver test & data generation
# generating data -- stocks in Tokyo and New York
X = np.array([[1,2,3,4,5,4,3,2,1,0],
              [2,3,4,5,6,5,4,3,2,1],
              [6,4,6,4,6,4,6,4,6,4],
              [9,5,9,5,9,5,9,5,9,5]])
Y = np.array([[1,2,3,4,5,4,3,2,1,0],
              [9,8,7,8,9,8,7,8,9,8],
              [2,3,4,5,6,5,4,3,2,1]])
# driver test
MCA(X, Y)
