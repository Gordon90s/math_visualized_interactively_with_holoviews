import holoviews as hv
import numpy as np
from autograd import grad  # derivative package
hv.extension('bokeh')



# define function f
def f(x):
    return x**2/10.0 - x + 1

# create points
min_x = -10.0
max_x = 12.0
x = np.linspace(min_x, max_x, num = 200)
y = f(x)

# create HoloViews objects
#hv_f = hv.Curve((x, y), 'x', 'y')
hv_f = hv.Curve((x, y))
hv_hline = hv.HLine(0)

# generate plot
hv_f * hv_hline





#------------------------------------------



# optimize plotting ranges to accomodate for coming tangent
range_x = max_x - min_x
range_expand_x = 0.02  # increase x-range by 2%
min_plot_x = min_x - range_x * range_expand_x
max_plot_x = max_x + range_x * range_expand_x

min_y = np.min(y)
max_y = np.max(y)
range_y = max_y - min_y
range_expand_y  = 0.1  # increase y-range by 10%
min_plot_y = min_y - range_y * range_expand_y
max_plot_y = max_y + range_y * range_expand_y

hv_f = hv_f.redim.range(x=(min_plot_x, max_plot_x), y=(min_plot_y, max_plot_y))  # apply changes to figure

# rename axis
hv_f = hv_f.redim(y='f(x)')

# fine tune plot styling
import bokeh.palettes as bp  # import color palettes for beautiful colors
color_palette = 'Inferno'
color_1 = bp.all_palettes[color_palette][256][145]
color_2 = bp.all_palettes[color_palette][256][20]
# plot styling options
styling_options = {'Curve': dict(height=400, width=640, tools=['hover'], toolbar='right', color=color_1, line_width=2.5),
           'HLine': dict(color='grey', line_width=2)}

# generate customized plot
layout_f = hv_f * hv_hline
layout_f = layout_f.options(styling_options)  # add styling options
layout_f







#------------------------------------------



# get derivative
f_prime = grad(f)

# define the tangent to f at x_1
def tangent_f(x, x_1):
    return f_prime(x_1)*(x-x_1) + f(x_1)

# create HoloViews object
def hv_tangent_f(x_1):
    return hv.Curve((x, tangent_f(x, x_1))).options(color = color_2)
# create vertical line
def hv_vline(x_1):
    return hv.VLine(x_1)

# create DynamicMap for tangent
default_x_1 = min_x + range_x*0.2  # default plotting value dynamic map
dmap = hv.DynamicMap(hv_tangent_f, kdims=[hv.Dimension('x_1', range=(min_x, max_x), default=default_x_1)])

# create DynamicMap for vertical line
dmap_vline = hv.DynamicMap(hv_vline, kdims = [hv.Dimension('x_1', range=(min_x, max_x), default=default_x_1)])
opts_vline = {'VLine': dict(color='grey', line_width=0.5, line_dash='dashed')}
dmap_vline = dmap_vline.options(opts_vline)  # add styling options

# generate final function plot + tangent
layout_tangent = layout_f * dmap * dmap_vline
layout_tangent = layout_tangent.redim.range(x = (min_plot_x, max_plot_x), y = (min_plot_y, max_plot_y))
layout_tangent



#------------------------------------------


# how to get from x_n to x_{n+1}
def newton_iteration(x_n):
    return x_n - f(x_n)/f_prime(x_n)

# how to get from x_0 to x_n with all the steps in between
def newton_algo(x_0, n_steps):
    x_n = x_0  # initialize
    xs = [x_0]  # initialize list to store all values x for all n_steps (i.e. number of iterations)
    ys = [f(x_0)]  # same for y
    for i in range(n_steps):
        x_n_plus_1 = newton_iteration(x_n)
        xs.append(x_n_plus_1)
        ys.append(f(x_n_plus_1))
        x_n = x_n_plus_1
    coords = np.zeros((n_steps+1,2))  # create matrix for x values to be saved in first column, y values in 2nd column
    coords[:,0] = xs
    coords[:,1] = ys
    return coords

# define start value and number of iterations n_steps
x_0 = -8.5
n_steps = 6
coords = newton_algo(x_0, n_steps+1)
hv_coords = hv.Points(coords)

# create lists that will contain the HoloViews objects for each step of the Newton Algorithm
hv_tangent_list = []
hv_x_n_list = []
hv_xy_points = []

# plotting style parameters
opts_vline = {'VLine': dict(color='grey', line_dash='dashed', line_width=0.5)}
opts_curve = {'Curve': dict(color=color_2, line_dash='solid', line_width=1.5)}
opts_points = {'Points': dict(marker='o', size=5, color='black')}

# saving the HoloViews objects into the lists
for i in range(n_steps+1):
    hv_curve_newton = hv.Curve((x,tangent_f(x,coords[i,0]))).options(opts_curve)
    hv_tangent_list.append(hv_curve_newton)
    hv_vline_newton = hv.VLine(coords[i,0]).options(opts_vline)
    hv_x_n_list.append(hv_vline_newton)
    hv_points_newton = (hv.Points(coords[i,:].reshape(1,2))*hv.Points((coords[i,0],0))*hv.Points((coords[i+1,0],0))).options(opts_points)
    hv_xy_points.append(hv_points_newton)

# create HoloViews map
dict_steps = {int(steps): hv_tangent_list[steps] * hv_x_n_list[steps] * hv_x_n_list[steps+1]
              * hv_xy_points[steps] for steps in range(n_steps)}
hmap_newton = hv.HoloMap(dict_steps, kdims=['Steps'])

# and plot them together with our previous plots
newton_viz = hmap_newton * layout_f
newton_viz = newton_viz.redim.range(x = (min_plot_x, max_plot_x), y = (min_plot_y, max_plot_y))
newton_viz