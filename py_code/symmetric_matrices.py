# Determine if a matrix is symmetric

import holoviews as hv
import numpy as np
import copy
hv.extension('bokeh')



# styling options
cmap = 'blues'
scale_factor = 0.69  # to scale images
options = {'Image': dict(cmap = cmap, colorbar = True, colorbar_opts = {'padding':12}, height = int(380*scale_factor),
                         width = int(440*scale_factor), border = 10, xaxis = None,
                         tools=['hover'], yaxis = None, toolbar='right')}

opts_layout = {'Layout': dict(shared_axes=False, normalize=False, toolbar='right')}





# generate symmetric matrix
options_sym = copy.deepcopy(options)
options_sym["Image"]['width'] = 490
options_sym["Image"]['height'] = 430
options_sym["Image"]['cmap'] = 'blues'
#options_sym["Image"]['symmetric'] = True

n = 40
np.random.seed(2)
matrix = np.random.random((n,n))  # generates values between 0 and 1
matrix_tril = np.tril(matrix,0)  # extract lower triangular matrix
matrix_triu = matrix_tril.T  # transpose lower triangular matrix

matrix_sym = matrix_tril + matrix_triu  # create symmetric matrix, not that this doubles the values on the diagonal
matrix_sym_viz = hv.Image(matrix_sym).options(options_sym)


# symmetric matrices with noise
np.random.seed(2)

## example 1, randomly change 100 entries
matrix_sym_1 = matrix_sym + 0
n_values_to_change = 100
for i in range(n_values_to_change):
    matrix_sym_1[np.random.randint(0,n),np.random.randint(0,n)] += np.random.normal(0,0.15)
hv_matrix_sym_1 = hv.Image(matrix_sym_1).options(options).options(title_format='Example 1 (random replacements)')  

## example 2, add a small amount of noise to all entries
matrix_sym_2 = matrix_sym + np.random.normal(0,0.02, size=(n,n))
hv_matrix_sym_2 = hv.Image(matrix_sym_2).options(options).options(title_format='Example 2 (low random noise)')

## example 3, add a larger amount of noise to all entries
matrix_sym_3 = matrix_sym + np.random.normal(0,0.12, size=(n,n))
hv_matrix_sym_3 = hv.Image(matrix_sym_3).options(options).options(title_format='Example 3 (heigh random noise)')

## create layout
matrix_sym_examples_viz = (hv_matrix_sym_1 + hv_matrix_sym_2 + hv_matrix_sym_3).options(title_format='Matrix representation').options(opts_layout)


# plot absolut differences between lower and upper matrix for each example

options_sym_div = copy.deepcopy(options)
options_sym_div["Image"]['cmap'] = 'RdBu'
options_sym_div["Image"]['symmetric'] = True

## example 1
diff_matrix_sym_1 = abs(np.tril(matrix_sym_1, 0) - np.triu(matrix_sym_1, 0).T)
hv_diff_matrix_sym_1 = hv.Image(diff_matrix_sym_1).options(options_sym_div).options(
    title_format='Example 1 (random replacements)')

## example 2
diff_matrix_sym_2 = abs(np.tril(matrix_sym_2, 0) - np.triu(matrix_sym_2, 0).T)
hv_diff_matrix_sym_2 = hv.Image(diff_matrix_sym_2).options(options_sym_div).options(
    title_format='Example 2 (low random noise)')

## example 3
diff_matrix_sym_3 = abs(np.tril(matrix_sym_3, 0) - np.triu(matrix_sym_3, 0).T)
hv_diff_matrix_sym_3 = hv.Image(diff_matrix_sym_3).options(options_sym_div).options(
    title_format='Example 3 (heigh random noise)')

## create layout
diff_viz = (hv_diff_matrix_sym_1 + hv_diff_matrix_sym_2 + hv_diff_matrix_sym_3).options(
    title_format='Absolute differences').options(opts_layout)



# adjust colormaps to matrix range ex-diagonals

