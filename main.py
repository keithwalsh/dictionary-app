import tkinter as tk
from src.gui import DictionaryApp

def main() -> None:
    """Initialize and run the dictionary application."""
    root = tk.Tk()
    app = DictionaryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 