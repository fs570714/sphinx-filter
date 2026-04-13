# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os

project = 'test'
copyright = '2025, F.S.'
author = 'F.S.'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

filter_dir = os.path.dirname(__file__) + "/../../"
print(filter_dir)
sys.path.insert(0, filter_dir)

extensions = ['myst_parser', 'sphinx_filter.filter', 'sphinx_markdown_builder']
myst_enable_extensions = ["colon_fence"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

source_suffix = {
    '.md': 'markdown',
}

html_show_sourcelink = False
html_copy_source = False

