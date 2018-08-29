# superpose two matrix visualizations into one image

import holoviews as hv
import numpy as np
import scipy
from scipy.linalg import dft
hv.extension('bokeh')




# styling options
scale_factor = 0.69  # to scale images
options = {'RGB': dict(height = int(480*scale_factor),
                         width = int(440*scale_factor), border = 10, xaxis = None,
                         tools=['hover'], yaxis = None, toolbar='right')}
opts_layout = {'Layout': dict(toolbar='right')}

# generate and plot complex discrete fourier transform (dft) matrix
n=50  # matrix size
fourier_transform_real = (np.real(dft(n))+1)/2  # normalize to values between 0 and 1
zeros = np.zeros((n,n))
matrix_1 = zeros + 1  # creating matrix with all entries equal to 1
fourier_transform_imag = (np.imag(dft(n))+1)/2  # normalize values

# RGB color mixing
## by using the red channel, colors go from black RBG(0,0,0) to red RBG(1,0,0)
hv_real_red = hv.RGB(np.dstack([fourier_transform_real,zeros,zeros]))  # real part in red
hv_real_red = hv_real_red.options(options).options(title_format = 'Real part')
hv.RGB(np.dstack([fourier_transform_real,zeros,zeros])) # only reds
## by using the blue channel, colors go from black RBG(0,0,0) to red RBG(0,0,1)
hv_imag_blue = hv.RGB(np.dstack([zeros,zeros,fourier_transform_imag]))  # img part in blue
hv_imag_blue = hv_imag_blue.options(options).options(title_format = 'Imaginary part')
hv.RGB(np.dstack([zeros,zeros,fourier_transform_imag]))  # only blues
## superpose red and blue image
hv_mixed_rgb = hv.RGB(np.dstack([fourier_transform_real,zeros,fourier_transform_imag]))  # mixing red and blues
hv_mixed_rgb = hv_mixed_rgb.options(options).options(title_format = 'Real + imaginary part')
hv.RGB(np.dstack([fourier_transform_real,zeros,fourier_transform_imag]))
## create layout
complex_matrix_viz = (hv_real_red + hv_imag_blue + hv_mixed_rgb).options(opts_layout)