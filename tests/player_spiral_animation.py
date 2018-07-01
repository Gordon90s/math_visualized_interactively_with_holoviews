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

# Declare the HoloViews object
start = 1
end = 1000
hmap = hv.HoloMap({i: spiral_equation(i/5,1) for i in range(start, end+1)})

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
