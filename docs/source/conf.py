"""
Configuration file for the Sphinx documentation builder.

Template Author: Franz-Martin Frieß
docs created with template version: 0.10.dev9+g414e38c

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html

TODO: switch fully to executable books yaml configuration
      (currently this is a manual mixture of sphinx and executable books)
"""

import os
import sys
from setuptools_scm import get_version

sys.path.insert(0, os.path.abspath(os.path.join("..", "..")))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

__author__ = "MCLProbability"
__email__ = "240669060+mclprobability@users.noreply.github.com"
__copyright__ = "Copyright 2026, " "Materials Center Leoben Forschung GmbH"
__license__ = "MIT"
__status__ = "Development"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

project = "Equayes"
author = "MCLProbability"
project_copyright = "2026, Materials Center Leoben Forschung GmbH"
release = version = "0.1_docs_only"
try:
    # override release with setuptools_scm get_version, if available
    release = version = get_version(
        root="../..", relative_to=__file__, git_describe_command="git describe --tags --match v[0-9]* "
    )
except:
    pass


extensions = [
    "myst_nb",  # makes jupyter notebooks integratable into sphinx docs + also enables myst-parser
    "sphinx_design",
    "sphinx_proof",
    "sphinx.ext.napoleon",  # can parse google/numpy docstring formats
    "sphinx.ext.autodoc.typehints",
    "sphinx.ext.duration",  # measures and shows the built time for each page
    "sphinx.ext.autosectionlabel",  # makes every (sub)heading a target directive automatically
    # 'sphinx.ext.autodoc',
    # "sphinx_rtd_theme",
]

extensions.append("autoapi.extension")  # creates automatic API references from docstrings (alternative to sphinx.autodoc)

# Prefix document path to section labels, to use:
# `path/to/file:heading` instead of just `heading`
autosectionlabel_prefix_document = True

nb_execution_mode = "auto"
nb_execution_excludepatterns = ["*.ipynb"]
myst_enable_extensions = [
    "colon_fence",
    # "deflist",
    "dollarmath",
    "amsmath",
    "substitution",
    # "html_image",
    # "linkify",
]
myst_substitutions = {"version": release}
myst_heading_anchors = 3
# myst_extended_syntax = True

# source_suffix = {  # define which files should be parsed by which parser(-extension)
# '.ipynb': 'myst-nb'
# #'.myst': 'myst'
# }

templates_path = ["_templates"]
exclude_patterns = []

autodoc_typehints = (
    "both"  # for typehints (extension 'sphinx.ext.autodoc.typehints' necessary) "signature" is another possible value
)

# autoapi_root = 'rooty'
# autoapi_ignore = []
# autoapi_keep_files = True
autoapi_type = "python"

# set auto-api src folder if given:
autoapi_dirs = ["../../equayes"]

autoapi_template_dir = "_templates/autoapi"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "private-members",
    #'special-members',
    "imported-members",
    "show-inheritance-diagram",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_theme_options = {
    "repository_url": "https://github.com/mclprobability/Equayes",
    "use_repository_button": True,
    # "use_issues_button": True,
    "use_edit_page_button": True,
    "show_toc_level": 2,
    "logo": {
        "text": f"{project} v{release}",
    },
}
html_static_path = ["_static"]

# html_title = "Your title"
html_logo = "_references/mcl_logo_ohnetext_v_small.jpg"


rst_prolog = """
.. role:: summarylabel
"""  # This custom role is for nice sphinx-autoapi summary table

html_css_files = [
    "css/custom.css",
]


def contains(seq, item):
    return item in seq


def prepare_jinja_env(jinja_env) -> None:
    jinja_env.tests["contains"] = contains


autoapi_prepare_jinja_env = prepare_jinja_env
