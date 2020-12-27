import os
from setuptools import find_namespace_packages
from pathlib import Path

from shared_setup import setup_pkg

here = Path(__file__).parent.absolute()

# just leave the types in the code
setup_pkg(
    name='bdsim.core',
    packages=find_namespace_packages(),
    description='Blocks, Wires and BlockDiagram classes for `bdsim`',  # TODO
    long_description=(here / 'README.md').open().read(),
    install_requires=[],
    here=here
)
