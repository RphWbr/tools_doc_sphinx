"""
tools_doc_sphinx
================

Package with tools for automatic generation of files used in Sphinx
documentation
"""

__version__ = "0.1.1"
__authors__ = "Raphaël Weber"


from os.path import dirname
from pkgutil import iter_modules

pkg_dir = dirname(__file__)
__path__ = [pkg_dir]

__all__ = []
for _, module_name, _ in iter_modules(__path__):
	__all__.append(module_name)
