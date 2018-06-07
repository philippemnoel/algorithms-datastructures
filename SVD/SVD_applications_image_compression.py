"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Philippe M. Noël
Original Code From Eli Tziperman - Harvard APMTH120
Singular Value Decomposition - Image Compression -- Python 3
Based on: https://inst.eecs.berkeley.edu/~ee127a/book/login/l_svd_apps_image.html
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import matplotlib
import numpy as np
import scipy as scipy
import matplotlib.pyplot as plt
from numpy import linalg
from scipy.linalg import svd
from scipy.misc import imread
from skimage.color import rgb2gray

def SVDImgCompression():
    """ Uses SVD to Perform Image Compression of a .bmp, .jpg or .png Image """
    # read data
    img = scipy.misc.imread('beach.jpg') # loads image as a 3D array
    img = rgb2gray(img)
    img = np.double(img) # transform to real values
    N = np.size(img[:,1]) # image size

    # display original image
    plt.figure(0); plt.clf(); plt.imshow(img); plt.set_cmap('gray')
    plt.title('Original Image, size = ' + str(N) + ' by ' + str(N))
    plt.show()

    # perform SVD through scipy method
    U, S, V = scipy.linalg.svd(img)

    # plotting the singular values for analyasis
    plt.figure(1); plt.clf();
    plt.subplot(1, 2, 1); plt.plot(S); plt.title('Singular Values')
    plt.xlabel('n'); plt.ylabel('$\sigma_n$')
    plt.subplot(1, 2, 2); plt.semilogy(S); plt.title('Log of Singular Values')
    plt.xlabel('n'); plt.ylabel('$\log(\sigma_n)$')
    plt.show()

    # reconstructing the data with many different number of singular values
    for k in [1, 3, 5, 10, 20, 30, 50, 80, 100, 120, 300, N]:
        plt.figure(2); plt.clf()
        # low-rank SVD reconstruction using k degrees
        img_k = U[:,0:k] @ np.diag(S[0:k]) @ V[0:k,:]
        compression_ratio = (100 * N * k * 2) / (N ** 2)
        # calculating explained variance
        explained_variance = 100 * sum(S[0:k] ** 2) / sum(S ** 2)

        # show the reconstructed image for this k
        plt.imshow(img_k); plt.set_cmap('gray')
        plt.title('Reconstructed Image with k = ' + str(k) +  ', \n' +
                  'Compression Ratio = ' + str(compression_ratio) + ', \n' +
                  'Explained Variance = ' + str(explained_variance))
        plt.show()


# test driver
SVDImgCompression()
