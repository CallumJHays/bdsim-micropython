from setuptools import find_namespace_packages
from shared_setup import setup_pkg

setup_pkg(
    name='bdsim.sim',
    packages=find_namespace_packages(),
    description='Simulation software for bdsim',
    install_requires=['bdsim.core']
)
