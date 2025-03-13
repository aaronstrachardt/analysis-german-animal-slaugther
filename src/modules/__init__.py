"""
German animal slaughter analysis modules package.

This package contains modules for analyzing animal slaughter data in Germany.
"""

from . import config
from . import data_preparation
from . import data_validation
from . import visualization

__all__ = ['config', 'data_preparation', 'data_validation', 'visualization']
