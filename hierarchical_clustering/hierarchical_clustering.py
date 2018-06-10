"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Philippe M. Noël
Hierarchical Clustering Algorithm -- Python 3
Original Code from Harvard APMTH120
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import numpy as np
import scipy as scipy
import matplotlib
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import cophenet, dendrogram, linkage, fcluster

def HierarchicalClustering(X):
    """ Takes in a N by 2 array X and performs the hierarchical clustering """
    # draw original data
    plt.figure(1); plt.clf()
    plt.plot(X[:,0], X[:,1], '.')
    plt.title('Original Input Data');

    # perform near-neighbor hierarchical clustering of X
    Z = linkage(X, 'ward') # other methods could be used

    # plot dendrogram
    plt.figure(2); plt.clf()
    dendrogram(Z, truncate_mode='lastp', p=12, leaf_rotation=90.,
               leaf_font_size=12., show_contracted=True)
    plt.title('Dendrogram of Hierarchical Clustering of X'); plt.show()

    # we now find the appropriate number of clusters with elbow plot
    # establish max number of clusters
    if np.size(X[:,1]) < 10:
        k_max = np.size(X[:,1]) - 1
    else:
        k_max = 10
    # diameters of clusters
    diameters = np.zeros((k_max, k_max))
    max_diameter = np.zeros((k_max, 1))

    # loop over all k number of clusters
    for k in range(1, k_max + 1):
        # divide into requested number of clusters
        idx = fcluster(Z, k, 'maxclust')
        # calculate max diameter of clusters
        for i in range(1, k + 1):
            # check all points belonging to cluster i out of the k clusters
            a_cluster = X[idx==i,:]
            dist_in_cluster = pdist(a_cluster, 'euclid')
            # store diameters
            if np.size(dist_in_cluster) > 1:
                diameters[i - 1, k - 1] = np.mxa(dist_in_cluster)
            else diameters[i - 1, k - 1] = 0
        max_diameter[k - 1] = np.max(diameters[:, k - 1]) # max for a specific k

    # elbow plot
    plt.figure(3); plt.clf()
    plt.plot(np.arange(1, k_max + 1), max_diameter, '-x')
    plt.xlabel('k'); plt.ylabel('Max Diameter of Clusters')
    plt.title("Elbow Plot: Finding Optimal # of Clusters"); plt.show()


# driver test & data generation
# generate random test data
shift_1 = np.ones((N, 2))
shift_2 = np.hstack([np.ones((N, 1), -np.ones((N , 1)))])
np.random.seed(8765) # for reproductibility
X = np.vstack([np.random.random])
X = np.vstack([np.random.random((N, 2)) * 0.3 * 0.75 + shift1,
               np.random.random((N, 2)) * 0.3 * 0.50 - shift1,
               np.random.random((N, 2)) * 0.3 * 0.25 + shift2,
               np.random.random((N, 2)) * 0.3 * 0.35 - shift2])
# driver test
HierarchicalClustering(X)
