import pytest
import json
import os
from src.data_manager import JsonDataManager
from unittest.mock import mock_open, patch

@pytest.fixture
def data_manager():
    return JsonDataManager('test_data.json')

def test_load_empty_file(data_manager):
    with patch('builtins.open', mock_open(read_data="")):
        with patch('os.path.exists', return_value=False):
            data = data_manager.load()
            assert data == {}

def test_load_valid_json(data_manager):
    test_data = '{"key": "value"}'
    with patch('builtins.open', mock_open(read_data=test_data)):
        with patch('os.path.exists', return_value=True):
            data = data_manager.load()
            assert data == {"key": "value"}

def test_save_data(data_manager):
    test_data = {"key": "value"}
    mock_file = mock_open()
    with patch('builtins.open', mock_file):
        data_manager.save(test_data)
        mock_file.assert_called_once()