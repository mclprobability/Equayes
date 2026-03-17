"""
This module organizes how logging is utilized throughout the project.
"""

import logging.config
import platform
from pathlib import Path

from . import CONFIG, LOG_CONFIG, PROJECT_ROOT


class HostnameFilter(logging.Filter):
    """
    A simple helper class for adding hostname of the workstation in the log files.
    """

    hostname = platform.node()

    def filter(self, record):
        record.hostname = HostnameFilter.hostname
        return True


def setup_logging():
    """
    Sets up logging configuration using the pre-loaded LOG_CONFIG.
    """
    try:
        # Adjust file paths for file handlers in LOG_CONFIG
        for handler in LOG_CONFIG["handlers"]:
            if "filename" in LOG_CONFIG["handlers"][handler]:
                # Create full path for log files
                log_filename = str(
                    Path(
                        PROJECT_ROOT,
                        CONFIG["paths"]["log_path"],
                        Path(LOG_CONFIG["handlers"][handler]["filename"]).name,
                    )
                )
                LOG_CONFIG["handlers"][handler]["filename"] = log_filename

        # Apply logging configuration from LOG_CONFIG
        logging.config.dictConfig(LOG_CONFIG)

        # Add HostnameFilter to all handlers
        logger = logging.getLogger()
        for handler in logger.handlers:
            handler.addFilter(HostnameFilter())  # Ensure HostnameFilter is applied to all handlers

    except Exception as e:
        raise RuntimeError("Error in setting up logging configuration.") from e


def getLogger(src_name="equayes"):
    """
    Returns a logger object fully configured by LOG_CONFIG.

    Args:
        src_name: Name of the logger (default is 'mcl_example_project').

    Returns:
        logging.Logger: Configured logger object.
    """
    setup_logging()  # Ensure logging is set up before returning the logger
    logger = logging.getLogger(src_name)

    # Ensure HostnameFilter is added to the logger and its handlers
    for handler in logger.handlers:
        handler.addFilter(HostnameFilter())

    if logger.parent:
        for handler in logger.parent.handlers:
            handler.addFilter(HostnameFilter())

    return logger
