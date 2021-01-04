from setuptools import find_namespace_packages
import sys
sys.path.append('../../')
from shared_setup import setup_pkg  # nopep8

print('NAMESPACE_PKGS=', find_namespace_packages(include='bdsim.*'))

setup_pkg(
    name='bdsim.vision',
    packages=find_namespace_packages(include='bdsim.*'),
    description='OpenCV blocks for bdsim',
    install_requires=['bdsim.core', 'opencv-python']
)
