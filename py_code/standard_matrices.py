# visualize different matrices with colormaps

import holoviews as hv
import numpy as np
import copy
hv.extension('bokeh')


# styling options
cmap = 'blues'
scale_factor = 0.73  # to scale images
options = {'Image': dict(cmap = cmap, colorbar = True, colorbar_opts = {'padding':12}, height = int(380*scale_factor), 
                         width = int(440*scale_factor), border = 10, xaxis = None,
                         tools=['hover'], yaxis = None, toolbar='above')}

opts_layout = {'Layout': dict(shared_axes=False, normalize=False)}

# visualize standard matrices
## generate identity matrix
n = 25  # set up matrix size
unit_matrix = np.identity(n)
hv_unit_matrix = hv.Image(unit_matrix).options(options)

## generate band matrices
### create function that returns banded matrix
def band_matrix_fct(n,value_diag,band_a):
    band_matrix = np.zeros((n,n))
    band_matrix[np.arange(n-1), np.arange(n-1)+1] = np.repeat(band_a,n-1)
    band_matrix[np.arange(n), np.arange(n)] = np.repeat(value_diag,n)
    band_matrix[np.arange(n), np.arange(n)-1] = np.repeat(band_a,n)
    band_matrix[n-1,0] = band_a
    return band_matrix


### styling options
options_divergence = copy.deepcopy(options)
options_divergence['Image']['cmap'] = 'RdBu'
options_divergence['Image']['symmetric'] = True

### generate matrix
n = 5
value_diag = 4
band_a = -1
band_block_matrix = np.zeros((n**2,n**2))  # init
for i in range(n):
    band_block_matrix[i*n:(i+1)*n,i*n:(i+1)*n] = band_matrix_fct(n,value_diag,band_a)
for i in range(n-1): 
    band_block_matrix[(i+1)*n:(i+2)*n,i*n:(i+1)*n] = -np.identity(n)
    band_block_matrix[i*n:(i+1)*n,(i+1)*n:(i+2)*n] = -np.identity(n)
hv_band_block_matrix = hv.Image(band_block_matrix).options(options_divergence) 

## generate triangular matrix
n = 25
matrix = np.random.random((n,n))  # generates values between 0 and 1
matrix_tril = np.tril(matrix)  # extract lower triangular matrix
hv_matrix_tril = hv.Image(matrix_tril).options(options)

## create layout with the 3 matrices
standard_matrices_viz = (hv_unit_matrix + hv_band_block_matrix + hv_matrix_tril).options(opts_layout)


#---------------------------------------------------------------------------

# generate two correlation matrices + one with missing values
## correlation matrices using multivariate normal random variables
### function that creates correlation matrices of size d and 'dependence structure influencing' value k
### lower k means higher dependence structure and vice versa
def factor(d,k):
    W = np.random.multivariate_normal(mean = np.zeros(d), cov = np.identity(d), size = k)
    S = W.T @ W + np.diag(np.random.uniform(size = d))
    D = np.diag(1.0/np.sqrt(np.diag(S)))
    S = D @ S @ D
    return S

n = 40
np.random.seed(2)

### generate matrices with difference dependence structure
corr_matrix1 = factor(n,k=1)
corr_matrix2 = factor(n,k=4)

### tweak options to remove colorbar of the left plot & change colormap
options_corr = copy.deepcopy(options_divergence)
options_corr["Image"]['cmap'] = 'bwr_r'
options_left = copy.deepcopy(options_corr)
options_left["Image"]['colorbar'] = False
options_left["Image"]['width'] = int(440*scale_factor*0.86)

### generate HV objects
hv_corr_matrix1 = hv.Image(corr_matrix1).options(options_left)
hv_corr_matrix2 = hv.Image(corr_matrix2).options(options_corr)
hv_corr_matrix_layout = (hv_corr_matrix1 + hv_corr_matrix2)


## matrix with missing values
### generate random matrix (entries are from independenet uniform random variables between 0 and 1)
np.random.seed(2)
matrix_miss = np.random.random((n,n))
### remove some values
nb_missing_values = 100
for i in range(nb_missing_values):
    matrix_miss[np.random.randint(0,n),np.random.randint(0,n)] = np.nan
### generate HV object    
hv_matrix_miss = hv.Image(matrix_miss).options(options).options(clipping_colors = {'NaN':'lime'})


## generate layout of correlation matrices and matrix with missing values
corr_and_missing_viz = (hv_corr_matrix_layout + hv_matrix_miss).options(opts_layout)



#---------------------------------------------------------------------------


# generate large matrix with strong dependence structure
n = 500
np.random.seed(2)

options_corr3 = copy.deepcopy(options_corr)
options_corr3["Image"]['width'] = 750
options_corr3["Image"]['height'] = 700

corr_matrix3 = factor(n,k=1)
matrix_corr_big_viz = hv.Image(corr_matrix3).options(options_corr3)


