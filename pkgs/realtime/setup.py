from setuptools import find_namespace_packages
from pathlib import Path
from shared_setup import setup_pkg

here = Path(__file__).parent.absolute()

setup_pkg(
    name='bdsim.realtime',
    packages=find_namespace_packages(),
    description='Realtime executor for `bdsim` in CPython',
    long_description=(here / 'README.md').open().read(),
    install_requires=['bdsim.core'],
    here=here
)