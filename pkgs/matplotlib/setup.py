from setuptools import find_namespace_packages
from pathlib import Path
from shared_setup import setup_pkg

setup_pkg(
    name='bdsim.matplotlib',
    packages=find_namespace_packages(),
    description='Matplotlib SCOPE displays for bdsim',
    install_requires=['bdsim.core', 'matplotlib', 'spatialmath-python']
)
