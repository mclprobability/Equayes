# installability

Repositories created with the Data-Science-Project-Template are pip installable out of the box.  
The `equayes` is the installed source folder, the `pyproject.toml` specifies the pip install process and the `MANIFEST.in` defines which non-python files should be included into the pip package.

In a CLI pointing to the root of the created repository, install the package with `pip install .`.  
If you are in the development process do a `pip install -e .`. This way, any changes in the packages' code are instantly reflected in the installed package.

If you want any third party package dependencies to be installed along with your package, add them to the list in the `dependencies` section of the `pyproject.toml` file.
