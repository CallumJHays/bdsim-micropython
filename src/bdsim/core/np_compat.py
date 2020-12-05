# numpy compatability module to share a common API between
# CPython numpy and MicroPython ulab

try:
    from ulab import *
    ndarray = array

# except ImportError:
#     from numpy import * # type: ignore