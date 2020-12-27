"""
Because python <3.5 does not support type-hints, we have a custom script to split the source code
into type-less code (.py) and type-hints (.pyi). This is run as a part of `shared_setup.py` if
the python version is less than 3.5 and installs to a hidden folder for distribution.

Subpackages installed in editable mode (`pip install -e`) generally accesses the source-code
directly, so in order for it to work as expected, the source code files must be watched and 
re-transpiled (as above) after any change. That is the purpose of this script.
"""

# from shared_setup import
