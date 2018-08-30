import holoviews as hv
import numpy as np
hv.extension('bokeh')
import bokeh.palettes as bp  # for color palettes



# define function of choice
def fct(x):
    fct_def = np.sin(x/5)
    return fct_def

# and its integral (computed by hand)
def int_fct(x):
    return -5*np.cos(x/5)

# integral for a given interval
def int_fct_ev(x1,x2):
    return int_fct(x2) - int_fct(x1)

x = np.linspace(0,10, num = 201)  # range of x over which to plot x
y = fct(x)




# plot styling
color_palette = 'Inferno'
col_1 = bp.all_palettes[color_palette][256][145]
col_2 = bp.all_palettes[color_palette][256][20]
opts_poly = {'Polygons': dict(color=col_1, width=350, height = 400)}
opts_curve_1 = {'Curve': dict(color= col_2, width=350, height = 400)}
opts_curve_2 = {'Curve': dict(color='red', width=350, height = 400)}
opts_point = {'Points':dict(color='black', marker='+', size=11)}

# create rectangle from starting point with width and height
def hv_rectangle(x=0, y=0, width=.05, height=.05):
    return hv.Polygons([np.array([(x,y), (x+width, y), (x+width, y+height), (x, y+height)])]).options(opts_poly)

# Create curve and integral
hv_curve = hv.Curve((x,y),'x','f(x)').options(opts_curve_1)
hv_int = hv.Area((x,y),'x','f(x)').options(color=col_1) # create integral polygone from input vector x and y





# number of steps to approximate the integral with
n_steps = np.arange(3,30)

# create empty list to store all integral approximations for all n_steps
hv_int_box_approx = []
approx_int = []  # value of approximated integral for all n_steps

# calculate approximation for each step
for j in range(len(n_steps)):
    x_steps = np.linspace(0,10,num=n_steps[j]+1)
    hv_int_box_approx_j = []  # list to store all rectangles for a given n_steps
    approx_int_j = 0.0  # value of approximated integral
    # how to approximate a function using rectangles
    for i in range(n_steps[j]):
        hv_int_box_approx_j.append(hv_rectangle(x=x_steps[i], y=0, width=x_steps[1]-x_steps[0], height=(fct(x_steps[i])+fct(x_steps[i+1]))/2))
        approx_int_j = approx_int_j+(x_steps[1]-x_steps[0])*(fct(x_steps[i])+fct(x_steps[i+1]))/2  # calculate approx integral
    # add all rectangles together and create an ndoverlay
    polygone_dict = {i:hv_int_box_approx_j[i] for i in range(n_steps[j])}
    ndoverlay = hv.NdOverlay(polygone_dict)
    hv_int_box_approx.append(ndoverlay)
    approx_int.append(approx_int_j)

# create dictionary containing the curve approx. for each step and create HoloMap object
polygone_dict = {j:hv_int_box_approx[j] for j in range(len(n_steps))}
hmap_poly = hv.HoloMap(polygone_dict, kdims=['Steps'])

# calculate differences between actual and estimated integral
real_int = int_fct_ev(0,10)  # known value of the integral
int_error = approx_int - real_int  # difference between actual and estimated integral

# create HV objects for error curve
hv_int_error = hv.Curve((n_steps,int_error), 'steps', 'error').options(opts_curve_2)
hv_int_error_points = []

# create hmap for error or error curve
for j in range(len(n_steps)):
    hv_int_error_points.append(hv.Points((n_steps[j],int_error[j])).options(opts_point))
error_points_dict = {j:hv_int_error_points[j] for j in range(len(n_steps))}
hmap_error_points = hv.HoloMap(error_points_dict, kdims=['Steps'])
# create horizontal line at 0
hv_hline = hv.HLine(0).options(color='black',line_width=0.8, line_dash='dashed')

# create layouts
layout_approx_int = (hmap_poly * hv_curve).redim.range(x=(0,10), y = (0,1.08))
layout_error_fct = (hv_int_error * hmap_error_points *hv_hline).redim.range(x=(0,20),y=(-0.28,0.025))
int_approx_viz = (layout_approx_int + layout_error_fct).options(title_format='')