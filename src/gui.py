import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os
from typing import Optional
from .dictionary_manager import DictionaryManager

class DictionaryApp:
    """GUI application for managing a personal dictionary.
    
    This class handles all GUI-related operations and user interactions,
    delegating data operations to the DictionaryManager.
    """
    
    def __init__(self, root: tk.Tk) -> None:
        """Initialize the GUI application.
        
        Args:
            root: The root Tkinter window.
        """
        self.root = root
        self.dict_manager = DictionaryManager()
        
        self._setup_window()
        self._create_widgets()
        self.populate_treeview()
        
    def _setup_window(self) -> None:
        """Configure the main window properties."""
        self.root.title("Dictionary App")
        
        # Add icon
        icon_path = 'icon.ico'
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
        self.root.iconbitmap(icon_path)
        
    def _create_widgets(self) -> None:
        """Create and configure all GUI widgets."""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Add search frame with grid layout instead of pack
        ttk.Label(main_frame, text="Search:").grid(row=0, column=0, sticky=tk.W)
        self.search_entry = ttk.Entry(main_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_entry.bind('<KeyRelease>', self.search_terms)

        # Term and definition entries (now aligned with search)
        ttk.Label(main_frame, text="Term:").grid(row=1, column=0, sticky=tk.W)
        self.term_entry = ttk.Entry(main_frame, width=30)
        self.term_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(main_frame, text="Definition:").grid(row=2, column=0, sticky=tk.W)
        self.definition_entry = ttk.Entry(main_frame, width=30)
        self.definition_entry.grid(row=2, column=1, padx=5, pady=5)

        # Create buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Add Term", command=self.add_term).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Term", command=self.edit_term).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Term", command=self.remove_term).pack(side=tk.LEFT, padx=5)

        # Create treeview
        self.treeview = ttk.Treeview(main_frame, columns=("Term", "Definition"), show="headings")
        self.treeview.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Bind double-click event
        self.treeview.bind('<Double-1>', self.on_double_click)

        # Configure treeview columns
        self.treeview.heading("Term", text="Term")
        self.treeview.heading("Definition", text="Definition")
        self.treeview.column("Term", width=150)
        self.treeview.column("Definition", width=300)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.treeview.yview)
        scrollbar.grid(row=4, column=2, sticky=(tk.N, tk.S))
        self.treeview.configure(yscrollcommand=scrollbar.set)

        # Configure window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def add_term(self) -> None:
        """Handle adding a new term or updating an existing one."""
        term = self.term_entry.get()
        definition = self.definition_entry.get()
        if term and definition:
            self.dict_manager.add_term(term, definition)
            self.term_entry.delete(0, tk.END)
            self.definition_entry.delete(0, tk.END)
            self.populate_treeview()
        else:
            messagebox.showerror("Error", "Term and Definition fields cannot be empty!")
    
    def populate_treeview(self) -> None:
        """Update the treeview with current dictionary contents."""
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        for term, definition in self.dict_manager.get_all_terms().items():
            self.treeview.insert("", tk.END, values=(term, definition))
    
    def remove_term(self) -> None:
        """Handle removing a selected term."""
        selected_items = self.treeview.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select a term to remove!")
            return
        
        selected_item = selected_items[0]
        term = self.treeview.item(selected_item)['values'][0]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to remove '{term}'?"):
            self.dict_manager.remove_term(term)
            self.populate_treeview()
    
    def on_closing(self) -> None:
        """Handle application closing."""
        self.dict_manager.save_data()
        self.root.destroy() 
    
    def search_terms(self, event: Optional[tk.Event] = None) -> None:
        """Filter the treeview based on search input (terms only).
        
        Args:
            event: Optional keyboard event that triggered the search.
        """
        search_text = self.search_entry.get().lower()
        
        # Clear current treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        # Populate with filtered results (searching only terms)
        for term, definition in self.dict_manager.get_all_terms().items():
            if search_text in term.lower():
                self.treeview.insert("", tk.END, values=(term, definition))
    
    def edit_term(self) -> None:
        """Handle editing the selected term."""
        selected_items = self.treeview.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select a term to edit!")
            return
        
        selected_item = selected_items[0]
        term, definition = self.treeview.item(selected_item)['values']
        
        # Populate entry fields with selected term
        self.term_entry.delete(0, tk.END)
        self.term_entry.insert(0, term)
        self.definition_entry.delete(0, tk.END)
        self.definition_entry.insert(0, definition)
        
        # Remove old term and update UI
        self.dict_manager.remove_term(term)
        self.populate_treeview()

    def on_double_click(self, event: tk.Event) -> None:
        """Handle double-click event on treeview item."""
        item = self.treeview.identify('item', event.x, event.y)
        if item:
            self.edit_term() 