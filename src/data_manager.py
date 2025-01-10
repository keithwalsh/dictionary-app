from typing import Dict, Any
import json
import os
from .utils import app_data_path

class JsonDataManager:
    """Handles JSON file operations for data persistence.
    
    This class provides a clean interface for loading and saving data to JSON files,
    with proper error handling and UTF-8 encoding support.
    """
    
    def __init__(self, filename: str) -> None:
        """Initialize the JSON data manager.
        
        Args:
            filename: Name of the JSON file to manage.
        """
        self.filepath = app_data_path(filename)
    
    def load(self) -> Dict[str, Any]:
        """Load data from JSON file with UTF-8 encoding.
        
        Returns:
            Dict[str, Any]: Dictionary containing loaded data.
        """
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save(self, data: Dict[str, Any]) -> None:
        """Save data to JSON file with UTF-8 encoding.
        
        Args:
            data: Dictionary containing data to save.
        """
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False) 