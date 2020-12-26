# `bdsim.core`

This is the core of bdsim. It includes Blocks, Wires and how they are connected as a BlockDiagram. This blockdiagram can be executed manually via `bd.exec()` but typically they are run by either the simulation package `bdsim.sim.simulate(bd, T=10)`, or by the realtime package `bdsim.realtime.run(bd)` - both of which are installed separately.
