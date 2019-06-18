import matplotlib.pyplot as plt
import numpy as np

pepper_image = plt.imread('Fig0508(a)(circuit-board-pepper-prob-pt1).tif')
gauss_image = plt.imread('Fig0507(b)(ckt-board-gauss-var-400).tif')


def plot_image(image1, image2):
    fig, ax = plt.subplots(1,2)
    ax[0].imshow(image1, cmap='gray')
    ax[0].set_title('Orginal Image')
    ax[1].imshow(image2, cmap = 'gray')
    ax[1].set_title('Filtered image')
    plt.tight_layout()
    plt.show()

def alpha_trimmed_mean(image, d, boxsize=3):
    padded_image = np.pad(image, (0, boxsize), mode='symmetric')
    result = np.zeros(image.shape)
    rows, cols = image.shape

    for row in range((rows)):
        for col in range((cols)):
            sorted_vals = sorted(padded_image[row:row + boxsize, col:col + boxsize].flatten(), reverse=True)
            sorted_len = len(sorted_vals)
            sorted_vals_cut = sorted_vals[int(d / 2): int(sorted_len - d / 2)]
            result[row, col] = np.sum(sorted_vals_cut) // (sorted_len - d)
    return result.astype('uint8')

alpha_gauss = alpha_trimmed_mean(gauss_image, d = 2, boxsize= 3)

import scipy.misc
scipy.misc.imsave('out_alpha_trimmed_mean.jpg', alpha_gauss)

plot_image(gauss_image,alpha_gauss)