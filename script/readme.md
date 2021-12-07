# Evaluation scripts

This folder contains scripts, which may be useful for evaluating experimental and model data.
In `microval`, a Python package is given and in `example`, Jupyter notebooks show how to use it.

## Installing the Python package
We recommend using an [anaconda](https://www.anaconda.com/products/individual) or [miniconda](https://docs.conda.io/en/latest/miniconda.html) environment.
Switch into the `microval` folder and create an environment (named e.g. `mfvf`) with the necessary requirements by
```bash
conda create --name mfvf --file requirements.txt
```
Then, install the package via `pip` (following command installs in development mode)
```bash
pip install -e .
```
You are then able to import the package in Python by
```python
import microval
```

## Example code
The following Jupyter notebooks are given in `example` to demonstrate the code's usage:
  * `Experimental.ipynb` shows how to plot binarized and segmented time series data
  * `Simulation.ipynb` shows how to overlay heatmaps from the simulation with the experimental data