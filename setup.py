from setuptools import setup, find_packages

setup(
    name="dictionary-app",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "tkinter",  # Usually comes with Python
    ],
    python_requires=">=3.9",
)
