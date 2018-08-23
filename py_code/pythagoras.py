# Pythagoras a^2 + b^2 = c^2 visual proof

import holoviews as hv
from holoviews import Image, HoloMap, DynamicMap, Polygons, Text
import numpy as np
from numpy import array
hv.extension('bokeh')
import bokeh.palettes as bp  # for color palettes

# define function that returns coordinates of rectangle and line
def rectangle(x=0, y=0, width=.05, height=.05):
    return array([(x, y), (x + width, y), (x + width, y + height), (x, y + height)])
def line(x=0, y=0, width=.05, height=.05):
    return array([(x, y), (x + width, y + height)])

# choose color for plotting
color_palette = 'Inferno'
col_sq_1 = bp.all_palettes[color_palette][256][20]
col_sq_2 = bp.all_palettes[color_palette][256][20]
col_sq_3 = bp.all_palettes[color_palette][256][20]
col_rect = bp.all_palettes[color_palette][256][145]

# options for plot styling
opts = {'Polygons': dict(toolbar=None, xaxis=None, yaxis=None, width=355, height=380, line_width=1.5, show_frame=False)}

# left part of the visual proof, squares of area a^2 and b^2 + 4 triangles of area a*b/2
def square_left(a=1):
    # we set a + b = 100 then convert to a + b = 1
    a = a / 100.0
    b = 1.0 - a
    poly_1 = Polygons([rectangle(a, b, b, a), rectangle(0, 0, a, b)]).options(color=col_rect)
    poly_2 = Polygons([rectangle(0, b, a, a), rectangle(a, 0, b, b)]).options(color=col_sq_1)
    poly_3 = Polygons([line(0, 0, a, b), line(a, b, b, a)])
    text_1 = [
        (a / 2, -0.05, 'a'), (-0.05, b / 2, 'b'),
        (a / 2, 1.05, 'a'), (1.05, b / 2, 'b'),
        (a + b / 2, -0.05, 'b'), (-0.05, b + a / 2, 'a'),
        (a + b / 2, 1.05, 'b'), (1.05, b + a / 2, 'a'),
        (a / 2.5, (b + 0.1 / a) / 2.5, 'c'),
        (a + (b - 0.082 / a) / 2, b + a / 2, 'c')
    ]
    text_2 = [
        (a / 2, b + a / 2, 'a\u00b2'), (a + b / 2, b / 2, 'b\u00b2')
    ]
    output = (poly_1 * poly_2 * poly_3 * hv.Labels(text_1) * hv.Labels(text_2).options(text_color='white')).options(opts)
    output = output.relabel("a\u00b2: {}".format(np.round((a)*100)**2), "b\u00b2: {}".format(np.round((1-a)*100)**2))
    return output

# right part of the visual proof, squares of area c^2 + 4 triangles of area a*b/2
def square_right(a=1):
    a = a / 100.0
    b = 1.0 - a

    poly_5 = Polygons([rectangle(0, 0, a + b, b + a)]).options(color=col_rect)
    poly_6 = Polygons([array([[a, 0], [a + b, a], [b, b + a], [0, b], [a, 0]])]).options(color=col_sq_3)
    text_1 = [
        (a / 2, -0.05, 'a'), (-0.05, b / 2, 'b'),
        (b / 2, 1.05, 'b'), (1.05, a / 2, 'a'),
        (a + b / 2, -0.05, 'b'), (-0.05, b + a / 2, 'a'),
        (b + a / 2, 1.05, 'a'), (1.05, a + b / 2, 'b')
    ]
    text_2 = Text((b + a) / 2, (b + a) / 2, 'c\u00b2').options(color='white')
    output = (poly_5 * poly_6 * hv.Labels(text_1) * text_2).options(opts)
    output = output.relabel("c\u00b2: {}".format(np.round((a)*100)**2+np.round((1-a)*100)**2))
    return output

# create dynamic maps of square_left and square_right
dmap_left = DynamicMap(square_left, kdims=['a'])
dmap_right = DynamicMap(square_right, kdims=['a'])

# and plot together
range_a = (20, 80)

pythagoras_viz = (dmap_left.redim.range(a=range_a) + dmap_right.redim.range(a=range_a))
pythagoras_viz = pythagoras_viz.options(toolbar=None).redim.range(x=(-0.1, 1.1), y=(-0.1, 1.1))
pythagoras_viz = pythagoras_viz
pythagoras_viz