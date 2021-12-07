# Macro model

`macro_P8.inp` is the ABAQUS input file for specimen `P8`'s macro model.
It can be started e.g. by the command
```bash
abaqus job=macro_P8 input=macro_P8.inp cpus=4 ask_delete=OFF interactive

```
where `abaqus` points to your ABAQUS installation. Note that the input file can also be viewed in ABAQUS/CAE by using the `Import...` functionality.

The according result file `macro_P8.odb` used in the submodeling analysis is provided on Fordatis.
This analysis was carried out in `ABAQUS 2018.HF2`.
<br/>[:arrow_down_small:download](https://fordatis.fraunhofer.de/rest/bitstreams/323afd09-0744-4132-bd7d-c009b5af3660/retrieve)

If you want to use a finer or coarser mesh in the analysis, one would preferably use the analytical geometry which `macro_P8.inp` is based on.
To construct it, the script `create.py` is provided, which loads the border coordinates of `P8` into ABAQUS/CAE.
The present input file was then created by fitting this to an analytical geometry using lines and circular arcs.
The script should be used by ABAQUS/CAE's `Run script...` functionality.