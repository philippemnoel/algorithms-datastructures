"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Philippe M. Noël
k-NN Kernel Regression Algorithm -- Python 3
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import matplotlib
import numpy as np
import scipy as scipy
import matplotlib.pyplot as plt
from numpy import linalg

def k_NN_regression(N, k, sigma):
    """ Performs k-NN Kernel Regression of N Data Points, using k Nearest
        Neighbors and Sigma for Calculating Weights as Gaussian of Distances """
    # example case of house price as function of area & age
    # suppose the dependence is given by price = 2 + area^2 - age
    age, area = np.arange(0, 1, 0.05), np.arange(0, 1, 0.05)
    AGE, AREA = np.meshgrid(age, area)
    price = 2 + AREA ** 2 - AGE

    # data plotting
    plt.figure(1); plt.clf(); plt.contour(age, area, price); plt.colorbar
    plt.axis('square'); plt.set_cmap('jet')
    plt.xlabel('Age'); plt.ylabel('Area')
    plt.title('True House Prices (Contours) and Training Data (x)')
    plt.show()

    # generate training data
    np.random.seed(7639) # for reproducibility
    X = np.random.random((2, N)) # coordinates = (age, area)
    V = 2 + X[1,:] ** 2 - X[0,:] # labels

    # plot training data (colors indicate label values (house prices))
    plt.scatter(X[0,:], X[1,:], s=24, c=V, marker='x')
    # plot a marker at the point to be classified
    x, y = 0.8, 0.3
    plt.scatter(x, y, s=400, marker='+');
    plt.show()

    # calculate distances from training data to point to be classified
    d = np.zeros((N))
    for i in range(N):
        d[i] = np.linalg.norm(np.array([x,y]) - X[:,i])

    # sort distances, find k Nearest Neighbors & their distances for a given k
    I = d.argsort(axis=0)
    X_NN = X[:,I[:k]]; V_NN = V[I[:k]]; d_NN = d[I[:k]]
    K = np.diag(np.exp(-1 * (d_NN / sigma) ** 2)) # kernel K

    # get nearest neighbors information
    print('Nearest Neighbors Coordinates: ', end=""); print(X_NN.T)
    print('Nearest Neighbors Labels (Prices): ', end=""); print(V_NN.T)
    print('Nearest Neighbors Distances: ', end=""); print(d_NN.T)
    print('Nearest Neighbors Weights: ', end=""); print(np.diag(K))

    # calculating regression coefficients
    w = np.linalg.inv(X_NN @ K @ X_NN.T) @ X_NN @ K @ V_NN.T

    # get predicted versus real label
    print('Predicted Price Based On Optimal Regression Coefficients: ', end="")
    predicted_output = w @ np.array([x,y]).T
    print(predicted_output)
    true_label = 2 + y ** 2 - x
    print('True Label Value: ' + str(true_label))

    # render success
    return predicted_output


# test driver
k_NN_regression(50, 6, 0.2)
