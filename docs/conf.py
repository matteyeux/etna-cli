import os
import sys

sys.path.append(".")

project = "etna-cli"
copyright = "2020, matteyeux"
author = "matteyeux"


#release = get some shit done to print current release
version = "replace_me"

# -- General configuration ---------------------------------------------------
needs_sphinx = "2.0"
extensions = ["sphinx.ext.autodoc", "sphinx_click.ext", "sphinxcontrib.contentui"]


templates_path = ["_templates" "."]
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

master_doc = "index"
language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "env", ".gitignore", "Makefile", "requirements.txt", "README.md", "etnawrapper/README.rst"]
pygments_style = "colorful"

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_theme_options = {"style_nav_header_background": "#3f51b5"}
html_static_path = []

html_context = {
  "display_github": True, # Add 'Edit on Github' link instead of 'View page source'
  "github_user": "matteyeux",
  "github_repo": "etna-cli",
  "github_version": "master",
  "conf_py_path": "/docs/",
  "source_suffix": source_suffix,
}

html_sidebars = {"**": ["globaltoc.html", "relations.html", "sourcelink.html"]}

# workaround to remove multiple build warnings caused by upstream bug.
from recommonmark.parser import CommonMarkParser

class CustomCommonMarkParser(CommonMarkParser):
    def visit_document(self, node):
        pass

def setup(app) -> None:
     app.add_source_parser(CustomCommonMarkParser)


os.system("git clone https://github.com/tbobm/etnawrapper")
