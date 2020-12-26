from setuptools import find_namespace_packages
from pathlib import Path
from shared_setup import setup_pkg

here = Path(__file__).parent.absolute()

setup_pkg(
    name='bdsim.matplotlib',
    packages=find_namespace_packages(),
    description='Matplotlib SCOPE displays for bdsim',
    long_description=open(str(here / 'README.md')).read(),
    # TODO: , 'matplotlib', 'spatialmath-python']
    install_requires=['bdsim.core']
)
