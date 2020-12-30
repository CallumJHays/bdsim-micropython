"This is a meta-package grouping all subpackages required for typical bdsim use"

from shared_setup import setup_pkg
from pathlib import Path

here = Path(__file__).parent.absolute()

setup_pkg(
    name='bdsim',
    packages=[],
    description='Simulate dynamic systems expressed in block diagram form using Python.',  # TODO
    install_requires=['bdsim.core', 'bdsim.matplotlib', 'bdsim.server', 'bdsim.sim',
                      'bdsim.realtime', 'bdsim.robots', 'bdsim.webapp-full'],
    extras_require={
        # include the vision package if necessary (needs OPENCV)
        'vision': ['bdsim.vision']
    })
