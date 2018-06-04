"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Philippe M. Noël
Gradient Steepest Descent Backpropagation Algorithm -- Python 3
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import matplotlib
import numpy as np
import scipy as scipy
import matplotlib.pyplot as plt
from scipy.io import loadmat
from numpy import linalg

def squared_error_cost(y_pred, y_true):
    """ Squared Error Cost for Supervised Learning NN """
    return 0.5 * sum((y_true - y_pred) ** 2)


def sigmoid(z):
    """ Sigmoid Function """
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_prime(z):
    """ Derivative of the Sigmoid Function """
    return sigmoid(z) * (1 - sigmoid(z))


def feedforward(X, w2, b2, w3, b3, w4, b4):
    """ A 2 Hidden-layer Feedforward Algorithm for Sigmoid Neural Network, with
        input X and weights and biases w and b """
    # feedforward part
    # input layer
    a1 = X
    # first hidden layer
    a2 = sigmoid(w2 @ a1 + b2)
    # second hidden layer
    a3 = sigmoid(w3 @ a2 + b3)
    # output layer
    y = sigmoid(w4 @ a3 + b4)
    return a2, a3, y


def backpropagation(X, y, w2, b2, w3, b3, w4, b4, a2, a3, a4):
    """ A 2 Hidden-layer Backpropagation Algorithm for Sigmoid Neural Network,
        with input X, label y, weights and biases w and b and feedforward
        predicted label a4 """
    # calculate cost & derivative
    cost = squared_error_cost(a4, y);
    dcost = (a4 - y)

    # backpropagation algorithm
    # second hidden layer - output layer weights
    delta4 = dcost * sigmoid_prime(w4 @ a3 + b4)
    nabla_b4 = delta4
    nabla_w4 = delta4 @ (sigmoid(w3 @ a2 + b3)).T
    # first hidden layer - second hidden layer weights
    delta3 = (w4.T @ delta4) * sigmoid_prime(w3 @ a2 + b3)
    nabla_b3 = delta3
    nabla_w3 = delta3 @ (sigmoid(w2 @ X + b2)).T
    # input - first hidden layer weights
    delta2 = (w3.T @ delta3) * sigmoid_prime(w2 @ X + b2)
    nabla_b2 = delta2
    nabla_w2 = delta2 @ X.T

    # output
    return nabla_w2, nabla_b2, nabla_w3, nabla_b3, nabla_w4, nabla_b4


def neural_network(X, y, w2, b2, w3, b3, w4, b4):
    """ A 2 Hidden-layer Sigmoid Neural Network with input X and weights and
        biases w and b """
    # display our initial weights and biases
    print("w2 = "); print(w2)
    print("b2 = "); print(b2)
    print("w3 = "); print(w3)
    print("b3 = "); print(b3)
    print("w4 = "); print(w4)
    print("b4 = "); print(b4)

    # display training data and labels
    print("X = "); print(X)
    print("y = "); print(y)

    # feedforward
    a2, a3, y_pred = feedforward(X, w2, b2, w3, b3, w4, b4)
    print("Initial Predicted Label = "); print(y_pred)

    # current cost
    initial_cost = squared_error_cost(y_pred, y)
    print("Initial Cost After Feedforward = "); print(initial_cost)

    # backpropagation
    # n_w = nabla_w // n_b = nabla_b
    n_w2, n_b2, n_w3, n_b3, n_w4, n_b4 = backpropagation(X, y, w2, b2, w3, b3, w4, b4, a2, a3, y_pred);

    # steepest descent weight improvement
    eta = 0.1 # learning rate
    w2 = w2 - eta * n_w2; b2 = b2 - eta * n_b2
    w3 = w3 - eta * n_w3; b3 = b3 - eta * n_b3
    w4 = w4 - eta * n_w4; b4 = b4 - eta * n_b4

    # re-evaluate solution and cost for revised network
    _, _, new_y_pred = feedforward(X, w2, b2, w3, b3, w4, b4)
    new_cost = squared_error_cost(new_y_pred, y)
    print("Revised Predicted Label = "); print(new_y_pred)
    print("Revised Cost After Steepest Descent = "); print(new_cost)


# driver test & data generation
# generate data
X = np.array([[0.5,1.0]]).T
y = np.array([[1.0,1.0]]).T
data = scipy.io.loadmat('data6.mat')
w2 = data['w2']; b2 = data['b2']
w3 = data['w3']; b3 = data['b3']
w4 = data['w4']; b4 = data['b4']
# driver test
neural_network(X, y, w2, b2, w3, b3, w4, b4)
