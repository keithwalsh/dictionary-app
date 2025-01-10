"""
Main entry point for the Dictionary Application.

This module initializes and launches the GUI application for managing
a personal dictionary of terms and definitions.

Author: Keith Walsh
Email: keithwalsh@gmail.com
GitHub: https://github.com/keithwalsh/dictionary-app
"""

import sys
import tkinter as tk
from typing import NoReturn

from src.gui import DictionaryApp


def main() -> NoReturn:
    """
    Initialize and run the dictionary application.
    
    Creates the main Tkinter window, initializes the application instance,
    and starts the main event loop. This function never returns normally
    as it enters the Tkinter main loop.
    
    Raises:
        TclError: If the Tkinter initialization fails
        ImportError: If required modules cannot be imported
    """
    try:
        root = tk.Tk()
        root.title("Dictionary Application")
        app = DictionaryApp(root)
        root.mainloop()
    except tk.TclError as e:
        print(f"Failed to initialize Tkinter: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 