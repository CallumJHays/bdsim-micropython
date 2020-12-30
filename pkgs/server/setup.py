from setuptools import find_namespace_packages
import sys
sys.path.append('../../')
from shared_setup import setup_pkg  # nopep8

setup_pkg(
    name='bdsim.server',
    packages=find_namespace_packages(),
    description='Data logging and Webapp proxy server for bdsim',
    install_requires=['bdsim.core', 'bdsim.webapp-full']
)
