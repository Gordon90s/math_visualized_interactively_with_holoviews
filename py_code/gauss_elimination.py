import holoviews as hv
import numpy as np
import copy
hv.extension('bokeh')




# styling options
cmap = 'RdBu'
scale_factor = 0.69  # to scale images
options = {'Image': dict(cmap = cmap, symmetric=True, colorbar = True, colorbar_opts = {'padding':12}, height = int(420*scale_factor),
                         width = int(480*scale_factor), border = 10, xaxis = None,
                         tools=['hover'], yaxis = None, toolbar='right')}

opts_layout = {'Layout': dict(shared_axes=False, normalize=False, toolbar='left', title_format='')}





# construct a matrix for Gauss algorithm
## step 1: correlation matrix
### function that creates correlation matrices of size d and 'dependence structure influencing' value k
### lower k means higher dependence structure and vice versa
### (already used in Section 'Standard Matrices')
def factor(d,k):
    W = np.random.multivariate_normal(mean = np.zeros(d), cov = np.identity(d), size = k)
    S = W.T @ W + np.diag(np.random.uniform(size = d))
    D = np.diag(1.0/np.sqrt(np.diag(S)))
    S = D @ S @ D
    return S
np.random.seed(3)
n = 15
corr_matrix1 = factor(n,k=10)

## step 2: multiply with a random diagonal matrix
np.random.seed(1)
M_diag_vector = np.random.uniform(0.5,3,size = n)
M_diag = np.diag(M_diag_vector)
M = np.linalg.multi_dot([M_diag,corr_matrix1,M_diag])

## Gauss elimination algorithm without pivot
hv_gauss = []  # create empty list for HV objects
A_k = M  # initialize
L_k = M_k = np.identity(n)
hv_gauss.append((hv.Image(M_k).options(title_format='M_0') + hv.Image(L_k).options(title_format='L_0')\
                + hv.Image(A_k).options(title_format='A = U_0')).options(options).options(opts_layout))
### apply steps in algorithm
for k in range(n-1):
    l_k = np.concatenate([np.zeros(k+1),np.squeeze(np.asarray(A_k[k+1:,k]/A_k[k,k])).reshape(n-k-1,)]) # matrix vs array vs single point... really?
    M_k = np.identity(n) - np.transpose(np.matrix(l_k)) @ np.eye(1,n,k)
    M_k_minus = np.identity(n) + np.transpose(np.matrix(l_k)) @ np.eye(1,n,k)  # inverse of M_k
    A_k = np.matmul(M_k,A_k)
    L_k = np.matmul(L_k,M_k_minus)
    hv_gauss.append((hv.Image(M_k).options(title_format='M_%s' %(k+1)) + hv.Image(L_k).options(title_format='L_%s' %(k+1))\
                     + hv.Image(A_k).options(title_format='U_%s' %(k+1))).options(options).options(opts_layout))

### HoloMap object
dict_gauss = {int(k): hv_gauss[k] for k in range(n)}
gauss_elimination_viz = hv.HoloMap(dict_gauss, kdims = ['Iteration']).collate().cols(2)

