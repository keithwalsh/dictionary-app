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
        
        # Add placeholder text and bind focus events
        self.search_entry.insert(0, "Search terms...")
        self.search_entry.bind('<FocusIn>', self._on_search_focus_in)
        self.search_entry.bind('<FocusOut>', self._on_search_focus_out)
        
        # Set initial focus to search entry
        self.search_entry.focus()

        # Term and definition entries (now aligned with search)
        ttk.Label(main_frame, text="Term:").grid(row=1, column=0, sticky=tk.W)
        self.term_entry = ttk.Entry(main_frame, width=30)
        self.term_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(main_frame, text="Definition:").grid(row=2, column=0, sticky=tk.W)
        self.definition_entry = ttk.Entry(main_frame, width=30)
        self.definition_entry.grid(row=2, column=1, padx=5, pady=5)

        # Update Labels section - reduce padding between entry and button
        ttk.Label(main_frame, text="Labels:").grid(row=3, column=0, sticky=tk.W)
        self.label_entry = ttk.Entry(main_frame, width=30)
        self.label_entry.grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="+", width=3, command=self.add_label).grid(row=3, column=2)

        # Labels filter frame
        self.filter_frame = ttk.LabelFrame(main_frame, text="Filter by Labels", padding="5")
        self.filter_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.label_vars = {}  # Dictionary to store checkbox variables
        self.update_label_filters()

        # Create buttons (moved to row 5)
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Add Term", command=self.add_term).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Term", command=self.edit_term).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Term", command=self.remove_term).pack(side=tk.LEFT, padx=5)

        # Create treeview (moved to row 6)
        self.treeview = ttk.Treeview(main_frame, columns=("Term", "Definition", "Labels"), show="headings")
        self.treeview.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure treeview columns
        self.treeview.heading("Term", text="Term")
        self.treeview.heading("Definition", text="Definition")
        self.treeview.heading("Labels", text="Labels")
        self.treeview.column("Term", width=150)
        self.treeview.column("Definition", width=250)
        self.treeview.column("Labels", width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.treeview.yview)
        scrollbar.grid(row=6, column=2, sticky=(tk.N, tk.S))
        self.treeview.configure(yscrollcommand=scrollbar.set)

        # Configure window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def add_term(self) -> None:
        """Handle adding a new term or updating an existing one."""
        term = self.term_entry.get()
        definition = self.definition_entry.get()
        if term and definition:
            # Use stored labels if they exist (from edit operation)
            labels = getattr(self, 'current_labels', [])
            self.dict_manager.add_term(term, definition, labels)
            
            # Clear the stored labels
            if hasattr(self, 'current_labels'):
                del self.current_labels
            
            self.term_entry.delete(0, tk.END)
            self.definition_entry.delete(0, tk.END)
            self.populate_treeview()
        else:
            messagebox.showerror("Error", "Term and Definition fields cannot be empty!")
    
    def populate_treeview(self) -> None:
        """Update the treeview with current dictionary contents."""
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        
        terms = self.dict_manager.get_all_terms()
        for term, term_data in terms.items():
            labels_str = ", ".join(term_data.get("labels", []))
            self.treeview.insert("", tk.END, values=(
                term, 
                term_data["definition"], 
                labels_str
            ))
    
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
        
        # Populate with filtered results
        terms = self.dict_manager.get_all_terms()
        for term, term_data in terms.items():
            if search_text in term.lower():
                labels_str = ", ".join(term_data.get("labels", []))
                self.treeview.insert("", tk.END, values=(
                    term, 
                    term_data["definition"],
                    labels_str
                ))
    
    def edit_term(self) -> None:
        """Handle editing the selected term."""
        selected_items = self.treeview.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select a term to edit!")
            return
        
        selected_item = selected_items[0]
        values = self.treeview.item(selected_item)['values']
        term, definition, labels = values
        
        # Convert labels string back to list
        labels_list = [label.strip() for label in labels.split(',')] if labels else []
        
        # Populate entry fields with selected term
        self.term_entry.delete(0, tk.END)
        self.term_entry.insert(0, term)
        self.definition_entry.delete(0, tk.END)
        self.definition_entry.insert(0, definition)
        
        # Store the labels temporarily
        self.current_labels = labels_list
        
        # Remove old term and update UI
        self.dict_manager.remove_term(term)
        self.populate_treeview()

    def on_double_click(self, event: tk.Event) -> None:
        """Handle double-click event on treeview item."""
        item = self.treeview.identify('item', event.x, event.y)
        if item:
            self.edit_term() 

    def _on_search_focus_in(self, event: tk.Event) -> None:
        """Handle search entry focus in event.
        
        Args:
            event: The focus in event object.
        """
        if self.search_entry.get() == "Search terms...":
            self.search_entry.delete(0, tk.END)

    def _on_search_focus_out(self, event: tk.Event) -> None:
        """Handle search entry focus out event.
        
        Args:
            event: The focus out event object.
        """
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search terms...") 

    def update_label_filters(self) -> None:
        """Update the label filter checkboxes."""
        # Clear existing checkboxes
        for var, widget in self.label_vars.values():
            widget.grid_forget()
        self.label_vars.clear()

        # Create new checkboxes for all labels
        row = 0
        col = 0
        for label in sorted(self.dict_manager.get_all_labels()):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(
                self.filter_frame, 
                text=label, 
                variable=var, 
                command=self.apply_filters
            )
            cb.grid(row=row, column=col, padx=5, sticky=tk.W)
            self.label_vars[label] = (var, cb)  # Store both variable and widget
            col += 1
            if col > 3:  # 4 checkboxes per row
                col = 0
                row += 1

    def add_label(self) -> None:
        """Add a label to the current term."""
        selected_items = self.treeview.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select a term to add a label!")
            return

        label = self.label_entry.get().strip()
        if not label:
            messagebox.showerror("Error", "Please enter a label!")
            return

        selected_item = selected_items[0]
        term = self.treeview.item(selected_item)['values'][0]
        self.dict_manager.add_label_to_term(term, label)
        self.label_entry.delete(0, tk.END)
        self.update_label_filters()
        self.populate_treeview()

    def apply_filters(self) -> None:
        """Apply label filters to the treeview."""
        selected_labels = [
            label for label, (var, _) in self.label_vars.items() 
            if var.get()
        ]
        
        # Clear current treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        # Get filtered terms
        filtered_terms = self.dict_manager.get_terms_by_labels(selected_labels)
        
        # Populate treeview with filtered results
        for term, term_data in filtered_terms.items():
            labels_str = ", ".join(term_data.get("labels", []))
            self.treeview.insert("", tk.END, values=(
                term, 
                term_data["definition"], 
                labels_str
            )) 