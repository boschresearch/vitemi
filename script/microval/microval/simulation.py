"""
Plot heatmaps from simulation.
"""

import numpy as np
import microval
import matplotlib.pyplot as plt


class SimulationResult:
    """
    Data structure for simulation data.
    """

    _scale_factor = 1.0
    _x0 = 0
    _y0 = 0

    def __init__(self, file_name):
        """
        Initialize the simulation result data.
        
        Attributes
        ----------
        file_name : string
            path to the exported image file
        """
        self._image_data = plt.imread(file_name)
        self._image_data = np.flipud(self._image_data).T
        self._image_data = self._crop_data(self._image_data)

    def _crop_data(self, data):
        alpha = data[3]
        non_transparent = np.where(alpha)
        imin, imax, jmin, jmax = non_transparent[0].min(), non_transparent[0].max(
        ), non_transparent[1].min(), non_transparent[1].max()
        data = data[:, imin:imax + 1, jmin:jmax + 1]
        return data

    def transform_to(self, region):
        """
        Transform simulation result to a specified region.
        
        Attributes
        ----------
        region : list
            region to transform to
            list or array in the form `[x_min, x_max, y_min, y_max]`
        """
        xmin, dx, ymin, dy = region[0], region[1] - \
            region[0], region[2], region[3] - region[2]
        self._x0, self._y0 = xmin, ymin
        self._scale_factor = dx / self._image_data.shape[1]
        return self

    def flip(self, updown=False, leftright=False):
        """
        Flip the image.
        
        Attributes
        ----------
        updown : bool
            optional, flip up/down
            default : False
        leftright : bool
            optional, flip left/right
            default : False
        """
        if updown:
            self._image_data = np.flip(self._image_data, axis=2)
        if leftright:
            self._image_data = np.flip(self._image_data, axis=1)
        return self

    def imshow(self, region=None, scale_factor=1.0, **kwargs):
        """
        Plot simulation data.
        
        Parameters
        ----------
        region : list or None
            optional, plot only a segement of the data, if value is not `None`
            list or array in the form `[x_min, x_max, y_min, y_max]`
            default : None
        scale_factor : float
            optional, scale factor for `scaled_imshow`
            default : 1.0
        kwargs
            optional, keyword arguments for `scaled_imshow` or `get_segmented_data`
        """
        if region is None:
            offset = [0, 0]
        else:
            offset = [region[0], region[2]]
        offset = [offset[0] + self._x0, offset[1] + self._y0]
        return microval.scaled_imshow(
            self._image_data,
            scale_factor=scale_factor *
            self._scale_factor,
            offset=offset,
            **kwargs)
