"""
This __init__.py file defines the whole project source code folder as a python
package. It can be empty.
In this case, we just showcase, that beside variables (see .utils/__init__.py),
even functions can be broadcasted here for well structured and clearer imports.
"""

version = "release_1"
try:
    from setuptools_scm import get_version

    version = get_version(root="..", relative_to=__file__, git_describe_command="git describe --tags --match v[0-9]*")
except:
    pass

# Importing here in the __init__.py like below makes it possible to import with
# >>> from equayes import Equayes
# instead of having to know, in which module (.py file) of the core package,
# the class Equayes is implemented.
# This means, we make module level objects importable at package level.
from .core.equayes import Equayes
from .utils import CONFIG, PARAMETERS, PROJECT_ROOT
