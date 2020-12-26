#!/bin/sh

set -o xtrace # display commands
set -e # crash on any error

# installs most packages relevant to bdsim development on an OS (in editable mode)
# the order is important so that deps are resolved locally
for PKG in core matplotlib micropython realtime robots server webapp-full server sim
do
  pip install --no-index -e pkgs/$PKG
done
