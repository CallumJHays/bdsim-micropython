from setuptools import find_namespace_packages
import sys
sys.path.append('../../')
from shared_setup import setup_pkg  # nopep8


setup_pkg(
    name='bdsim.raspberrypi',
    packages=find_namespace_packages(),
    description='Raspberry Pi IO blocks',
    install_requires=['bdsim.core'],
)
