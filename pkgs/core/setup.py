from setuptools import find_namespace_packages
import sys
sys.path.append('../../')
from shared_setup import setup_pkg  # nopep8

setup_pkg(
    name='bdsim.core',
    packages=find_namespace_packages(),
    description='Blocks, Wires and BlockDiagram classes for `bdsim`',  # TODO
    install_requires=['ansitable']
)
