from setuptools import find_namespace_packages
from shared_setup import setup_pkg


setup_pkg(
    name='bdsim.raspberrypi',
    packages=find_namespace_packages(),
    description='Raspberry Pi IO blocks',
    install_requires=['bdsim.core'],
)
