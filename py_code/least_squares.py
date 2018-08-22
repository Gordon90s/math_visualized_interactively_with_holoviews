# Visualization of the least square algorithm with slope a and offset b

import numpy as np
import holoviews as hv
hv.extension('bokeh')
import bokeh.palettes as bp # for color palettes



# set up model
np.random.seed(22)  # set seed for reproducability
n_points = 10  # number of points for the regression
errors = np.random.normal(scale = 1, size = n_points)
a = 1.0  # slope
b = -3.0  # offset
x = np.linspace(1,n_points,n_points)  # create x vector
y = a*x+b+errors  # simulated data

# define rectangle function to later draw squares
def rectangle(c=0, d=0, width=.05, height=.05):
    return np.array([(c,d), (c-width, d), (c-width, d-height), (c, d-height)])

# calculate estimates for y, error and sum of squared errors
def predictions(a_est=1, b_est=-3):
    y_est = a_est*x+b_est
    error_est = y - y_est
    sum_of_errors_est = sum(error_est**2)
    # first item returns y_est, second item returns error_est, third sum of squared errors
    return np.asarray([y_est,error_est,sum_of_errors_est])

# plot styling options
color_palette = 'PuRd'
col_1 = bp.all_palettes[color_palette][9][1]
col_2 = bp.all_palettes[color_palette][9][2]
col_3 = bp.all_palettes[color_palette][9][2]
options_curve = {'Curve': dict(color='red')}
options_points = {'Points': dict(marker='o', size=8,height=350, width=350)}
options_polygons = {'Polygons': dict(color=col_3)}
# options_dmap = {'DynamicMap': dict(height=350, width=350)}  # not working...

# create HoloViews objects
# simulated data
hv_points = hv.Points((x,y))#.options(options_points) why does that destroy my graphic...?
# it destroys not even the graphic it is involved (?!)
# adding this everywhere does not help either #.redim.range(a_est = (a_est_min, a_est_max), b_est = (b_est_min, b_est_max))

# y=a_est*x+b_est line
def hv_line_est(a_est, b_est):
    hv_curve = hv.Curve((x,predictions(a_est, b_est)[0])).options(options_curve) # squared errors visualized as squares
    hv_curve = hv_curve.relabel("sum_of_squares: {}".format(np.round(predictions(a_est, b_est)[2],2)))  # add sum of squares to graphic # I would like this output not as legend but on top
    return hv_curve
def hv_squares(a_est, b_est):
    hv_polygons = hv.Polygons([{('x', 'y'): rectangle(x, y, w, w)}
             for x, y, w in np.c_[x,y,predictions(a_est, b_est)[1]]]).options(options_polygons)
    return hv_polygons
# create point of coordinate (a_est,b_est)
def hv_point_est(a_est, b_est):
    return hv.Points((a_est,b_est)).options(options_points)

# define estimate ranges and vectors for a_est and b_est
n_est = 100  # number of estimates for each a_est and b_est
a_est_min = 0.7
a_est_max = 1.3
b_est_min = -4.0
b_est_max = -2.0
a_est_vector = np.linspace(a_est_min,a_est_max,n_est)
b_est_vector = np.linspace(b_est_min,b_est_max,n_est)

# create matrix with squared error depending on a_est and b_est in the goal to draw contour lines
matrix = np.zeros((n_est,n_est))
for i in range(n_est):
    for j in range(n_est):
        matrix[i,j] = predictions(a_est_vector[j], b_est_vector[-i-1])[2]  # these are the sum of squares
bounds = (a_est_min,b_est_min,a_est_max,b_est_max)  # bounds for the coming plot
a_est_grid, b_est_grid = np.meshgrid(a_est_vector, b_est_vector)  # create input grid
hv_img = hv.Image(a_est_grid + b_est_grid, ['a estimate','b estimate'], bounds = bounds).options(cmap='PuRd',height=350, width=350)  # initialize plot; hv.Image content is added in next line
hv_img.data = matrix  # overwrite data with data we want
contour_levels=50
cmap_custom = hv.plotting.util.polylinear_gradient(['#000000', '#000000'], 20)  # color map in only black
hv_contours = hv_img * hv.operation.contours(hv_img, levels=contour_levels).options(show_legend=False, cmap=cmap_custom)

# set up dimensions for kdims for coming dynamic maps
dim_a_est = hv.Dimension('a_est', range=(a_est_min, a_est_max), default=1)
dim_b_est = hv.Dimension('b_est', range=(b_est_min, b_est_max), default=-3.0)

# dynamic maps
dmap_coords_a_b_est = hv.DynamicMap(hv_point_est, kdims=[dim_a_est,dim_b_est])
dmap_squares = hv.DynamicMap(hv_squares, kdims=[dim_a_est,dim_b_est]).options(height=350, width=350)  #options(options_dmap) # why does this not work?
dmap_line_est = hv.DynamicMap(hv_line_est, kdims=[dim_a_est,dim_b_est])
ls_layout = (dmap_squares * dmap_line_est * hv_points).redim.range(x=(0,11.5), y=(-2.5,7.8))

# generate layouts
contour_layout = hv_contours * dmap_coords_a_b_est
least_square_viz = (ls_layout + contour_layout)
least_square_viz

# visualize only points with fitted line
hv_points_viz = hv_points.options(height=400,width=700).redim.range(x=(0,11), y=(-2.5,7.5))
hv_points_viz *= hv_line_est(a,b).options(color='red')
hv_points_viz