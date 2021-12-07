"""
Plotting experimental data.
"""

import numpy as np
import h5py
import microval


class ImageData:
    """
    Abstract class for image data.
    """
    def _clip_data(self, data_arr, region):
        sel_x, sel_y = range(region[0], region[1] -
                             1), range(region[2], region[3] - 1)
        data_arr = data_arr[np.array(sel_x, dtype=int)[
            :, None], np.array(sel_y, dtype=int)[None, :]]
        return data_arr


class TimeSeriesData(ImageData):
    """
    Abstract class for time series data from a `mat`m file.
    
    Attributes
    ----------
    fatigue_data_key : string
        key for accessing the data in the `mat` file
    fatigue_data
        data of the `mat` file
    """
    fatigue_data_key = "FatigueDataStruct"

    def __init__(self, fatiguedata_mat_file_name):
        """
        Initialize the `TimeSeriesData`.
        
        Parameters
        ----------
        fatiguedata_mat_file_name : string
            path to the mat file to read data from
        """
        self._fatigue_mat_data = self._get_mat_file_contents(fatiguedata_mat_file_name)
        self.fatigue_data = self._fatigue_mat_data[self.fatigue_data_key]

    def _get_mat_file_contents(self, mat_file_name):
        return h5py.File(mat_file_name, 'r')

    def _clip_data(self, data_arr, region, scale_factor=1.):
        region = [int(r / scale_factor) for r in region]
        return super(TimeSeriesData, self)._clip_data(data_arr, region)

    def _invert_blackwhite_colorimage(self, image_data):
        w = np.where(
            np.logical_and(
                image_data[0] == 0.0,
                image_data[1] == 0.0,
                image_data[2] == 0.0))
        w2 = np.where(
            np.logical_and(
                image_data[0] == 1.0,
                image_data[1] == 1.0,
                image_data[2] == 1.0))
        for i in range(3):
            image_data[i][w] = 1 - image_data[i][w]
            image_data[i][w2] = 1 - image_data[i][w2]
        return image_data

    def imshow(self, data, region=None, **kwargs):
        """
        Plot the data.
        
        Parameters
        ----------
        data : np.array
            image data to plot
        region : list or None
            optional, plot only a segement of the data, if value is not `None`
            list or array in the form `[x_min, x_max, y_min, y_max]`
            default : None
        kwargs
            optional, keyword arguments for `scaled_imshow`
        """
        if region is None:
            offset = [0, 0]
        else:
            offset = [region[0], region[2]]
        return microval.scaled_imshow(
            data, offset=offset, **kwargs)

    def cyclenumbers(self):
        """
        Get cycle numbers.
        
        Returns
        -------
        cycles : np.array
            array of cycle numbers for all time frames
        """
        xs, ys = self.fatigue_data['Cyclenumber'].shape
        cyclenumbers = []
        for x in range(xs):
            for y in range(ys):
                v = self._fatigue_mat_data[self.fatigue_data['Cyclenumber'][x, y]]
                cyclenumbers.append(v[0])
        return np.array(cyclenumbers)[:, 0]


class BinaryData(TimeSeriesData):
    """
    Data structure for binary data.
    
    Attributes
    ----------
    binary_data_key : string
        key for accessing the binaray data in the `mat` file
    """
    
    binary_data_key = 'image_time_series'

    def __init__(self, binaraydata_mat_file_name, *args, **kwargs):
        super(BinaryData, self).__init__(*args, **kwargs)
        self._binary_mat_data = self._get_mat_file_contents(binaraydata_mat_file_name)
        self.binary_data = self._binary_mat_data[self.binary_data_key]

    def imshow(self, time_step_number=-1, subtract_initial_state=False, **kwargs):
        """
        Plot binary data.
        
        Parameters
        ----------
        time_step_number : int
            optional, index time step array of time step to plot
            default : -1
        subtract_initial_state : bool
            optional, subtract first frame to get difference image
            default : False
        kwargs
            optional, keyword arguments for `scaled_imshow` or `get_binary_data`
        """
        data = self.get_binary_data(
            time_step_number=time_step_number, subtract_initial_state=subtract_initial_state, **kwargs)
        return TimeSeriesData.imshow(self, data, Cmap='Greys', **kwargs)

    def get_binary_data(
            self,
            time_step_number=-1,
            region=None,
            scale_factor=1.0,
            subtract_initial_state = False,
            **kwargs):
        """
        Get data for a defined time step.
        
        Parameters
        ----------
        time_step_number : int
            optional, index time step array of time step to plot
            default : -1
        region : list or None
            optional, return only a segement of the data, if value is not `None`
            list or array in the form `[x_min, x_max, y_min, y_max]`
            default : None
        scale_factor : float
            optional, scale factor for clipping the image
            default : 1.0
        subtract_initial_state : bool
            optional, subtract first frame to get difference image
            default : False
            
        Returns
        -------
        np.array
            matrix of binarized data
        """
        
        def data_for_timestepno(n):
            binary_data_timestep = self._binary_mat_data[self.binary_data[n][0]]
            return  np.array(binary_data_timestep)/255.
        
        data_arr = data_for_timestepno(time_step_number)
        if subtract_initial_state:
            data_arr = data_arr - data_for_timestepno(0)
        
        if region is not None:
            data_arr = self._clip_data(data_arr, region, scale_factor)
        return data_arr

    def get_num_binary_data(self):
        """
        Get number of frames in the binary data.
        
        Returns
        -------
        int
            number of frames
        """
        return len(self.binary_data)


