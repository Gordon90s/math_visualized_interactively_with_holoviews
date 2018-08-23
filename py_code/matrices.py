# visualize matrices with colormaps

import holoviews as hv
from holoviews import Image, HoloMap, DynamicMap
import numpy as np
from numpy import linalg as LA
from numpy import random, array, linspace
import scipy
from scipy import linalg
from scipy.linalg import hilbert, tri
import copy
hv.extension('bokeh')






# styling options
cmap = 'blues'
scale_factor = 0.73  # to scale images
options = {'Image': dict(cmap = cmap, colorbar = True, colorbar_opts = {'padding':12}, height = int(380*scale_factor),
                         width = int(440*scale_factor), border = 10, xaxis = 'bottom-bare', yaxis = 'left-bare', toolbar=None)}

opts_layout = {'Layout': dict(shared_datasource=False, normalize=False, toolbar=None)}

# set up matrix size
n = 25

# visualize identity matrix
unit_matrix = np.identity(n)
hv_unit_matrix = hv.Image(unit_matrix).options(options)


# create function that returns banded matrix
def band_matrix_fct(n, value_diag, band_a):
    band_matrix = np.zeros((n, n))
    band_matrix[np.arange(n - 1), np.arange(n - 1) + 1] = np.repeat(band_a, n - 1)
    band_matrix[np.arange(n), np.arange(n)] = np.repeat(value_diag, n)
    band_matrix[np.arange(n), np.arange(n) - 1] = np.repeat(band_a, n)
    band_matrix[n - 1, 0] = band_a
    return band_matrix


# draw banded block matrix
options_divergence = copy.deepcopy(options)
options_divergence['Image']['cmap'] = 'RdBu'
options_divergence['Image']['symmetric'] = True

n = 5
value_diag = 4
band_a = -1
band_block_matrix = np.zeros((n ** 2, n ** 2))  # init
for i in range(n):
    band_block_matrix[i * n:(i + 1) * n, i * n:(i + 1) * n] = band_matrix_fct(n, value_diag, band_a)
for i in range(n - 1):
    band_block_matrix[(i + 1) * n:(i + 2) * n, i * n:(i + 1) * n] = -np.identity(n)
    band_block_matrix[i * n:(i + 1) * n, (i + 1) * n:(i + 2) * n] = -np.identity(n)

hv_band_block_matrix = hv.Image(band_block_matrix).options(options_divergence)



# triangular matrix
n = 25
matrix = np.random.random((n,n))
matrix_tril = np.tril(matrix)
hv_matrix_tril = hv.Image(matrix_tril).options(options)


# create layout of first 3 matrices
standard_matrices_viz = (hv_unit_matrix + hv_band_block_matrix + hv_matrix_tril).options(opts_layout)





