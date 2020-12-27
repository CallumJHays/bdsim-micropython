"This is a meta-package grouping all subpackages required for typical bdsim use"

from shared_setup import setup_pkg
from pathlib import Path

here = Path(__file__).parent.absolute()

setup_pkg(
    name='bdsim',
    packages=[],
    description='Simulate dynamic systems expressed in block diagram form using Python.',  # TODO
    long_description=(here / 'README.md').open().read(),
    install_requires=['core', 'matplotlib', 'server', 'sim',
                      'realtime', 'robots', 'webapp-full'],
    here=here)
