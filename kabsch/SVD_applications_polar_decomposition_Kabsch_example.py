"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Philippe M. Noël
Singular Value Decomposition - Kabsch Algorithm for Molecules Fit -- Python 3
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import matplotlib
import numpy as np
import scipy as scipy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import linalg
from scipy import linalg


def Kabsch(X, Y):
    """ Takes in X and Y, Two Molecules Represented as 2D Arrays of Coordinates
        and Checks Whether They Are the Same using SVD """
    # plot original molecules
    plt.figure(1).gca(projection='3d');
    hl1 = plt.plot(X[0,:], X[1,:], X[2,:], 'r-x', markersize=3)
    hl2 = plt.plot(Y[0,:], Y[1,:], Y[2,:], 'b-x', markersize=3)
    plt.xlabel('x'); plt.ylabel('y')
    plt.title('Are These Molecules The Same?'); plt.show();

    # find centers of mass and translate both molecules to origin of axes
    Y_t = np.zeros(X.shape); X_t = np.zeros(X.shape) # Y & X translated
    for i in range(N):
        y_mean = np.array([np.mean(Y[0,:]), np.mean(Y[1,:]), np.mean(Y[2,:])]).T
        x_mean = np.array([np.mean(X[0,:]), np.mean(X[1,:]), np.mean(X[2,:])]).T
        Y_t[:,i] = Y[:,i] - y_mean;
        X_t[:,i] = X[:,i] - x_mean;
    plt.figure(2).gca(projection='3d')
    hl1 = plt.plot(X[0,:], X[1,:], X[2,:], 'r-x', markersize=3)
    hl2 = plt.plot(Y[0,:], Y[1,:], Y[2,:], 'b-x', markersize=3)
    hl3 = plt.plot(Y_t[0,:], Y_t[1,:], Y_t[2,:],'g--o', markersize=3)
    plt.title('Green: Translated Blue and Red with Center of Mass at Origin.')
    plt.xlabel('x'); plt.ylabel('y'); plt.show()

    # find optimal rotation matrix using SVD (polar decomp)
    C = X @ Y_t.T; d = np.sign(np.linalg.det(C))
    # sanity check
    if abs(d) < 0.01:
        raise ValueError('Error: Singular Covariance.')
    V, S, W = scipy.linalg.svd(C); W = W.T
    U = W @ np.array([[1,0,0], [0,1,0], [0,0,d]]) @ V.T

    # rotate the molecule to optimal position using the matrix we found
    Y_tr = np.zeros(X.shape) # Y translated & rotated
    for i in range(N):
        Y_tr[:,i] = U.T @ Y_t[:,i]

    # plot the final molecule to see if they are the same
    plt.figure(3).gca(projection='3d')
    hl1 = plt.plot(X[0,:], X[1,:], X[2,:], 'r-x', markersize=3)
    hl2 = plt.plot(Y[0,:], Y[1,:], Y[2,:], 'b-x', markersize=3)
    hl3 = plt.plot(Y_t[0,:], Y_t[1,:], Y_t[2,:],'g--o', markersize=3)
    hl4 = plt.plot(Y_tr[0,:], Y_tr[1,:], Y_tr[2,:], 'c--o', markersize=3)
    plt.xlabel('x'); plt.ylabel('y')
    plt.legend([hl1, hl2, hl3, hl4], ['X', 'Y', 'Y translated', 'Y translated & rotated'])
    plt.title('Cyan: Rotated Green to Orient with Red'); plt.show()


# test driver & data generation
# data
# original molecule
X1 = np.array([[0.1,1,1],[0.2,1.5,1.2],[0.3,1.6,1.7],[1,2,1.8],[1.5,2.2,1.9],
               [1.5,2.5,1.5],[1.5,2.8,1.1],[1,2.7,0.5],[0.25,2.5,0.5]]).T
N = np.size(X1[1,:])
X = np.copy(X1) # final position, X, centered around zero
for i in range(N):
    x_mean = np.array([np.mean(X1[0,:]), np.mean(X1[1,:]), np.mean(X1[2,:])])
    X[:,i] = X1[:,i] - x_mean
# creating the translated noisy second molecule
# rotate about a specified axis, calculated in Matlab using
# rotationmat3D(pi*0.4,[0 0 1])
A = np.array([[0.3090,   -0.9511,      0],
              [0.9511,    0.3090,      0],
              [0,         0,           1]])
Y = np.copy(X1)
for i in range(N):
    Y[:,i] = A @ X[:,i];
# translating and adding a bit of random noise
for i in range(N):
    Y[:,i] = Y[:,i] + np.array([4,3,3]) + 0.2 * (np.random.random((1, 3)) - 0.5)
# driver test
Kabsch(X, Y)
