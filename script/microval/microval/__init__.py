"""
Module for plotting experimental and simulative data.
"""

import numpy as np
import matplotlib.pyplot as plt

def scaled_imshow(X, scale_factor = 1.0, offset=[0, 0], invert_axis=False, **kwargs):
    """
    Plotting an image with `matplotlib`'s function `imshow`.
    Allows for scaling and offsetting the image.
    
    Parameters
    ----------
    X : np.array
        Image data to plot with `imshow`.
    scale_factor : float
        optional, scale factor for the image
        default : 1.0
    offset : list
        optional, offset image plotting
        first entry in the list gives x-axis-offset and second the y-axis-offset
        default : [0,0]
    invert_axis : bool
        optional, flips the plot
        default : False
    kwargs
        optional, keyword arguments for `imshow`
    """
    offs = np.array(offset)
    size_x, size_y = X.shape[-2] * scale_factor, X.shape[-1] * scale_factor

    X = X.T
    if invert_axis:
        X = np.flipud(X)

    plt.imshow(X,
               origin='lower',
               extent=[offs[0], offs[0] + size_x, offs[1], offs[1] + size_y],
               **kwargs)
