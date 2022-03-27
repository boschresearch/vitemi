# Simulation model files

The simulation of the mesoscale fatigue specimen `P8` in the paper is conducted with ABAQUS.
The model consists of two successive stages: a macroscopic (macro) model and the actual micromechanical (micro) validation model.
Files for each of these stages can be found in the subfolders `macro` and `micro`.
Furthermore, the general concepts are explained below.

## Macro model
The macro model utilizes an isotropic continuum model to calculate the overall loading state.
This is important to prescribe appropriate boundary conditions for the micromechanical simulation.

As the specimen is fatigued in the very high cycle (VHCF) regime, no significant plastic deformation is expected at this scale.
Therefore, we uses a linear-elastic material model with a YOUNG's modulus of `E = 210 GPa` and a POISSON's ratio of `ν = 0.3`.

The calculated loading state is mapped to the micro model using a [submodeling approach](https://abaqus-docs.mit.edu/2017/English/SIMACAEANLRefMap/simaanl-c-submodeloverview.htm). 

## Micro model
On the microscopic scale, a crystal plasticity (CP) model is used to consider the constitutive behavior for individual grains.
The model itself is derived from the acquired electron backscatter diffraction (EBSD) data, which can be found in the repositories' `data` folder.
This data is mapped to a regular voxel mesh and extruded by some elements in the out-of-plane-direction.

The parametrization of the CP model is described in the accompanying paper.
It is mainly derived by fitting the model's homogenized response to cyclically stabilized stress-strain hysteresis curves acquired for macroscopic fatigue specimen.
These hysteresis curves can also be found in the `data` folder.

In the paper, a small strain CP model is used, which is implemented as a user material subroutine (UMAT) for ABAQUS.
The latter is currently not provided with the current repository.
However, we point out several codes available freely:
  - [Columbia University](http://www.columbia.edu/~jk2079/Kysar_Research_Laboratory/Single_Crystal_UMAT.html)
  - [Center for Advanced Vehicular Systems at Mississippi State University](https://icme.hpc.msstate.edu/mediawiki/index.php/Code:_ABAQUS_CPFEM.html)

The given model in `micro` assumes a certain interface, which a third-party UMAT may have to be customized to.
Consequently, a template showing the UMAT's integration is given.