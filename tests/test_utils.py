"""
This file implements unittest code to test for proper functionality of the
equayes.utils subpackage.

It uses "unittest" framework from the python standard library.
"""

import unittest
from datetime import date
from unittest.mock import mock_open, patch

from equayes.utils import log
from equayes.utils.configuration import load_yaml_config, update_yaml_config

logger = log.getLogger("unittest_utils")

__author__ = "MCLProbability"
__email__ = "240669060+mclprobability@users.noreply.github.com"
__copyright__ = "Copyright 2026, " "Materials Center Leoben Forschung GmbH"
__license__ = "MIT"
__status__ = "Development"


class LoggerTests(unittest.TestCase):
    def test_simple_log(self):
        try:
            logger.info("Logging works like a charm")
        except:
            self.fail("Simple logger.info raised an error :(")


class ConfigTests(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data="test_key: base_value"))
    @patch("pathlib.Path.is_file")
    def test_load_yaml_config(self, patched_isfile):
        """
        unittest if load_yaml_config() works as expected
        """
        patched_isfile.return_value = True
        result = load_yaml_config("fake_config.yml")
        self.assertEqual(result, {"test_key": "base_value"})

        patched_isfile.return_value = False
        result = load_yaml_config("fake_config.yml")
        self.assertEqual(result, {})

    @patch("builtins.open", mock_open(read_data="test_key: local_value"))
    @patch("pathlib.Path.is_file")
    def test_update_yaml_config(self, patched_isfile):
        """
        unittest if update_yaml_config() works as expected
        """
        config = {"test_key": "base_value"}

        patched_isfile.return_value = True
        update_yaml_config(config, "local_fake_config.yml")
        self.assertEqual(config, {"test_key": "local_value"})

        other_config = {"test_key": "base_value"}
        patched_isfile.return_value = False
        update_yaml_config(other_config, "local_fake_config.yml")
        self.assertEqual(other_config, {"test_key": "base_value"})
