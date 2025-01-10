"""Dictionary application package.

This package provides a simple desktop application for managing
a personal dictionary of terms and definitions.
"""

from .gui import DictionaryApp
from .dictionary_manager import DictionaryManager

__all__ = ['DictionaryApp', 'DictionaryManager']
__version__ = '1.0.0' 