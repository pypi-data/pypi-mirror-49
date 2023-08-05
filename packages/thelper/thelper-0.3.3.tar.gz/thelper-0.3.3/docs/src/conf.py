# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../'))


# -- Project information -----------------------------------------------------

project = 'thelper'
copyright = '2018, Pierre-Luc St-Charles'
author = 'Pierre-Luc St-Charles'
version = release = '0.3.3'


# -- General configuration ---------------------------------------------------

nitpicky = False  # caused too many dummy warnings as of 2019/05 due to attribs
nitpick_ignore = [
    ("py:class", "object"),
    ("py:class", "abc.ABC"),
    ("py:class", "torch.optim.lr_scheduler._LRScheduler"),
    ("py:class", "torch.utils.data.dataset.Dataset"),
    ("py:class", "torch.utils.data.dataloader.DataLoader"),
    ("py:class", "torch.utils.data.sampler.Sampler"),
    ("py:class", "torch.nn.modules.module.Module"),
    ("py:class", "torch.nn.Module"),
    ("py:class", "torchvision.transforms.transforms.Compose")
]

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.extlinks',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosectionlabel',
]

autosectionlabel_prefix_document = True

if os.getenv("SPELLCHECK"):
    extensions += "sphinxcontrib.spelling",
    spelling_show_suggestions = True
    spelling_lang = "en_US"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["modules.rst"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "trac"

extlinks = {
    "issue": ("https://github.com/plstcharles/thelper/issues/%s", "#"),
    "pr": ("https://github.com/plstcharles/thelper/pull/%s", "PR #"),
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'sphinx_rtd_theme'
import sphinx_py3doc_enhanced_theme
html_theme = "sphinx_py3doc_enhanced_theme"
html_theme_path = [sphinx_py3doc_enhanced_theme.get_html_theme_path()]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}
html_theme_options = {
    "githuburl": "https://github.com/plstcharles/thelper/"
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}
html_sidebars = {
    "**": ["searchbox.html", "globaltoc.html", "sourcelink.html"],
}
html_short_title = "%s-%s" % (project, version)
html_use_smartypants = True

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'thelperdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'thelper.tex', 'thelper Documentation',
     'Pierre-Luc St-Charles', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'thelper', 'thelper Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'thelper', 'thelper Documentation',
     author, 'thelper', 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Extension configuration -------------------------------------------------
on_rtd = os.environ.get('READTHEDOCS') == 'True'

if on_rtd:
    autodoc_mock_imports = [
        'albumentations',
        'argparse',
        'augmentor',
        'cv2',
        'git',
        'h5py',
        'lz4',
        'matplotlib',
        'numpy',
        'PIL',
        'PIL.Image',
        'pip',
        'pynput',
        'pynput.keyboard',
        'scipy'
        'shapely',
        'sklearn',
        'sklearn.metrics',
        'tensorboardX',
        'torch',
        'torch.nn',
        'torch.nn.functional',
        'torch.optim',
        'torch.utils',
        'torch.utils.data',
        'torch.utils.data.sampler',
        'torch.utils.model_zoo',
        'torchvision',
        'torchvision.transforms',
        'torchvision.utils',
        'tqdm',
    ]


def skip(app, what, name, obj, skip, options):
    if name == "__init__" or name == "__call__" or name == "__getitem__":
        return False
    return skip


def run_apidoc(_):
    if on_rtd:
        argv = ["-M", "-o", ".", "../../thelper"]
    else:
        argv = ["-M", "-f", "-o", "./src/", "../thelper"]
    try:
        # Sphinx 1.7+
        from sphinx.ext import apidoc
        apidoc.main(argv)
    except ImportError:
        # Sphinx 1.6 (and earlier)
        from sphinx import apidoc
        argv.insert(0, apidoc.__file__)
        apidoc.main(argv)


def setup(app):
    app.connect("autodoc-skip-member", skip)
    app.connect("builder-inited", run_apidoc)
