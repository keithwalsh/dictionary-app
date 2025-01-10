from typing import Dict
from .data_manager import JsonDataManager

class DictionaryManager:
    """Manages dictionary data operations including loading, saving, and modifications.
    
    This class handles all data-related operations for the dictionary application,
    delegating file I/O operations to the JsonDataManager.
    """
    
    def __init__(self) -> None:
        """Initialize the dictionary manager and load existing data."""
        self._data_manager = JsonDataManager('data.json')
        self._dictionary: Dict[str, str] = self._data_manager.load()
    
    def save_data(self) -> None:
        """Save dictionary data to storage."""
        self._data_manager.save(self._dictionary)
    
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