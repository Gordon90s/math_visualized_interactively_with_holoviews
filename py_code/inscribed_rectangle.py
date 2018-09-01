# visualize a step in a possible proof of the inscribed rectangle problem

import holoviews as hv
import numpy as np
import bokeh.palettes as bp  # for color palettes
import pandas as pd
hv.extension('bokeh')

# read loop data
loop = pd.read_csv("data/inscribed_rectangle.csv", names=['x', 'y'])

# set up data
len_loop = loop.values.shape[0]
x = loop.values[:, 0]
y = loop.values[:, 1]
lin = range(len_loop)

# styling options
## colors
color_palette = 'Inferno'
col_rect = bp.all_palettes[color_palette][256][135]
col_path_1 = bp.all_palettes[color_palette][256][145]
col_path_2 = bp.all_palettes[color_palette][256][185]
## options
opts_poly = {'Polygons': dict(line_width=1.5, color='white', xaxis=None, yaxis=None, show_frame=False)}
opts_rectangle = dict(color=col_rect, fill_alpha=0.8)
opts_point_1 = {'Points': dict(color=col_path_1, size=6.0)}
opts_point_2 = {'Points': dict(color=col_path_2, size=6.0)}
opts_path_1 = {'Path': dict(color=col_path_1, line_width=3)}
opts_path_2 = {'Path': dict(color=col_path_2, line_width=3)}

## create HV loop object
hv_loop = hv.Polygons((x, y)).options(opts_poly).redim.range(x=(50, 1250), y=(75, 1150))


# create polygons and paths
def hv_polygons(a, b, c, d):
    return hv.Polygons([np.c_[loop.values[a, :], loop.values[b, :], loop.values[c, :], loop.values[d, :]].T]).options(
        **opts_rectangle)


def hv_paths(a, b, c, d):
    diag_1 = hv.Path([np.c_[loop.values[a, :], loop.values[c, :]].T]).options(opts_path_1)
    diag_2 = hv.Path([np.c_[loop.values[b, :], loop.values[d, :]].T]).options(opts_path_2)
    point_1 = ((loop.values[a, :] + loop.values[c, :]) / 2)
    point_2 = ((loop.values[b, :] + loop.values[d, :]) / 2)
    diag_1_point = hv.Points((point_1[0], point_1[1])).options(opts_point_1)
    diag_2_point = hv.Points((point_2[0], point_2[1])).options(opts_point_2)
    return diag_1 * diag_2 * diag_1_point * diag_2_point


# set up dimensions
a_dim = hv.Dimension(('a', 'a'), default=310)
b_dim = hv.Dimension(('b', 'b'), default=402)
c_dim = hv.Dimension(('c', 'c'), default=82)
d_dim = hv.Dimension(('d', 'd'), default=187)

# create dynamic maps
dmap_polygons = hv.DynamicMap(hv_polygons, kdims=[a_dim, b_dim, c_dim, d_dim])
dmap_polygons = dmap_polygons.redim.range(a=(0, len_loop - 1), b=(0, len_loop - 1), c=(0, len_loop - 1),
                                          d=(0, len_loop - 1))
dmap_diags = hv.DynamicMap(hv_paths, kdims=[a_dim, b_dim, c_dim, d_dim])
dmap_diags = dmap_diags.redim.range(a=(0, len_loop - 1), b=(0, len_loop - 1), c=(0, len_loop - 1), d=(0, len_loop - 1))

# create layout
inscribed_rectangle_viz = (hv_loop * dmap_polygons + hv_loop * dmap_diags).options(title_format='')
