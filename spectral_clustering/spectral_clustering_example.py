"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Philippe M. Noël
Spectral Clustering Algorithm -- Python 3
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import numpy as np
import scipy as scipy
import matplotlib
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist,squareform
from sklearn.cluster import KMeans
from numpy import linalg


def SpectralClustering(X, N, k):
    """ Divides a set or network X into two or more subsets using the
        eigenvectors of the Laplacian matrix """
    # plot original data
    plt.figure(0); plt.clf()
    plt.plot(X[:,0], X[:,1], '.')
    plt.legend(['Data']); plt.title('Original Data')
    plt.tight_layout(); plt.show()

    # build distance, adjacency, degree & Laplacian matrices
    distances = squareform(pdist(X, 'euclid'))
    dist_mean = np.mean(distances)
    sigma = dist_mean / 2 # somewhat arbitrary choice of threshold
    W = np.exp(-distances ** 2 / sigma ** 2) # adjacency matrix
    D = np.diag(sum(W)) # degree matrix
    L = D - W # Laplacian matrix
    plt.figure(1); plt.subplot(2,2,4); plt.imshow(L); plt.colorbar
    plt.title('Laplacian: $L=D-W$');
    plt.subplot(2,2,3); plt.imshow(D); plt.colorbar
    plt.title('Degree Matrix');
    plt.subplot(2,2,2); plt.imshow(W); plt.colorbar
    plt.title('Similarity: $\exp(-d_{ij}^2/\sigma^2)$');
    plt.subplot(2,2,1); plt.imshow(distances); plt.colorbar
    plt.title('Distances, $d_{ij}=|x_i-x_i|$')
    plt.tight_layout(); plt.show()

    # calculate & sort eigenvalues
    D, V = scipy.linalg.eig(L)
    idx = D.argsort(); D = D[idx]; V = V[:,idx]; D = np.diag(D)

    # display number of clusters depending on given k
    if k == 2:
        print('Using eigenvector #2 to cluster the data!')
    else:
        print('Using eigenvectors #2-' + str(k) + ' to cluster the data!')

    # for better plotting
    colors = 'rgbcmyrgbcmyrgbcmyrgbcmy'
    marker = '......xxxxxx++++++oooooo'

    # plot eigenvalues & eigenvectors & highlight second smallest
    # eigenvalues
    plt.figure(3); plt.clf(); plt.subplot(2,1,1)
    d = np.diag(D); plt.plot(d, '-x')
    plt.plot(1, d[1], 'ro'); plt.plot(1, d[1], 'rx')
    plt.title('Eigenvalues of Laplacian Matrix')
    plt.subplot(2,1,2); plt.title('Eigenvectors 1-4 of Laplacian Matrix');
    for i in range(4):
        hl = plt.plot(V[:,i], colors[i] + 'x-')
    plt.legend(['1','2','3','4']); plt.tight_layout(); plt.show()

    # assign clusters based on sign of second eigenvector
    if k == 2:
        idx = np.zeros((N * 4, 1))
        idx[V[:,1] > 0] = 0
        idx[V[:,1] <= 0] = 1
    # KMeans more efficient here so we just do that instead (kinda cheating)
    elif k > 2:
        kmeans = KMeans(n_clusters=k, n_init=5, copy_x=True).fit(V[:,:k])
        idx = kmeans.labels_
        C = kmeans.cluster_centers_

    # plot our clustered results
    X_0, X_1 = [], []
    plt.figure(4); plt.clf()
    for i in range(k):
        X_0 = [X[i,0] for i in range(N * 4) if idx[i] == i]
        X_1 = [X[i,1] for i in range(N * 4) if idx[i] == i]
        plt.plot(X_0, X_1, colors[i] + marker[i])
        plt.hold(True)
    legend = [] # building the legend
    for i in range(k):
        legend.append('Cluster ' + str(i))
    plt.legend(legend); plt.title('Cluster Assignments')
    plt.tight_layout(); plt.show()


# driver test & data generation
# generating data of several random clusters
N = 20; sigma = 0.3; k = 2; mu = 0
shift1 = np.ones((N, 2)); shift2 = np.hstack([np.ones((N, 1)),-np.ones((N, 1))])
np.random.seed(6734) # for reproductibility
X = np.vstack([np.random.normal(mu, sigma, (N, 2)) * 0.25 - 0.7 * shift2,
               np.random.normal(mu, sigma, (N, 2)) * 0.35 + shift1,
               np.random.normal(mu, sigma, (N, 2)) * 0.25 - shift2 + 0.4 * shift1,
               np.random.normal(mu, sigma, (N, 2)) * 0.35 - shift2 - 0.5 * shift1])
# driver test
SpectralClustering(X, N, k)
