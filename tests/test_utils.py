import pytest
import os
import sys
from unittest.mock import patch
from src.utils import app_data_path

def test_app_data_path_not_frozen():
    with patch('sys.frozen', False, create=True):
        path = app_data_path('test.txt')
        assert isinstance(path, str)
        assert path.endswith('test.txt')

def test_app_data_path_frozen():
    with patch('sys.frozen', True, create=True):
        with patch('sys.executable', '/path/to/exe'):
            path = app_data_path('test.txt')
            assert isinstance(path, str)
            assert path.endswith('test.txt')