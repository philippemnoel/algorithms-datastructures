"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Philippe M. Noël
Neural Network 2D Regression Algorithm -- Python 3
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import keras
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from keras.layers import Dense, Activation, Dropout
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
from numpy import linalg


def neural_network(X, y):
    """ Classifies data X and labels y with a 2D Neural Network Regression """
    # plotting initial training data for visualization
    plt.figure(1); plt.clf()
    plt.xlim([-1,11]); plt.ylim([-1,11])
    plt.xlabel('x'); plt.ylabel('y')
    for i in range(1, np.size(y)):
        plt.plot(X[i,0], X[i,1],'bo')
        plt.text(X[i,0] + 0.1, X[i,1], str(np.int64(y[i])))
    plt.title('Training Data: Label as Function of (x,y)'); plt.show()

    # creating the neural network model
    np.random.seed(3456) # for reproductibility
    net = Sequential()
    net.add(Dense(3, input_dim=2, kernel_initializer='uniform', activation='sigmoid'))
    net.add(Dense(3, kernel_initializer='uniform', activation='sigmoid'))
    net.add(Dense(3, kernel_initializer='uniform', activation='sigmoid'))
    net.add(Dense(1, kernel_initializer='uniform', activation='linear'))

    # compiling the model
    net.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

    # training the model and displaying its training results
    out = net.fit(X, y, epochs=10000, batch_size=16, verbose=0)
    print('Initial Loss = ' + str(out.history["loss"][1]))
    print('Final Loss = ' + str(out.history["loss"][-1]))
    print('Initial Accuracy = ' + str(out.history["acc"][1]))
    print('Final Accuracy = ' + str(out.history["acc"][-1]))

    # plotting progress of optimization
    plt.figure(2); plt.clf()
    plt.plot(out.history["acc"])
    plt.plot(out.history["loss"])
    plt.legend(['accuracy','loss']); plt.show()

    # using our trained network to classify a new point
    X_test = np.array([[2],[0]]).T
    y_pred = net.predict(X_test)
    print('X_test = ' + str(X_test))
    print('Predicted Output = ' + str(y_pred))

    # render success
    return y_pred


# test driver & data generation
# generating data
X = np.array([[2,7,0,7,4,3,9,1,8,4,10,6,4,5,2,3,5,8,3,4],
              [10,6,7,10,8,1,3,4,4,1,1,7,10,8,0,0,2,4,6,9]]).T
y = np.array([3,3,1,3,3,1,2,1,2,1,2,3,3,3,1,1,2,2,1,3])
# driver test
neural_network(X, y)
