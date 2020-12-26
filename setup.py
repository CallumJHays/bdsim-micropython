"This is a meta-package grouping all subpackages required for typical bdsim use"

from shared_setup import setup_pkg
from pathlib import Path

setup_pkg(
    name='bdsim',
    packages=[],
    description='Simulate dynamic systems expressed in block diagram form using Python.',  # TODO
    long_description=open(
        str(Path(__file__).parent.absolute() / 'README.md')).read(),
    subpkg_deps=['core', 'matplotlib', 'server', 'sim',
                 'realtime', 'robots', 'webapp-full'])
