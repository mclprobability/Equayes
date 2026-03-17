# Getting started...
This Equayes repository collects (python) sourcecode, which is part the MCL project "Equayes".  
Because it follows a software [best-practice workflow](sw_dev_workflow), the existing code (functions, classes, objects) is (re-)usable within:
- python console (CLI)
- IPython environment
- Jupyter Notebooks
- other .py files 

## Installation

This package is pip installable :)


::::{tab-set}
:::{tab-item} Developer
:sync: tab1


```{include} ../../README.md
:start-after: "## Developer Installation"
:end-before: "## User Installation"
:relative-images:
```

:::
:::{tab-item} User
:sync: tab2


```{include} ../../README.md
:start-after: "## User Installation"
:end-before: "## Repository Creation Info"
:relative-images:
```


:::
:::{tab-item} De-Installation
:sync: tab2

Each project's python package is installed with the **MCL-**-suffix to easily identify in-house developed packages.  
So your project/package called `equayes` and you `pip install` it, you'll find your package via `pip list` (or `conda list`) under `m` called **`MCL-equayes`**.  

That also means, to `pip uninstall` the package, do it via
```console
pip uninstall MCL-equayes
```

:::
::::



