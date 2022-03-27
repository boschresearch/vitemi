# Experimental data

All experimental data is provided through a separate Fordatis repository but can be downloaded directly below.

The purpose of this page is to list and explain individual experimental data files used for the validation of micromechanical fatigue simulation.
The data acquisition is covered exhaustively elsewhere:

> *Ali Riza Durmaz, Nadira Hadzic, Thomas Straub, Chris Eberl, Peter Gumbsch* **Efficient Experimental and Data-Centered Workflow for Microstructure-Based Fatigue Data** [Experimental Mechanics](https://link.springer.com/article/10.1007/s11340-021-00758-x)


The raw data is acquired with different techniques such as optical image acquisition, scanning electron microscopy (SEM) and electron backscatter diffraction (EBSD). The different modalities are spatially registered using specimen surface features as well as affine and elastic transformation.
Dense surface damage maps are provided as a mask derived from the highly resolved SEM maps. The damage instances were segmented (multi-class pixel-wise classification) using a deep learning model introduced in 

> *Akhil Thomas, Ali Riza Durmaz, Thomas Straub, Chris Eberl* **Automated Quantitative Analyses of Fatigue-Induced Surface Damage by Deep Learning** [Materials](https://www.mdpi.com/1996-1944/13/15/3298/htm)


and then checked for correctness/adapted by experts. For validation of computational damage features or fatigue indicator parameters either this damage mask (`foreground_mask.mat`) can be utilized or alternatively a series of optical images acquired in-situ (`image_time_series_(red).mat`). Therefore, both data sets can be loaded and superimposed to the simulation data. This is performed by executing the python script `Simulation.ipynb` available in another subdirectory called `script`. 
Two versions of the timeseries data is provided below, a full version containing all acquired images uncompressed in format `uint16` with 12bit information (15.1 GB) and a reduced version compressed to `uint8` where every second image was discarded (1.1 GB). We suggest to start with the compressed version, when timeseries data is supposed to be used as reference.

## The provided files include:

- **fatigue_data.mat**: A mat.file (v7.3) that contains control data acquired during the fatigue cyclic loading. It references loading cycles with images and change in bending resonant frequency. The data points where no image was acquired were discarded.
<br/>[:arrow_down_small:download](https://fordatis.fraunhofer.de/rest/bitstreams/f86bb4ca-2a4c-428a-8e5b-6fa318dd6222/retrieve)
- **fatigue_data_red.mat**: A reduced version of former where every second data instance was discarded.
<br/>[:arrow_down_small:download](https://fordatis.fraunhofer.de/rest/bitstreams/1910d200-0578-4a23-be24-341fe6d60cad/retrieve)
- **image_time_series.mat**: mat.file (v7.3) which comprises all grayscale images acquired in the course of the fatigue experiment with a stroboscope imaging setup. These images are not raw images but reduced to the same field of view and upsampled to the same resolution as the EBSD measurement. Each individual frame corresponds to one instance in `fatigue_data.mat`.
<br/>[:arrow_down_small:download](https://fordatis.fraunhofer.de/rest/bitstreams/1d9d3486-37c8-447b-8d84-d9ffbc606dc2/retrieve)
- **image_time_series_red.mat**: A reduced version of former where every second data instance was discarded and images were compressed from 12 bit to 8 bit to avoid memory limitations. Each individual frame corresponds to one instance in `fatigue_data_red.mat`.
<br/>[:arrow_down_small:download](https://fordatis.fraunhofer.de/rest/bitstreams/e2a227c7-8d02-4625-8658-03ba926df165/retrieve)
- **threshold_mask.mat**: mat.file (v7.3) containing a variable with the same name to perform threshold segmentation on the time series images. The thresholding was applied after subtracting the reference image (the first image in `image_time_series.mat`) from each image of the time series. 
<br/>[:arrow_down_small:download](https://fordatis.fraunhofer.de/rest/bitstreams/e0e0c9b9-a34f-4565-ae05-fdce881e63a4/retrieve)
- **sem_after_fatigue.tif**: SEM after fatigue describes a topography-sensitive, highly resolved stitch scan of the specimen surface.
<br/>[:arrow_down_small:download](https://fordatis.fraunhofer.de/rest/bitstreams/35551114-e8e3-4f11-aa22-265ced8bc138/retrieve)
- **sem_damage_mask.tif**: The analogous stitch mask, where damage was detected by a deep learning segmentation algorithm and then adjusted by a human expert. Three classes exist where `0` corresponds to background, `1` to cracks and `2` to protruded surface regions (protrusions).
<br/>[:arrow_down_small:download](https://fordatis.fraunhofer.de/rest/bitstreams/eeb18e6a-9648-4f19-a06a-a09142129a02/retrieve)
- **foreground_mask.mat**: A three-dimensional array (mat.file (v7.3)) derived from the segmented SEM mask but registered and downsampled to the EBSD data. It has two channels where the first corresponds to cracks and the second corresponds to extrusion area.
<br/>[:arrow_down_small:download](https://fordatis.fraunhofer.de/rest/bitstreams/b0712bcd-4cd4-410a-b5e8-964da253980a/retrieve)
- **ebsd.ang**: This file contains the orientation mapping data (Euler angles in Bunge notation) and further metrics collected for the highly-loaded region of the specimen. It is collected with a TSL EDAX EBSD system.
<br/>[:arrow_down_small:download](https://fordatis.fraunhofer.de/rest/bitstreams/91c16229-f78d-47ec-90da-cd767176fc97/retrieve)
- **macroscopic_testing.zip**: Contains a series of stress-strain hysteresis curves as tab-separated ASCII-files with different load amplitudes (`14003_x.txt`) and a tensile test (`14003_static.txt`). These curves are typically used to calibrate the hardening models or validate macroscopic hardening. The structure of these ASCII-files is as follows.
All of the data is given as tab (`\t`) delimited text files.
The structure is as follows:
    - `14003_static.txt`<br>
    Tensile testing data, four columns:

    | Tensile strain / [%] | Tensile displacement / [mm] | Tensile Loading / [N] | Tensile stress / [MPa] |
    |---|---|---|---|
    |...|...|...|...|

    - `14003_$amp$.txt`<br>
    Strain-controlled hysteresis data at `R = -1`, where `$amp$` stands for the strain amplitude in percent.
    Two columns:
    
    | Strain / [%] | Stress / [MPa] |
    |---|---|
    |...|...|
    
    <br/>[:arrow_down_small:download](https://fordatis.fraunhofer.de/rest/bitstreams/71010203-cada-4c75-91e5-46df50ae151c/retrieve)
- **specimen_geom_bc.zip**: ASCII-files describing the specimen border, the controlled displacement amplitude during fatigue, and the specimen thickness.
    The structure is as follows:
    - `border_coordinates.txt`<br>
        XY coordinates of the planar specimen geometry. Can be used in FE model.
    - `displacement_vector.txt`<br>
        Loading of the specimen is applied in out-of-plane-direction (bending load case) for `R = -1` on the right side.
        This file are the x, y and z components for the displacement vector to apply.
    - `sample_thickness.txt`<br>
        The samples thickness in z direction.
        
    <br/>[:arrow_down_small:download](https://fordatis.fraunhofer.de/rest/bitstreams/71010203-cada-4c75-91e5-46df50ae151c/retrieve)