# Micromechanical modeling

The micromechanical model features the meshed grain morphology in an elastic embedding.
In addition to the setup for the crystal plasticity (CP) model, it is described in the following.
The latter is integrated into ABAQUS by a user material subroutine (UMAT).

## Simulation model
In the subdirectory `model`, the ABAQUS input files for the micromechanical model are found.
The main file is `RVE.inp` and the others are dependencies imported by the `*INCLUDE` command.
The model can be started by
```bash
abaqus job=RVE input=RVE.inp cpus=4 ask_delete=OFF globalmodel=macro_P8.odb user=umatCP.f90 interactive
```
where the macro model result file `macro_P8.odb` must be used as the driving model and a CP material routine `umatCP.f90` must be provided (see next section).

The model itself is meshed electron backscatter diffraction (EBSD) data.
Due to it's large size, the mesh file `Mesh.inp` is given on Fordatis.
<br/>[:arrow_down_small:download](https://fordatis.fraunhofer.de/rest/bitstreams/e968bcf4-2df2-4b13-b18f-e1b91b775005/retrieve)

The grains are represented as sections by `*SECTION` cards and the grain's orientation is specified by local coordinate systems using the `*ORIENTATION` card.
These orientations are specified by EULER angles, which can't be evaluated by ABAQUS directly.
Therefore, this is done by a function in the FORTRAN subroutine and a text file `graindata.txt` is provided with the grain's EULER angles in BUNGE notation.
In this file, the line numbers correspond to the section numbering `G_X` and local coordinate system numbering `Grain-X`, where `X` is the 1-based line number.

## User material subroutine
The main UMAT file is `umatCP.f90`, which gives the structure necessary to integrate CP material behavior.
It includes `globals.f90`, where global parameters can be set separately and imported into the main file.

CP material behavior must be given in the FORTRAN function `subroutine umat`, [as defined by ABAQUS](https://abaqus-docs.mit.edu/2017/English/SIMACAESUBRefMap/simasub-c-umat.htm).
If the file `graindata.txt` is present as explained above, the provided algorithm will take care of rotation of global into local coordinates.
Thus, the material behavior of the UMAT can be specified in _local_, i.e. lattice, coordinates.

The `props` vector in the UMAT is defined as follows.

| `props` entry | Parameter name |
|---|---|
| `props(1)` | Stiffness C11 |
| `props(2)` | Stiffness C12 |
| `props(3)` | Stiffness C44 |
| `props(4)` | Number of slip systems |
| `props(5)` | Critical resolved shear stress |
| `props(6)` | Reference shear rate |
| `props(7)` | Flow rule exponent |
| `props(8)` | Kinematic hardening rule, 1 stands for Armstrong-Frederick, 2 stands for Ohno-Wang |
| `props(9)` | Number of kinematic hardening parameters |
| `props(10)` | Kinematic hardening parameter #1 |
| `props(11)` | Kinematic hardening parameter #2 |
| `props(12)` | Kinematic hardening parameter #3 |

## Demo result file

The result file evaluated in the paper is given in Fordatis.
<br/>[:arrow_down_small:download part 1](https://fordatis.fraunhofer.de/rest/bitstreams/e1ed8b4f-3fef-4792-922c-b93137d608c9/retrieve)
<br/>[:arrow_down_small:download part 2](https://fordatis.fraunhofer.de/rest/bitstreams/a2fbd20d-440b-43a9-9770-db7921025214/retrieve)

Three full steps were calculated, which amounts to three loading cycles.
The first frame corresponds to peak loading and the fourth frame to the state after completion of the cycle.
Only four frames are output per step to keep the result file size limited.

Fatigue indicator parameters (FIPs) are saved as solution dependent variables (SDVs) in the following order:

| FIP name | Field output name |
|---|---|
| Accumulated plastic slip (`FIP_P`) | SDV26 |
| FATEMI-SOCIE FIP (`FIP_FS`) | SDV27 |
| Dissipated energy FIP (`FIP_W`) | SDV88 |

Heatmaps for the FIP can be exported as image files by the script `export_fip_heatmap.py`.
The script should be used by ABAQUS/CAE's `Run script...` functionality.