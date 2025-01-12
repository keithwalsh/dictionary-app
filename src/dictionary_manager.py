from typing import Dict, List, Set, Optional, Any
from .data_manager import JsonDataManager

class DictionaryManager:
    """Manages dictionary data operations including loading, saving, and modifications.
    
    This class handles all data-related operations for the dictionary application,
    delegating file I/O operations to the JsonDataManager.
    """
    
    def __init__(self) -> None:
        """Initialize the dictionary manager and load existing data."""
        self._data_manager = JsonDataManager('data.json')
        self._dictionary: Dict[str, Dict[str, Any]] = self._data_manager.load()
    
    def save_data(self) -> None:
        """Save dictionary data to storage."""
        self._data_manager.save(self._dictionary)
    
    def add_term(self, term: str, definition: str, labels: Optional[List[str]] = None) -> None:
        """Add a new term and definition to the dictionary.
        
        Args:
            term: The term to add.
            definition: The definition of the term.
            labels: Optional list of labels for the term.
        """
        self._dictionary[term] = {
            "definition": definition,
            "labels": labels or []
        }
    
    def remove_term(self, term: str) -> None:
        """Remove a term from the dictionary.
        
        Args:
            term: The term to remove.
        """
        del self._dictionary[term]
    
    def get_all_terms(self) -> Dict[str, Dict[str, Any]]:
        """Get all terms and their data.
        
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary containing all terms with their definitions and labels.
        """
        return dict(self._dictionary)
    
    def add_label_to_term(self, term: str, label: str) -> None:
        """Add a label to an existing term.
        
        Args:
            term: The term to add the label to.
            label: The label to add.
        """
        if term in self._dictionary:
            if "labels" not in self._dictionary[term]:
                self._dictionary[term]["labels"] = []
            if label not in self._dictionary[term]["labels"]:
                self._dictionary[term]["labels"].append(label)
    
    def remove_label_from_term(self, term: str, label: str) -> None:
        """Remove a label from a term.
        
        Args:
            term: The term to remove the label from.
            label: The label to remove.
        """
        if term in self._dictionary and "labels" in self._dictionary[term]:
            self._dictionary[term]["labels"].remove(label)
    
    def get_all_labels(self) -> Set[str]:
        """Get all unique labels used in the dictionary.
        
        Returns:
            Set[str]: Set of all unique labels.
        """
        labels = set()
        for term_data in self._dictionary.values():
            labels.update(term_data.get("labels", []))
        return labels
    
    def get_terms_by_labels(self, labels: List[str]) -> Dict[str, Dict[str, Any]]:
        """Get all terms that match any of the provided labels.
        
        Args:
            labels: List of labels to filter by.
        
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary of terms that match the labels.
        """
        if not labels:  # If no labels specified, return all terms
            return dict(self._dictionary)
        
        filtered_terms = {}
        for term, term_data in self._dictionary.items():
            term_labels = term_data.get("labels", [])
            if any(label in term_labels for label in labels):
                filtered_terms[term] = term_data
        return filtered_terms
    
    def get_term_definition(self, term: str) -> str:
        """Get the definition for a specific term.
        
        Args:
            term: The term to get the definition for.
        
        Returns:
            str: The definition of the term.
        """
        return self._dictionary[term]["definition"]
    
    def get_term_labels(self, term: str) -> List[str]:
        """Get the labels for a specific term.
        
        Args:
            term: The term to get the labels for.
        
        Returns:
            List[str]: The labels associated with the term.
        """
        return self._dictionary[term].get("labels", []) 