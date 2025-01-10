import os
import sys

def app_data_path(relative_path: str) -> str:
    """Get the path to the directory where the executable resides or data directory.
    
    Args:
        relative_path: The relative path to append to the application directory.
    
    Returns:
        str: The absolute path to the requested file or directory.
    """
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(application_path, relative_path) 