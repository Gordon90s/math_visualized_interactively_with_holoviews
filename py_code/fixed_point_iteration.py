# visualize conditions for which a fix-point exists or not for a linear function

import holoviews as hv
import numpy as np
hv.extension('bokeh')
import bokeh.palettes as bp  # for color palettes


# Define line a*x+b
n = 201
a = 0.8  # slope
b = 2  # offset
x = np.linspace(0,25,n)
def fct(a,x,b):
    return a*(x-2)+b
y = fct(a,x,b)


# styling options
color_palette = 'Inferno'
col_1 = bp.all_palettes[color_palette][256][145]
col_2 = bp.all_palettes[color_palette][256][20]
opts_line_x_x = {'Curve':dict(color='black',line_width=0.8, line_dash='dashed', width=600, height=390)}
opts_curve = {'Curve':dict(color=col_1, width=600, height=390)}

# create HV object for a*x + b together and line y = x
hv_curve = hv.Curve((x,y),'x','y').options(opts_curve)
hv_curve_xx = hv.Curve((x,x)).options(opts_line_x_x)




# create HoloMap object with varying slope
n_a = 20 # number of slope changes
lower_slope_limit = 0.4
upper_slope_limit = 1.2

# let a vary between lower and upper_slope_limit
a_var = np.linspace(lower_slope_limit,upper_slope_limit,n_a)
y_list = []
for i in range(n_a):
    y_list.append(hv.Curve((x,fct(a_var[i],x,b))).options(opts_curve))
# create HoloMap object
dict_y = {i:y_list[i] for i in range(n_a)}
hmap_y = hv.HoloMap(dict_y, kdims = ['a'])

# Find fixpoint (if it exists, which it doesn't if a >= 1)
x_0 = 8.0  # starting value
n_steps = 7
steps = range(0, n_steps)
hv_path_list = []
for i in range(n_a):
    hv_path_list_j = []
    x_n = x_0
    path = []
    for j in steps:
        y_n = fct(a_var[i], x_n, b)
        x_n_1 = y_n
        path = path + [(x_n, 0), (x_n, x_n), (x_n, y_n), (x_n_1, y_n)]
        hv_path_list_j.append(hv.Path([path]).options(color=col_2))
        x_n = x_n_1
    hv_path_list.append(hv_path_list_j)

dict_path = {(i, j): hv_path_list[i][j] for i in range(n_a) for j in steps}
hmap_path = hv.HoloMap(dict_path, kdims=[hv.Dimension(('a', 'a'), default=8), 'step']).options(title_format='')
fix_point_viz = hmap_y * hv_curve_xx * hmap_path
fix_point_viz_1 = fix_point_viz.redim.range(x=(0, 9), y=(0, 9))
fix_point_viz_2 = fix_point_viz


