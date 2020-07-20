# -*- coding: utf-8 -*-

# All configuration values have a default; values that are commented out
# serve to show the default.

import os
import subprocess
import sys

import json
from jsmin import jsmin

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
if "READTHEDOCS" not in os.environ:
    sys.path.insert(1, os.path.abspath("../../"))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
needs_sphinx = "1.6"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "numpydoc",
    "sphinxcontrib.bibtex",
    "sphinx_gallery.gen_gallery",
]
# numpydoc_show_class_members = False
# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "pysteps"
copyright = "2020, PySteps developers"
author = "PySteps developers"


# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
def get_version():
    """
    Returns project version as string from 'git describe' command.
    """

    from subprocess import check_output

    _version = check_output(["git", "describe", "--tags", "--always"])

    if _version:
        return _version.decode("utf-8")
    else:
        return "X.Y"


# The short X.Y version.
version = get_version().lstrip("v").rstrip().split("-")[0]

# The full version, including alpha/beta/rc tags.
release = version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Read the Docs build --------------------------------------------------


def set_root():
    fn = os.path.abspath(os.path.join("..", "..", "pysteps", "pystepsrc"))
    with open(fn, "r") as f:
        rcparams = json.loads(jsmin(f.read()))

    for key, value in rcparams["data_sources"].items():
        new_path = os.path.join("..", "..", "pysteps-data", value["root_path"])
        new_path = os.path.abspath(new_path)

        value["root_path"] = new_path

    fn = os.path.abspath(os.path.join("..", "..", "pystepsrc.rtd"))
    with open(fn, "w") as f:
        json.dump(rcparams, f, indent=4)


if "READTHEDOCS" in os.environ:
    repourl = "https://github.com/pySTEPS/pysteps-data.git"
    dir = os.path.join(os.getcwd(), "..", "..", "pysteps-data")
    dir = os.path.abspath(dir)
    subprocess.check_call(["rm", "-rf", dir])
    subprocess.check_call(["git", "clone", repourl, dir])
    set_root()
    pystepsrc = os.path.abspath(os.path.join("..", "..", "pystepsrc.rtd"))
    os.environ["PYSTEPSRC"] = pystepsrc

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
# html_theme = 'classic'
html_theme = "sphinx_rtd_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["../_static"]
html_css_files = ["../_static/pysteps.css"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    "**": [
        "relations.html",  # needs 'show_related': True theme option to display
        "searchbox.html",
    ]
}

html_domain_indices = True

autosummary_generate = True

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "pystepsdoc"

# -- Options for LaTeX output ---------------------------------------------

# This hack is taken from numpy (https://github.com/numpy/numpy/blob/master/doc/source/conf.py).
latex_preamble = r"""
    \usepackage{amsmath}
    \DeclareUnicodeCharacter{00A0}{\nobreakspace}
    
    % In the parameters section, place a newline after the Parameters
    % header
    \usepackage{expdlist}
    \let\latexdescription=\description
    \def\description{\latexdescription{}{} \breaklabel}
    
    % Make Examples/etc section headers smaller and more compact
    \makeatletter
    \titleformat{\paragraph}{\normalsize\py@HeaderFamily}%
                {\py@TitleColor}{0em}{\py@TitleColor}{\py@NormalColor}
    \titlespacing*{\paragraph}{0pt}{1ex}{0pt}
    \makeatother
    
    % Fix footer/header
    \renewcommand{\chaptermark}[1]{\markboth{\MakeUppercase{\thechapter.\ #1}}{}}
    \renewcommand{\sectionmark}[1]{\markright{\MakeUppercase{\thesection.\ #1}}}
"""

latex_elements = {
    "papersize": "a4paper",
    "pointsize": "10pt",
    "preamble": latex_preamble
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

latex_domain_indices = False

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "pysteps.tex", "pysteps Reference", author, "manual"),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "pysteps", "pysteps Reference", [author], 1)]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "pysteps",
        "pysteps Reference",
        author,
        "pysteps",
        "One line description of project.",
        "Miscellaneous",
    ),
]

# -- Options for Sphinx-Gallery -------------------------------------------

# The configuration dictionary for Sphinx-Gallery

sphinx_gallery_conf = {
    "examples_dirs": "../../examples",  # path to your example scripts
    "gallery_dirs": "auto_examples",  # path where to save gallery generated examples
    "filename_pattern": r"/*\.py",  # Include all the files in the examples dir
}
