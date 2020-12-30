from setuptools import find_namespace_packages
import sys
sys.path.append('../../')
from shared_setup import setup_pkg  # nopep8

setup_pkg(
    name='bdsim.realtime',
    packages=find_namespace_packages(),
    description='Realtime executor for `bdsim` in CPython',
    install_requires=['bdsim.core']
)
