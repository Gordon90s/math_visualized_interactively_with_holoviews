# display 4 uniform sequential and 4 diverging colormaps

import numpy as np
import holoviews as hv
hv.extension('bokeh')
from holoviews.plotting.util import process_cmap
import bokeh.palettes as bp # for color palettes





colormaps = hv.plotting.list_cmaps()
spacing = np.linspace(0, 1, 256)[np.newaxis]  # get 256 colors

# fetch colormaps by category
def filter_cmaps(category):
    return hv.plotting.util.list_cmaps(records=True,category=category,reverse=False)
# styling options
opts = {'Image': dict(height=80, width=280,xaxis=None, yaxis=None, toolbar=None, border=14, show_frame=False)}

# create a plot of 4 uniform sequential colormaps
cms = filter_cmaps('Uniform Sequential')
cms = list(cms[i] for i in [0,6,12,20])  # select 4 specific colormaps

hv_cmap = [hv.Image(spacing, ydensity=1, label="{0}".format(r.name)).options(cmap=process_cmap(r.name))\
            .options(opts) for r in cms]
cmap_seq_viz = (hv_cmap[0] + hv_cmap[1] + hv_cmap[2] + hv_cmap[3]).cols(2).options(toolbar=None)





# create a plot of 4 diverging colormaps
cms = filter_cmaps('Diverging')
cms = list(cms[i] for i in [4,8,14,23])

hv_cmap = [hv.Image(spacing, ydensity=1, label="{0}".format(r.name)).options(cmap=process_cmap(r.name))\
            .options(opts) for r in cms]
cmap_div_viz = (hv_cmap[0] + hv_cmap[1] + hv_cmap[2] + hv_cmap[3]).cols(2).options(toolbar=None)
