# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst
#
# Astropy documentation build configuration file.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this file.
#
# All configuration values have a default. Some values are defined in
# the global Astropy configuration which is loaded here before anything else.
# See astropy.sphinx.conf for which values are set there.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath('..'))
# IMPORTANT: the above commented section was generated by sphinx-quickstart, but
# is *NOT* appropriate for astropy or Astropy affiliated packages. It is left
# commented out with this explanation to make it clear why this should not be
# done. If the sys.path entry above is added, when the astropy.sphinx.conf
# import occurs, it will import the *source* version of astropy instead of the
# version installed (if invoked as "make html" or directly with sphinx), or the
# version in the build directory (if "python setup.py build_sphinx" is used).
# Thus, any C-extensions that are needed to build the documentation will *not*
# be accessible, and the documentation will not build correctly.

import datetime
import os
import sys

try:
    from sphinx_astropy.conf.v1 import *  # noqa
except ImportError:
    print('ERROR: the documentation requires the sphinx-astropy package to be installed')
    sys.exit(1)

# Get configuration information from setup.cfg
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser
conf = ConfigParser()

conf.read([os.path.join(os.path.dirname(__file__), '..', 'setup.cfg')])
setup_cfg = dict(conf.items('metadata'))

# -- General configuration ----------------------------------------------------

# By default, highlight as Python 3.
highlight_language = 'python3'

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.2'

# To perform a Sphinx version check that needs to be more specific than
# major.minor, call `check_sphinx_version("x.y.z")` here.
# check_sphinx_version("1.2.1")

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns.append('_templates')

# This is added to the end of RST files - a good place to put substitutions to
# be used globally.
rst_epilog += """
"""

# -- Project information ------------------------------------------------------

# This does not *have* to match the package name, but typically does
project = setup_cfg['package_name']
author = setup_cfg['author']
copyright = '{0}, {1}'.format(
    datetime.datetime.now().year, setup_cfg['author'])

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

__import__(setup_cfg['package_name'])
package = sys.modules[setup_cfg['package_name']]

# The short X.Y version.
version = package.__version__.split('-', 1)[0]
# The full version, including alpha/beta/rc tags.
release = package.__version__


# -- Options for HTML output --------------------------------------------------

# A NOTE ON HTML THEMES
# The global astropy configuration uses a custom theme, 'bootstrap-astropy',
# which is installed along with astropy. A different theme can be used or
# the options for this theme can be modified by overriding some of the
# variables set in the global configuration. The variables set in the
# global configuration are listed below, commented out.


# Add any paths that contain custom themes here, relative to this directory.
# To use a different custom theme, add the directory containing the theme.
#html_theme_path = []

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes. To override the custom theme, set this to the
# name of a builtin theme or the name of a custom theme in html_theme_path.
html_theme = "sphinx_rtd_theme"


# Please update these texts to match the name of your package.
# html_theme_options = {
#     'logotext1': 'spec',  # white,  semi-bold
#     'logotext2': 'viz',  # orange, light
#     'logotext3': ':docs'   # white,  light
#     }


# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '_static/specviz_html_logo.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = ''

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = ''

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = '{0} v{1}'.format(project, release)

# Output file base name for HTML help builder.
htmlhelp_basename = project + 'doc'


# -- Options for LaTeX output -------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [('index', project + '.tex', project + u' Documentation',
                    author, 'manual')]


# -- Options for manual page output -------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [('index', project.lower(), project + u' Documentation',
              [author], 1)]


# -- Options for the edit_on_github extension ---------------------------------

if eval(setup_cfg.get('edit_on_github')):
    extensions += ['sphinx_astropy.ext.edit_on_github']

    versionmod = __import__(setup_cfg['package_name'] + '.version')
    edit_on_github_project = setup_cfg['github_project']
    if versionmod.version.release:
        edit_on_github_branch = "v" + versionmod.version.version
    else:
        edit_on_github_branch = "master"

    edit_on_github_source_root = ""
    edit_on_github_doc_root = "docs"

# -- Resolving issue number to links in changelog -----------------------------
github_issues_url = 'https://github.com/{0}/issues/'.format(setup_cfg['github_project'])

# -- Turn on nitpicky mode for sphinx (to warn about references not found) ----
#
nitpicky = True

nitpick_ignore = [('py:class', 'PyQt5.QtWidgets.QMainWindow'),
                  ('py:class', 'PyQt5.QtWidgets.QWidget'),
                  ('py:class', 'PyQt5.QtWidgets.QTextEdit'),
                  ('py:class', 'PyQt5.QtWidgets.QMdiSubWindow'),
                  ('py:class', 'PyQt5.QtWidgets.QTabBar'),
                  ('py:class', 'PyQt5.QtWidgets.QLabel'),
                  ('py:class', 'PyQt5.QtWidgets.QComboBox'),
                  ('py:class', 'PyQt5.QtWidgets.QMessageBox'),
                  ('py:class', 'PyQt5.QtWidgets.QDialog'),
                  ('py:class', 'PyQt5.QtWidgets.QToolBar'),
                  ('py:class', 'PyQt5.QtWidgets.QStyledItemDelegate'),
                  ('py:class', 'PyQt5.QtWidgets.QListView'),
                  ('py:class', 'PyQt5.QtCore.QMimeData'),
                  ('py:class', 'PyQt5.QtCore.QAbstractListModel'),
                  ('py:class', 'PyQt5.QtCore.QAbstractTableModel'),
                  ('py:class', 'PyQt5.QtCore.QThread'),
                  ('py:class', 'PyQt5.QtCore.QSortFilterProxyModel'),
                  ('py:obj', 'PyQt5.QtGui.QIcon'),
                  ('py:class', 'PyQt5.QtGui.QStandardItemModel'),
                  ('py:class', 'PyQt5.QtGui.QStandardItem'),
                  ('py:class', 'qtpy.QtGui.QMouseEvent'),
                  ('py:class', 'qtpy.QtCore.QModelIndex'),
                  ('py:class', 'qtpy.QtWigets.QMdiArea'),
                  ('py:class', 'qtpy.QtWidgets.QListView'),
                  ('py:class', 'pyqtgraph.widgets.PlotWidget.PlotWidget'),
                  ('py:class', 'pyqtgraph.graphicsItems.LinearRegionItem.LinearRegionItem'),
                  ('py:class', 'pyqtgraph.graphicsItems.TextItem.TextItem'),
                  ('py:class', 'pyqtgraph.graphicsItems.PlotDataItem.PlotDataItem')]

# add custom intersphinx
intersphinx_mapping['specutils'] = ('https://specutils.readthedocs.io/en/latest/', None)
intersphinx_mapping['pyqtgraph'] = ('http://www.pyqtgraph.org/documentation/', None)
