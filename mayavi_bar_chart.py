import numpy
from mayavi.mlab import *

def test_barchart():
    """ Demo the bar chart plot with a 2D array.
    """
    s = numpy.abs(numpy.random.random((3, 3)))
    return barchart(s)
