from setuptools import find_namespace_packages
from shared_setup import setup_pkg

setup_pkg(
    name='bdsim.vision',
    packages=find_namespace_packages(),
    description='OpenCV blocks for bdsim',
    install_requires=['bdsim.core', 'opencv']
)
