from setuptools import find_namespace_packages
from pathlib import Path

from shared_setup import setup_pkg

# just leave the types in the code
setup_pkg(
    name='bdsim.core',
    packages=find_namespace_packages(),
    description='Blocks, Wires and BlockDiagram classes for `bdsim`',  # TODO
    install_requires=[]
)
