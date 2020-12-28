from setuptools import find_namespace_packages
from setup import setup_pkg

setup_pkg(
    name='bdsim.webapp-lite',
    packages=find_namespace_packages(),
    description='Slimmed-down Realtime Telemetry Webapp for bdsim',
    install_requires=['bdsim.core']
)
