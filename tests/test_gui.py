import pytest
import tkinter as tk
from unittest.mock import Mock, patch, MagicMock
from src.gui import DictionaryApp

@pytest.fixture
def mock_root():
    root = Mock(spec=tk.Tk)
    # Add required tk attribute
    root.tk = Mock()
    return root

@pytest.fixture
def app(mock_root):
    # Mock all ttk widgets and messagebox
    with patch('src.gui.ttk') as mock_ttk, \
         patch('src.gui.messagebox') as mock_msgbox, \
         patch('src.gui.DictionaryManager') as mock_manager:
        
        # Setup mock ttk Frame and other widgets
        mock_frame = Mock()
        mock_ttk.Frame.return_value = mock_frame
        mock_frame.grid = Mock()
        
        # Create and configure mock treeview
        mock_treeview = Mock()
        mock_ttk.Treeview.return_value = mock_treeview
        mock_treeview.get_children.return_value = []
        
        app = DictionaryApp(mock_root)
        app.treeview = mock_treeview
        return app

def test_init(app, mock_root):
    assert app.root == mock_root
    assert app.dict_manager is not None

def test_add_term(app):
    # Setup
    app.term_entry = Mock()
    app.term_entry.get.return_value = "test"
    app.definition_entry = Mock()
    app.definition_entry.get.return_value = "definition"
    
    # Execute
    app.add_term()
    
    # Verify
    app.dict_manager.add_term.assert_called_once_with("test", "definition")
    app.term_entry.delete.assert_called_once_with(0, tk.END)
    app.definition_entry.delete.assert_called_once_with(0, tk.END)

def test_add_term_empty(app):
    # Setup
    app.term_entry = Mock()
    app.term_entry.get.return_value = ""
    app.definition_entry = Mock()
    app.definition_entry.get.return_value = ""
    
    with patch('tkinter.messagebox.showerror') as mock_error:
        # Execute
        app.add_term()
        
        # Verify
        mock_error.assert_called_once_with("Error", "Term and Definition fields cannot be empty!")
        app.dict_manager.add_term.assert_not_called()

def test_search_terms(app):
    # Setup
    app.search_entry = Mock()
    app.search_entry.get.return_value = "test"
    app.dict_manager.get_all_terms.return_value = {
        "test": "definition",
        "other": "other def"
    }
    
    # Mock treeview children
    app.treeview.get_children.return_value = ['item1', 'item2']
    
    # Execute
    app.search_terms()
    
    # Verify
    assert app.treeview.delete.call_count == len(app.treeview.get_children())
    app.treeview.insert.assert_called_with("", tk.END, values=("test", "definition"))

def test_on_closing(app):
    # Execute
    app.on_closing()
    
    # Verify
    app.dict_manager.save_data.assert_called_once()
    app.root.destroy.assert_called_once()

def test_edit_term(app):
    # Setup
    app.term_entry = Mock()
    app.definition_entry = Mock()
    app.treeview.selection.return_value = ['item1']
    app.treeview.item.return_value = {'values': ('test', 'definition')}
    
    # Execute
    app.edit_term()
    
    # Verify
    app.term_entry.delete.assert_called_with(0, tk.END)
    app.term_entry.insert.assert_called_with(0, 'test')
    app.definition_entry.delete.assert_called_with(0, tk.END)
    app.definition_entry.insert.assert_called_with(0, 'definition')
    app.dict_manager.remove_term.assert_called_with('test')

def test_edit_term_no_selection(app):
    # Setup
    app.treeview.selection.return_value = []
    
    with patch('tkinter.messagebox.showerror') as mock_error:
        # Execute
        app.edit_term()
        
        # Verify
        mock_error.assert_called_once_with("Error", "Please select a term to edit!") 

def test_remove_term(app):
    # Setup
    app.treeview.selection.return_value = ['item1']
    app.treeview.item.return_value = {'values': ['test_term', 'test_definition']}
    
    with patch('tkinter.messagebox.askyesno', return_value=True) as mock_confirm:
        # Execute
        app.remove_term()
        
        # Verify
        mock_confirm.assert_called_once()
        app.dict_manager.remove_term.assert_called_once_with('test_term')

def test_remove_term_no_selection(app):
    # Setup
    app.treeview.selection.return_value = []
    
    with patch('tkinter.messagebox.showerror') as mock_error:
        # Execute
        app.remove_term()
        
        # Verify
        mock_error.assert_called_once_with("Error", "Please select a term to remove!")
        app.dict_manager.remove_term.assert_not_called()

def test_remove_term_cancelled(app):
    # Setup
    app.treeview.selection.return_value = ['item1']
    app.treeview.item.return_value = {'values': ['test_term', 'test_definition']}
    
    with patch('tkinter.messagebox.askyesno', return_value=False) as mock_confirm:
        # Execute
        app.remove_term()
        
        # Verify
        mock_confirm.assert_called_once()
        app.dict_manager.remove_term.assert_not_called()

def test_on_double_click(app):
    # Setup
    mock_event = Mock()
    mock_event.x = 100
    mock_event.y = 100
    app.treeview.identify.return_value = 'item1'
    app.treeview.selection.return_value = ['item1']
    app.treeview.item.return_value = {'values': ('test', 'definition')}
    
    # Execute
    app.on_double_click(mock_event)
    
    # Verify
    app.treeview.identify.assert_called_once_with('item', mock_event.x, mock_event.y)
    app.treeview.selection.assert_called_once()

def test_on_double_click_no_item(app):
    # Setup
    mock_event = Mock()
    mock_event.x = 100
    mock_event.y = 100
    app.treeview.identify.return_value = None
    
    # Execute
    app.on_double_click(mock_event)
    
    # Verify
    app.treeview.identify.assert_called_once_with('item', mock_event.x, mock_event.y)

@patch('os.path.exists')
@patch('os.path.join')
def test_setup_window_frozen(mock_join, mock_exists, app):
    # Reset the mock to clear the initialization call
    app.root.iconbitmap.reset_mock()
    
    # Setup
    mock_join.return_value = 'path/to/icon.ico'
    mock_exists.return_value = True
    
    with patch('sys.frozen', True, create=True), \
         patch('sys._MEIPASS', 'meipass/path', create=True):
        # Execute
        app._setup_window()
        
        # Verify
        mock_join.assert_called_with('meipass/path', 'icon.ico')
        app.root.iconbitmap.assert_called_once_with('path/to/icon.ico')

@patch('os.path.exists')
@patch('os.path.join')
def test_setup_window_not_frozen(mock_join, mock_exists, app):
    # Reset the mock to clear the initialization call
    app.root.iconbitmap.reset_mock()
    mock_join.reset_mock()
    
    # Setup
    mock_join.return_value = 'path/to/icon.ico'
    mock_exists.return_value = True
    
    with patch('sys.frozen', False, create=True):
        # Execute
        app._setup_window()
        
        # Verify
        app.root.iconbitmap.assert_called_once_with('icon.ico')
        mock_join.assert_not_called()

def test_populate_treeview(app):
    # Setup
    app.dict_manager.get_all_terms.return_value = {
        'term1': 'def1',
        'term2': 'def2'
    }
    app.treeview.get_children.return_value = ['item1', 'item2']
    
    # Execute
    app.populate_treeview()
    
    # Verify
    assert app.treeview.delete.call_count == len(app.treeview.get_children())
    assert app.treeview.insert.call_count == 2
    app.treeview.insert.assert_any_call("", tk.END, values=('term1', 'def1'))
    app.treeview.insert.assert_any_call("", tk.END, values=('term2', 'def2')) 