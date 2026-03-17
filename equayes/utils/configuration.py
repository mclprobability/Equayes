"""
This module provides functions for PROJECT-RELATED configuration.
(No configuration of side technologies like CI Pipelines, git hooks, etc.)
"""

from pathlib import Path

import yaml

CONFIG_PATH = Path(Path(__file__).parent.parent.absolute(), "config")


def load_yaml_config(configfile: str = "base/parameters.yml", location: Path = CONFIG_PATH) -> dict:
    """
    Parses a yaml configuration file into a correspoinding dictionary.

    Args:
        configfile (str, optional): Name of the .yml file with the configuration,
            may also be a path/to/file.yml located INSIDE location argument.
        location (Path, optional): Path to yaml file, where config.yml is stored.
            Defaults to module constant <CONFIG_PATH>, which points to the
            packages' config folder.
            (It is recommended to put all configuration*.yml files into that folder.)

    Returns:
        dict: (potentially nested) dictionary with all yaml configurations inside.
    """

    filepath = Path(location, configfile)
    if not filepath.is_file():
        return {}
    with open(filepath, "r", encoding="utf-8") as file:
        config_dict = yaml.safe_load(file)
    return config_dict if type(config_dict) is dict else {}


def update_yaml_config(base_dict: dict, configfile: str, location: Path = CONFIG_PATH) -> dict:
    """
    Updates a given config dictionary (base_dict), with a new dictionary

    Args:
        base_dict (dict): Dictionary to update
        configfile (str): Name of the .yml file with the configuration,
            may also be a path/to/file.yml located INSIDE location argument.
        location (Path, optional): Path to yaml file, where config.yml is stored.
            Defaults to module constant <CONFIG_PATH>, which points to the
            packages' config folder.
            (It is recommended to put all configuration*.yml files into that folder.)

    Returns:
        dict: (potentially nested) updated dictionary with all yaml configurations inside.
    """
    if not (Path(location) / Path(configfile)).is_file():
        return base_dict

    config_dict = load_yaml_config(configfile=configfile, location=Path(location))
    _update_dictionary(base_dict, config_dict)


def _update_dictionary(base_dict: dict, config_dict: dict):
    for key, value in config_dict.items():
        if isinstance(value, dict) and key in base_dict and isinstance(base_dict[key], dict):
            # If both values are dictionaries, recursively update in-place
            _update_dictionary(base_dict[key], value)
        else:
            # Otherwise, simply update the value
            base_dict[key] = value
