# Create visualization of weekly commit activity over the past year of every Python visualization tool
# presented in [Great Data Visualization Tools for Python](https://www.youtube.com/watch?v=TPl9bMg8j8U)
# (except OpenGL, JavaScript, pandas and graphviz).
# Data fetched and saved on 16/8/2018.

import holoviews as hv
import pandas as pd
import numpy as np
hv.extension('bokeh')

# read data from file
df_big = pd.read_csv("./data/df_python_library_visualization.csv")

# sort data frame with respect to 'total commits' in descending order
df_big = df_big.sort_values(by=['total commits', 'repo'], ascending=False)

# remove columns that are not of interests for the visualization (was too lazy to correctly import the data set...)
df_big = df_big.drop(columns=['total commits', 'Unnamed: 0']).reset_index(drop=True)

# rename 'repo' into 'library'
df_big = df_big.rename(columns={df_big.columns[0]:'library'})

# format to HoloViews data set
hv_dataset = hv.Dataset(df_big, kdims=['week','library'], vdims =
['commits'])

# define plotting options
options = {'HeatMap': dict(width=900, height=500, tools=['hover'], default_tools=['save'],
logz=True, invert_yaxis=False, labelled=[],
                           toolbar='above', xaxis=None, colorbar=True,
cmap='inferno'),
          'Curve': dict(width=900, height=300, yaxis='left', xticks=52, xrotation=90,
line_color='black', framewise=True)}

# create heatmap
hv_heatmap = hv.HeatMap(hv_dataset, label='Repository Activity').options(options)

# declare Tap stream with heatmap as source and initial values
posxy = hv.streams.Tap(source=hv_heatmap, x=26, y='holoviews')

# define function to obtain curve of commmits per week based on library selected by tap on location
def tap_heatmap(x, y):
    return hv.Curve(hv_dataset.select(library=y), kdims='week',
                   label='library: %s' % y)

# create dynamic map
hv_dmap = hv.DynamicMap(tap_heatmap, kdims=[],
streams = [posxy]).options(options)

repo_activity_viz = (hv_heatmap + hv_dmap).cols(1)
