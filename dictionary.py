import json
import tkinter as tk
from tkinter import messagebox, ttk
import os
import sys

def app_data_path(relative_path):
    """Get the path to the directory where the executable resides or a designated data directory."""
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundled executable (e.g., using PyInstaller),
        # the sys.executable path will point to the executable file.
        application_path = os.path.dirname(sys.executable)
    else:
        # If run in a development environment, use the directory of the script.
        application_path = os.path.dirname(__file__)
    return os.path.join(application_path, relative_path)

class DictionaryApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.dictionary = self.load_data()

        self.root.title("Dictionary App")
        
        # Add icon
        icon_path = 'icon.ico'
        if hasattr(sys, '_MEIPASS'):  # Check if running as exe
            icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
        self.root.iconbitmap(icon_path)

        # Create an entry field for search
        self.search_entry = tk.Entry(root)
        self.search_entry.grid(row=0, column=1, padx=(40,0), sticky=tk.EW, pady=5)

        # Create a search button
        search_button = tk.Button(root, text="Search Term", command=self.search_term, width=12)
        search_button.grid(row=0, column=2, padx=(0, 5), pady=5, sticky=tk.W)

        # Create an entry field for the term
        self.term_entry = tk.Entry(root)
        self.term_entry.grid(row=1, column=1, padx=(40,0), sticky=tk.EW, pady=5)
        
        # Create an add button
        add_button = tk.Button(root, text="Add Term", command=self.add_term, width=12)
        add_button.grid(row=1, column=2, padx=(0, 5), pady=5, sticky=tk.W)
        
        # Create an entry field for the definition
        self.definition_entry = tk.Entry(root)
        self.definition_entry.grid(row=2, column=1, padx=(40,0), sticky=tk.EW, pady=5)
        
        # Create an edit button
        edit_button = tk.Button(root, text="Edit Term", command=self.edit_term, width=12)
        edit_button.grid(row=2, column=2, padx=(0, 5), pady=5, sticky=tk.W)


        # Treeview for displaying terms and descriptions
        self.treeview = ttk.Treeview(root, columns=("Term", "Description"), show="headings")
        self.treeview.heading("Term", text="Term")
        self.treeview.heading("Description", text="Description")
        self.treeview.column("Term", width=80)  # Adjust the width as needed
        self.treeview.column("Description", width=320)  # Adjust the width as needed
        self.treeview.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.populate_treeview()

    def load_data(self):
        """Load dictionary data from JSON file with UTF-8 encoding.
        
        Returns:
            dict: Dictionary containing terms and definitions.
        """
        data_path = app_data_path('data.json')
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            # Handle corrupted JSON file by returning empty dictionary
            return {}

    def save_data(self):
        """Save dictionary data to JSON file with UTF-8 encoding."""
        data_path = app_data_path('data.json')
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(self.dictionary, f, ensure_ascii=False)

    def populate_treeview(self):
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        for term, definition in self.dictionary.items():
            self.treeview.insert("", tk.END, values=(term, definition))

    def add_term(self):
        term = self.term_entry.get()
        definition = self.definition_entry.get()
        if term and definition:
            self.dictionary[term] = definition
            self.term_entry.delete(0, tk.END)
            self.definition_entry.delete(0, tk.END)
            self.populate_treeview()
        else:
            messagebox.showerror("Error", "Term and Definition fields cannot be empty!")

    def edit_term(self):
        selected_item = self.treeview.selection()
        if selected_item:
            term, definition = self.treeview.item(selected_item, "values")
            self.term_entry.insert(tk.END, term)
            self.definition_entry.insert(tk.END, definition)
            del self.dictionary[term]
            self.populate_treeview()

    def search_term(self):
        search_term = self.search_entry.get()
        for item in self.treeview.get_children():
            term, _ = self.treeview.item(item, "values")
            if term == search_term:
                self.treeview.selection_set(item)
                break

    def on_closing(self):
        self.save_data()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryApp(root)
    root.mainloop()
