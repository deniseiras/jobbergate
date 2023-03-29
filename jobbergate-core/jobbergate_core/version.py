"""
Provide the version of the package.
"""
from importlib import metadata


__version__ = metadata.version(__package__ or __name__)