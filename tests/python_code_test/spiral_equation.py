import holoviews as hv
from holoviews import Store
import numpy as np
hv.extension('bokeh')

renderer = hv.renderer('bokeh')


def spiral_equation(f, ph2):
    r = np.arange(0, 1, 0.005)
    xs, ys = (r * fn(f*np.pi*np.sin(r)+ph2) for fn in (np.cos, np.sin))
    paths = hv.Path([(xs,ys)], extents=(-0.22,-0.22,0.22,0.22))
    return paths
