#!/bin/sh

set -o xtrace # display commands
set -e # crash on any error

# installs most packages relevant to bdsim development on an OS (in editable mode)
# the order is important so that deps are resolved locally where possible
for PKG in core matplotlib micropython realtime robots webapp-full server sim webapp-lite vision
do
  pip install -e pkgs/$PKG
done
