"""
ScotusUtils: Tools for scraping, storing & analyzing SCOTUS Data
================================================================

Documentation is available in the docstrings

Contents
--------
ScotusUtils provides the following:

Subpackages
-----------
Using any of these subpackages requires an explicit import.  For example,
``import scotusutils.webtools``.

::

 dbtools                      --- Interfacing with 
 pdftools                     --- Tools for Text Extraction from PDFs
 webtools                     --- Scraping SCOTUS content from the web

"""
from scotusutils import utils
from scotusutils.utils import _MAIN_DIR, _CONFIG_DIR
from scotusutils import configtools
from scotusutils import webtools
from scotusutils import dbtools
