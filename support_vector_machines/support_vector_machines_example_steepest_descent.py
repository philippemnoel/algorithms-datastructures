"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Philippe M. Noël
Support Vector Machines Classification (Steepest Descent Iters) -- Python 3
The SVM Line is: w[0]x + w[1]y + b = 0
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import matplotlib
import numpy as np
import scipy as scipy
import matplotlib.pyplot as plt
from numpy import linalg
from scipy import io

def squared_mean_cost(X, y, C, w, N):
    """ Calculates Squared Mean Cost Between Current Guess & True Label """
    cost = 0.5 * sum(w ** 2)
    for i in range(N):
        cost += C * np.max([0, 1 - y[i] * w.T @ X[i,:]])
    return cost

def gradient(X, y, C, w, N):
    """ Calculates the Gradient for our Steepest Descent """
    d, grad = np.size(w), np.zeros(w.shape)
    for i in range(N):
        if y[i] * w.T @ X[i,:] < 1:
            for j in range(d):
                grad[j] = grad[j] - C * y[i] * X[i,j]
    return grad


def SVM(X, y, N, C, w, x, eta):
    """ Classfies Points With a Linear Function Trained with Steepest Descent """
    # plot training data
    sym = ['x' if y[i] < 0 else 'o' for i in range(N)] # define symbols
    plt.figure(1); plt.clf()
    for i in range(N):
        plt.plot(X[i,0], X[i,1], color='b', marker=sym[i], markersize=3)
        if N <= 30:
            plt.text(X[i,0] + 0.05, X[i,1], str(i), fontsize=8)
    # superimpose initial guess for the SVM line
    if w[1] != 0:
        hl, = plt.plot(x, (-x * w[0] - w[2]) / w[1], 'r--')
    elif w[0] != 0:
        hl, = plt.plot((-x * w[1] - w[2]) / w[0], x, 'r--')
    plt.xlabel('$X_1$'); plt.ylabel('$X_2$');
    plt.title('SVM Classification: o = +1, x = -1')
    plt.axis('square'); plt.xlim([-1,1]); plt.ylim([-1,1])
    plt.pause(0.05)

    # SVM learnig iterations -- we arbitrarily decide upon 10
    print('SVM Learning Iterations: ')
    for i in range(10):
        # get current cost and gradient
        cost = squared_mean_cost(X, y, C, w, N)
        grad = gradient(X, y, C, w, N)
        # adapt our w with steepest descent and our eta learning rate
        w = w - eta * grad
        # draw new SVM line
        plt.figure(2); hl.set(linestyle='--', color='m')
        if w[1] != 0:
            hl, = plt.plot(x, (-x * w[0] - w[2]) / w[1],'r-')
        elif w[0] != 0:
            hl, = plt.plot((-x * w[1] - w[2]) / w[0], x, 'r-')
        # re-plot data
        for i in range(N):
            plt.plot(X[i,0], X[i,1], color='b', marker=sym[i], markersize=3)
            if N <= 30:
                plt.text(X[i,0] + 0.05, X[i,1], str(i), fontsize=8)
        plt.xlabel('$X_1$'); plt.ylabel('$X_2$'); plt.title('Iteration #' + str(i))
        plt.axis('square'); plt.xlim([-1,1]); plt.ylim([-1,1])
        plt.pause(0.05)


# test driver & data generation
# loading data
mat = scipy.io.loadmat('X.mat')
X = np.array(mat['X']);
y = np.array(mat['y']).T
N = np.size(y)
C = 1000; dim = 2; eta = 0.01
# initialize w & b for plotting SVM lines
x = np.array([-10,5]); w = np.ones((dim + 1,1)); # last element is for b
# driver test
SVM(X, y, N, C, w, x, eta)
