from setuptools import find_namespace_packages
import sys
sys.path.append('../../')
from shared_setup import setup_pkg  # nopep8

setup_pkg(
    name='bdsim.webapp-lite',
    packages=find_namespace_packages(),
    description='Slimmed-down Realtime Telemetry Webapp for bdsim',
    install_requires=['bdsim.core']
)
