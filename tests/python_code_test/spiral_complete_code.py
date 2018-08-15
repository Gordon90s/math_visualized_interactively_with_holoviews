import holoviews as hv
import numpy as np
hv.extension('bokeh')

def spiral_equation(f, ph2):
    r = np.arange(0, 1, 0.005)
    xs, ys = (r * fn(f*np.pi*np.sin(r)+ph2) for fn in (np.cos, np.sin))
    paths = hv.Path([(xs,ys)], extents=(-0.22,-0.22,0.22,0.22))#.options(opts)
    return paths

kdims = [hv.Dimension('f', values = np.arange(1,195,0.1)),
         hv.Dimension('ph2', values = [1,2,3,4,5,6,7,8,9])]

spiral_dmap = hv.DynamicMap(spiral_equation, kdims = kdims)

hmap = spiral_dmap.overlay('ph2')