class SegmentedData(TimeSeriesData):
    """
    Data structure for segemented data.
    
    Attributes
    ----------
    segmented_data_key : string
        key for accessing the segmented data in the `mat` file
    """
    segmented_data_key = 'foreground_mask'

    def __init__(self, segmenteddata_mat_file_name, *args, **kwargs):
        super(SegmentedData, self).__init__(*args, **kwargs)
        self._seg_mat_data = self._get_mat_file_contents(segmenteddata_mat_file_name)
        self.segmented_data  = self._read_segmented_data()

    def _read_segmented_data(self):
        segmented_data = np.array(self._seg_mat_data[self.segmented_data_key])
        return np.append(segmented_data,[np.zeros(segmented_data[0].shape)],axis=0)

    def imshow(self, invert_blackwhite=False, as_binary = False, **kwargs):
        """
        Plot segmented data.
        Note that no definition of time step is required as segemented data only exists for last frame.
        
        Parameters
        ----------
        invert_blackwhite : bool
            optional, change black and white colors in plot
            default : False
        as_binary : bool
            optional, plot as binary data
            default : False
        kwargs
            optional, keyword arguments for `scaled_imshow` or `get_segmented_data`
        """
        data = self.get_segmented_data(**kwargs)
        if as_binary:
            data = data.T
            data[np.where(np.any(data==1,axis=2))] = 1
            data = data.T
        if invert_blackwhite:
            data = self._invert_blackwhite_colorimage(data)
        super(SegmentedData, self).imshow(data, **kwargs)

    def get_dimensions(self, scale_factor=1.):
        """
        Get dimensions for segemented image.
        
        Parameters
        ----------
        scale_factor : float
            optional, scale dimensions by a factor
            default : 1
        """
        return np.array(self.get_segmented_data().shape) * scale_factor

    def get_segmented_data(self, region=None, scale_factor=1., **kwargs):
        """
        Get segmented data.
        
        Parameters
        ----------
        region : list or None
            optional, return only a segement of the data, if value is not `None`
            list or array in the form `[x_min, x_max, y_min, y_max]`
            default : None
        scale_factor : float
            optional, scale factor for clipping the image
            default : 1.0
            
        Returns
        -------
        np.array
            matrix of segmented data
        """
        data_arr = np.array(self.segmented_data)
        if region is not None:
            data_arr = np.array(
                [self._clip_data(da, region, scale_factor) for da in data_arr])
        return data_arr

    def imshow_cracks(self, invert_blackwhite=False, **kwargs):
        """
        Plot only the cracks of segmented data.
        Note that no definition of time step is required as segemented data only exists for last frame.
        
        Parameters
        ----------
        invert_blackwhite : bool
            optional, change black and white colors in plot
            default : False
        kwargs
            optional, keyword arguments for `scaled_imshow` or `get_cracks_from_segmented_data`
        """
        data = self.get_cracks_from_segmented_data(**kwargs)
        if invert_blackwhite:
            data = self._invert_blackwhite_colorimage(data)
        return super(SegmentedData, self).imshow(data, **kwargs)

    def get_cracks_from_segmented_data(
            self, region=None, scale_factor=1., **kwargs):
        """
        Get only cracks in segmented data.
        
        Parameters
        ----------
        region : list or None
            optional, return only a segement of the data, if value is not `None`
            list or array in the form `[x_min, x_max, y_min, y_max]`
            default : None
        scale_factor : float
            optional, scale factor for clipping the image
            default : 1.0
            
        Returns
        -------
        np.array
            matrix of segmented data
        """
        segdat_mod = np.copy(self.segmented_data)
        segdat_mod[1] = 0
        if region is not None:
            segdat_mod = np.array(
                [self._clip_data(da, region, scale_factor) for da in segdat_mod])
        return segdat_mod
