# Dictionary App

[![codecov](https://codecov.io/gh/keithwalsh/dictionary_app/branch/main/graph/badge.svg)](https://codecov.io/gh/keithwalsh/dictionary-app)
![Build](https://github.com/keithwalsh/react-spreadsheet-ts/actions/workflows/build.yml/badge.svg)

A simple desktop application built with Python and Tkinter that allows users to manage a personal dictionary of terms and definitions.

## Features

- Add new terms and definitions
- Edit existing entries by double-clicking or using the Edit button
- Search functionality for both terms and definitions
- Persistent storage using JSON with UTF-8 support
- Simple and intuitive interface
- Cross-platform compatibility

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)
- PyInstaller (optional, for creating executable)

## Installation

1. Clone the repository:
```
git clone https://github.com/keithwalsh/dictionary-app.git
cd dictionary-app
```
2. No additional package installation is required if you have Python 3.x installed.

## Usage

### Running from Source

1. Run the application:
```
python main.py
```

### Running the Executable (if built)

1. Download the latest release for your platform
2. Run the Dictionary executable

### Using the Application

- **Add Terms**: Enter a term and its definition in the respective fields and click "Add Term"
- **Edit Terms**: Double-click any entry or select it and click "Edit Term"
- **Remove Terms**: Select an entry and click "Remove Term"
- **Search**: Type in the search field to filter terms and definitions in real-time

## Data Storage

- Dictionary data is automatically saved to `data.json` in the application directory
- Data is stored using UTF-8 encoding for international character support
- Automatic saving occurs when closing the application

## Building the Executable

To create a standalone executable:

1. Install PyInstaller:
```
pip install pyinstaller
```
2. Build the executable:
```
pyinstaller Dictionary.spec
```
The executable will be created in the `dist` directory.