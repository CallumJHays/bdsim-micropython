from setuptools import find_namespace_packages
from pathlib import Path
import sys

here = Path(__file__).parent.absolute()

# append the top-level of this repo to path so we can import the setup.py
sys.path.append(str(here / '../..'))

from setup import setup_pkg  # nopep8

setup_pkg(
    name='bdsim.webapp-lite',
    packages=find_namespace_packages(),
    description='Realtime Telemetry Webapp for bdsim',
    long_description=(here / 'README.md').open().read(),
    install_requires=['bdsim.core'],
    here=here
)
