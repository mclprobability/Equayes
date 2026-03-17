"""
An __init__.py file in a folder defines the folder as a python package.
It can be empty, which is quite common.

This __init__.py file is not empty to make it convinient, to import certain
objects from .utils package like in the example below.

Example:
From e.g. the repositories main.py just write
    >>> from equayes.utils import LOG_CONFIG
instead of
    >>> from equayes.utils.configuration import load_yaml_config
    >>> LOG_CONFIG = load_yaml_config("logging_config.yml")
"""

from pathlib import Path

from .configuration import load_yaml_config, update_yaml_config

# Dictionary which stores configuration from config/base/parameters.yml, config/local/parameters overwrites identical keys
PARAMETERS: dict = load_yaml_config()  # loads default base/parameters.yml
update_yaml_config(base_dict=PARAMETERS, configfile="local/parameters.yml")

# Dictionary which stores configuration from config/base/config.yml, config/local/config.yml overwrites identical keys
CONFIG: dict = load_yaml_config(configfile="base/globals.yml")
update_yaml_config(base_dict=CONFIG, configfile="local/globals.yml")

# Dictionary which stores key/value pairs stored under CONSTANTS section in config/base/config.yml (may also be overwritten by config/local/config.yml)
CONSTANTS = {}
try:
    CONSTANTS = CONFIG["constants"]
except KeyError:
    pass

# Always provides the absolute path of the repository root folder - very handy
PROJECT_ROOT = Path(__file__).parent.parent.parent

LOG_CONFIG = load_yaml_config(configfile="base/logging_config.yml")
update_yaml_config(base_dict=LOG_CONFIG, configfile="local/logging_config.yml")
