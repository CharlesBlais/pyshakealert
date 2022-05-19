# ShakeAlert utilities/library

## Installation

The following library required *cartopy* library for generating maps.  Unfortunatly, cartopy is not the friendliest to install using python PIP hence it is much easier to install using *miniconda* or *anaconda*.

### Using Anaconda

The following is assuming your anaconda environment has already been created and activated.  For more information, please visit the conda information [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).

```bash
conda install cartopy
conda install obspy
python -m pip install git+[git link]
# or, if project was git cloned and you are in the current directory
python -m pip install .
```

### Using PIP

Cartopy requires some base developper libraries installed for compilation.  The following are for RHEL/CentOS.

```bash
sudo yum install geos geos-devel proj proj-devel python3-devel
python -m pip install --user git+[git link]
# or, if project was git cloned and you are in the current directory
python -m pip install --user .
```
