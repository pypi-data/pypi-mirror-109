"""
Pyke: Makelike tool for Python
~=+~=+~=+~=+~=+~=+~=+~=+~=+~=+~=
"""

import click

__title__       = "pyke"
__author__      = "frissyn"
__version__     = "0.0.1a"
__license__     = "MIT"
__description__ = "Make-like build tool for Python."
__scripts__     = ["pyke = pyke:pykefile"]

@click.group()
def pykefile(): pass

@pykefile.command()
def cmd(): print("helloooo")