max_ex_1 = np.max(matrix_sym_1[0, 2])  # example 1
min_ex_1 = np.min(matrix_sym_1[0, 2])
max_ex_2 = np.max(matrix_sym_2[0, 2])  # example 2
min_ex_2 = np.min(matrix_sym_2[0, 2])
max_ex_3 = np.max(matrix_sym_3[0, 2])  # example 3
min_ex_3 = np.min(matrix_sym_3[0, 2])
for i in range(n):
    for j in range(n):
        if i != j:
            max_ex_1 = np.max([matrix_sym_1[i, j], max_ex_1])  # example 1
            min_ex_1 = np.min([matrix_sym_1[i, j], min_ex_1])
            max_ex_2 = np.max([matrix_sym_2[i, j], max_ex_2])  # example 2
            min_ex_2 = np.min([matrix_sym_2[i, j], min_ex_2])
            max_ex_3 = np.max([matrix_sym_3[i, j], max_ex_3])  # example 3
            min_ex_3 = np.min([matrix_sym_3[i, j], min_ex_3])

hv_diff_matrix_sym_1 = hv_diff_matrix_sym_1.redim.range(z=(min_ex_1, max_ex_1))  # example 1
hv_diff_matrix_sym_2 = hv_diff_matrix_sym_2.redim.range(z=(min_ex_2, max_ex_2))  # example 2
hv_diff_matrix_sym_3 = hv_diff_matrix_sym_3.redim.range(z=(min_ex_3, max_ex_3))  # example 3
## layout
diff_new_cmap_viz = (hv_diff_matrix_sym_1 + hv_diff_matrix_sym_2 + hv_diff_matrix_sym_3).options(
    title_format='Absolute differences with relative colormap').options(opts_layout)

# divide lower triangular matrix by upper triangular matrix

ratio_matrix_sym_1 = np.zeros((n, n))  # example 1
ratio_matrix_sym_2 = np.zeros((n, n))  # example 2
ratio_matrix_sym_3 = np.zeros((n, n))  # example 3
for i in range(n):
    for j in range(n):
        if i > j:
            ratio_matrix_sym_1[i, j] = np.tril(matrix_sym_1, -1)[i, j] / np.triu(matrix_sym_1, 1).T[
                i, j] - 1  # example 1
            ratio_matrix_sym_2[i, j] = np.tril(matrix_sym_2, -1)[i, j] / np.triu(matrix_sym_2, 1).T[
                i, j] - 1  # example 2
            ratio_matrix_sym_3[i, j] = np.tril(matrix_sym_3, -1)[i, j] / np.triu(matrix_sym_3, 1).T[
                i, j] - 1  # example 3

hv_ratio_matrix_sym_1 = hv.Image(ratio_matrix_sym_1).options(options_sym_div).options(
    title_format='Example 1 (random replacements)')
hv_ratio_matrix_sym_2 = hv.Image(ratio_matrix_sym_2).options(options_sym_div).options(
    title_format='Example 2 (low random noise)')
hv_ratio_matrix_sym_3 = hv.Image(ratio_matrix_sym_3).options(options_sym_div).options(
    title_format='Example 3 (heigh random noise)')
## layout
ratio_viz = (hv_ratio_matrix_sym_1 + hv_ratio_matrix_sym_2 + hv_ratio_matrix_sym_3).options(
    title_format='Relative differences').options(opts_layout)





# clip the colormap at certain thresholds to show more nuances visualization

hv_ratio_matrix_sym_1 = hv_ratio_matrix_sym_1.redim.range(z=(-4,4))
hv_ratio_matrix_sym_2 = hv_ratio_matrix_sym_2.redim.range(z=(-1,1))
hv_ratio_matrix_sym_3 = hv_ratio_matrix_sym_3.redim.range(z=(-4,4))

ratio_new_cmap_viz = (hv_ratio_matrix_sym_1 + hv_ratio_matrix_sym_2 + hv_ratio_matrix_sym_3).options(title_format='Relative differences with adjusted colormap').options(opts_layout)
 



