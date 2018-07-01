import numpy as np
import holoviews as hv

from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import Slider, Button

renderer = hv.renderer('bokeh')

def spiral_equation(f, ph2):
    r = np.arange(0, 1, 0.005)
    xs, ys = (r * fn(f*np.pi*np.sin(r)+ph2) for fn in (np.cos, np.sin))
    paths = hv.Path([(xs,ys)], extents=(-0.22,-0.22,0.22,0.22))
    return paths

kdims = [hv.Dimension('f', values = np.arange(1,200,1)),
         hv.Dimension('ph2', values = [1,2,3,4,5,6,7,8,9])]

spiral_dmap = hv.DynamicMap(spiral_equation, kdims = kdims)

hmap = spiral_dmap.overlay('ph2')

start = 1
end = 200

# Convert the HoloViews object into a plot
plot = renderer.get_plot(hmap)

def animate_update():
    year = slider.value + 1
    if year > end:
        year = start
    slider.value = year

def slider_update(attrname, old, new):
    plot.update(slider.value)

slider = Slider(start=start, end=end, value=0, step=1, title="Year")
slider.on_change('value', slider_update)

def animate():
    if button.label == '► Play':
        button.label = '❚❚ Pause'
        curdoc().add_periodic_callback(animate_update, 3)
    else:
        button.label = '► Play'
        curdoc().remove_periodic_callback(animate_update)

button = Button(label='► Play', width=60)
button.on_click(animate)

# Combine the bokeh plot on plot.state with the widgets
layout = layout([
    [plot.state],
    [slider, button],
], sizing_mode='fixed')

curdoc().add_root(layout)
