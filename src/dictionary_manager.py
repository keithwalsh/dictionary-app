from typing import Dict
import json
import os
from .utils import app_data_path

class DictionaryManager:
    """Manages dictionary data operations including loading, saving, and modifications.
    
    This class handles all data-related operations for the dictionary application,
    providing a clean interface for data manipulation while handling file I/O operations.
    """
    
    def __init__(self) -> None:
        """Initialize the dictionary manager and load existing data."""
        self._dictionary: Dict[str, str] = self._load_data()
    
    def _load_data(self) -> Dict[str, str]:
        """Load dictionary data from JSON file with UTF-8 encoding.
        
        Returns:
            Dict[str, str]: Dictionary containing terms and definitions.
        """
        data_path = app_data_path('data.json')
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_data(self) -> None:
        """Save dictionary data to JSON file with UTF-8 encoding."""
        data_path = app_data_path('data.json')
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(self._dictionary, f, ensure_ascii=False)
    
    def add_term(self, term: str, definition: str) -> None:
        """Add a new term and definition to the dictionary.
        
        Args:
            term: The term to add.
            definition: The definition of the term.
        """
        self._dictionary[term] = definition
    
    def remove_term(self, term: str) -> None:
        """Remove a term from the dictionary.
        
        Args:
            term: The term to remove.
        """
        del self._dictionary[term]
    
    def get_all_terms(self) -> Dict[str, str]:
        """Get all terms and definitions.
        
        Returns:
            Dict[str, str]: Dictionary containing all terms and definitions.
        """
        return dict(self._dictionary) 