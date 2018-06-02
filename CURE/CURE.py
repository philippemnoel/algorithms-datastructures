"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Philippe M. Noël
Clustering Using REpresentatives (CURE) Algorithm -- Python 3
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import numpy as np
import scipy as scipy
import matplotlib.pyplot as plt
from numpy import linalg
from scipy import io
from scipy.spatial.distance import pdist,squareform
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import fcluster

def CURE():
    """ Clustering Using REpresentatives from .mat file """
    # loading data
    X = scipy.io.loadmat('CURE_data.mat')['X']
    N = len(X[1,:])

    # randomly submsapling data to generate representatives
    np.random.seed(3989) # other seeds could be used
    X = X[:,np.random.permutation(N)]
    N_reps = 300 # arbitrarily subsampling first 300 points
    X_reps = X[:,0:N_reps]

    # hierarchical clustering of subsampe to get representatives
    Z = linkage(X.T, 'single') # single linkage due to nature of data
    k = 2 # 2 clusters
    IDX_reps = fcluster(Z, k, criterion='maxclust')

    # plotting representatives for visualization
    plt.figure(1); plot.clf()
    reds = np.vstack([X_reps[:,i] for i in range(N_reps) if IDX_reps[i] == 1])
    blues = np.vstack([X_reps[:,i] for i in range(N_reps) if IDX_reps[i] == 2])
    plt.plot(reds[:,0], red[:,1], '.r'); plt.plot(blues[:,0], blues[:,1], '.b')
    plt.legend(['Cluster #1', 'Cluster #2'])
    plt.title('Representatives, N = ' + str(N_reps))

    # going over data set to assign all points to clusters
    distances, IDX = np.zeros(N_reps), np.zeros(N)
    for i in range(N):
        # find nearest representative to data point i
        for j in range(N_reps):
            distances[j] = scipy.linalg.norm(X[:,i] - X_reps[:,j])
        # find nearest cluster and assign it
        nearest = np.argmin(distances)
        IDX[i] = IDX_reps[nearest]

    # plotting clustered dataset
    plt.figure(2); plot.clf()
    reds = np.vstack([X[:,i] for i in range(N) if IDX[i] == 1])
    blues = np.vstack([X[:,i] for i in range(N) if IDX[i] == 2])
    plt.plot(reds[:,0], red[:,1], '.r'); plt.plot(blues[:,0], blues[:,1], '.b')
    plt.legend(['Cluster #1', 'Cluster #2'])
    plt.title('Full Dataset, N = ' + str(N))


# test driver
CURE()
