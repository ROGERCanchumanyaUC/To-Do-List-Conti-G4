# docs/source/conf.py
# Configuration file for the Sphinx documentation builder.

from __future__ import annotations

import os
import sys

# -- Configuración del Path -------------------------------------------------
# Desde /docs/source subimos 2 niveles a la raíz del proyecto
# y así se puede importar "src.*"
sys.path.insert(0, os.path.abspath("../../"))

# -- Project information -----------------------------------------------------
project = "OOPRA"
copyright = "2026, Antony, Dayaneira, Diego y Roger"
author = "Antony, Dayaneira, Diego y Roger"
release = "v0.1"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # Google Style
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
]

# Napoleon (Google Style)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_param = True
napoleon_use_rtype = True

templates_path = ["_templates"]

language = "es"

# autodoc
autodoc_member_order = "bysource"
autodoc_typehints = "description"

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "undoc-members": False,
    "show-inheritance": True,
    "exclude-members": "metadata",
}

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
