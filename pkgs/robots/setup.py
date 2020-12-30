from setuptools import find_namespace_packages
import sys
sys.path.append('../../')
from shared_setup import setup_pkg  # nopep8

setup_pkg(
    name='bdsim.robots',
    packages=find_namespace_packages(),
    description='Robot geometry and dynamics blocks for bdsim',
    install_requires=['bdsim.core']
)
