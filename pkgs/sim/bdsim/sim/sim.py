import re
from bdsim.core.blockdiagram import BlockDiagram
from scipy import integrate
from bdsim.core import Struct, Block, Plug, np

# print a progress bar
# https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console


def printProgressBar(fraction,
                     prefix='',
                     suffix='',
                     decimals=1,
                     length=50,
                     fill='█',
                     printEnd="\r"):

    percent = ("{0:." + str(decimals) + "f}").format(fraction * 100)
    filledLength = int(length * fraction)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r{} |{}| {}% {}'.format(
        prefix, bar, percent, suffix), end=printEnd)


def simulate(bd: BlockDiagram,
             T=10.0,
             dt=0.1,
             solver='RK45',
             block=False,
             checkfinite=True,
             watch=[],
             **kwargs):
    """
        Run the block diagram

        :param T: maximum integration time, defaults to 10.0
        :type T: float, optional
        :param dt: maximum time step, defaults to 0.1
        :type dt: float, optional
        :param solver: integration method, defaults to ``RK45``
        :type solver: str, optional
        :param block: matplotlib block at end of run, default False
        :type block: bool
        :param checkfinite: error if inf or nan on any wire, default True
        :type checkfinite: bool
        :param watch: list of input ports to log
        :type watch: list
        :param ``**kwargs``: passed to ``scipy.integrate``
        :return: time history of signals and states
        :rtype: Sim class

        Assumes that the network has been compiled.

        Graphics display in all blocks can be disabled using the `graphics`
        option to the ``BlockDiagram`` instance.


        Results are returned in a class with attributes:

        - ``t`` the time vector: ndarray, shape=(M,)
        - ``x`` is the state vector: ndarray, shape=(M,N)
        - ``xnames`` is a list of the names of the states corresponding to columns of `x`, eg. "plant.x0",
          defined for the block using the ``snames`` argument
        - ``uN'` for a watched input where N is the index of the port mentioned in the ``watch`` argument
        - ``unames`` is a list of the names of the input ports being watched, same order as in ``watch`` argument

        If there are no dynamic elements in the diagram, ie. no states, then ``x`` and ``xnames`` are not
        present.

        The ``watch`` argument is a list of one or more input ports whose value during simulation
        will be recorded.  The elements of the list can be:
            - a ``Block`` reference, which is interpretted as input port 0
            - a ``Plug`` reference, ie. a block with an index or attribute
            - a string of the form "block[i]" which is port i of the block named block.


        """

    assert bd.compiled, 'Network has not been compiled'
    bd.T = T
    bd.count = 0
    bd.stop = None  # allow any block to stop.BlockDiagram by setting this to the block's name
    bd.checkfinite = checkfinite

    # preproces the watchlist
    pluglist = []
    plugnamelist = []
    re_block = re.compile(r'(?P<name>[^[]+)(\[(?P<port>[0-9]+)\])')
    for n in watch:
        if isinstance(n, str):
            # a name was given, with optional port number
            m = re_block.match(n)
            name = m.group('name')
            port = m.group('port')
            b = bd.blocknames[name]
            plug = b[port]
        elif isinstance(n, Block):
            # a block was given, defaults to port 0
            plug = n[0]
        elif isinstance(n, Plug):
            # a plug was given
            plug = n
        else:
            raise Exception("unreachable")
        pluglist.append(plug)
        plugnamelist.append(str(plug))

    # try:
    # tell all blocks we're doing a.BlockDiagram
    bd.start()

    # get initial state from the stateful blocks
    x0 = bd.getstate()
    if len(x0) > 0:
        print('initial state x0 = ', x0)

    if bd.options.progress:
        printProgressBar(0,
                         prefix='Progress:',
                         suffix='complete',
                         length=60)

    # out = scipy.integrate.solve_ivp.BlockDiagram._deriv, args=(bd,), t_span=(0,T), y0=x0,
    #             method=solver, t_eval=np.linspace(0, T, 100), events=None, **kwargs)
    if len(x0) > 0:
        # block diagram contains states, solve it using numerical integration

        scipy_integrator = integrate.__dict__[
            solver]  # get user specified integrator

        integrator = scipy_integrator(lambda t, y: bd.evaluate(y, t),
                                      t0=0.0,
                                      y0=x0,
                                      t_bound=T,
                                      max_step=dt)

        # initialize list of time and states
        tlist = []
        xlist = []
        plist = [[] for p in pluglist]

        while integrator.status == 'running':

            # step the integrator, calls _deriv multiple times
            integrator.step()

            if integrator.status == 'failed':
                print('integration completed with failed status ')

            # stash the results
            tlist.append(integrator.t)
            xlist.append(integrator.y)

            # record the ports on the watchlist
            for i, p in enumerate(pluglist):
                plist[i].append(p.block.inputs[p.port])

            # update all blocks that need to know
            bd.step()

            # update the progress bar
            if bd.options.progress:
                printProgressBar(integrator.t / T,
                                 prefix='Progress:',
                                 suffix='complete',
                                 length=60)

            # has any block called a stop?
            if bd.stop is not None:
                print('\n--- stop requested at t={:f} by {:s}'.format(
                    bd.t, str(bd.stop)))
                break

        # save buffered data in a Struct
        out = Struct('results')
        out.t = np.array(tlist)
        out.x = np.array(xlist)
        out.xnames = bd.statenames
        for i, p in enumerate(pluglist):
            out['u' + str(i)] = np.array(plist[i])
        out.unames = plugnamelist
    else:
        # block diagram has no states

        # initialize list of time and states
        tlist = []
        plist = [[] for p in pluglist]

        for t in np.arange(0, T, dt):  # step through the time range

            # evaluate the block diagram
            bd.evaluate([], t)

            # stash the results
            tlist.append(t)

            # record the ports on the watchlist
            for i, p in enumerate(pluglist):
                plist[i].append(p.block.inputs[p.port])

            # update all blocks that need to know
            bd.step()

            # update the progress bar
            if bd.options.progress:
                printProgressBar(t / T,
                                 prefix='Progress:',
                                 suffix='complete',
                                 length=60)

            # has any block called a stop?
            if bd.stop is not None:
                print('\n--- stop requested at t={:f} by {:s}'.format(
                    bd.t, str(bd.stop)))
                break

        # save buffered data in a Struct
        out = Struct('results')
        out.t = np.array(tlist)
        for i, p in enumerate(pluglist):
            out['u' + str(i)] = np.array(plist[i])
        out.unames = plugnamelist

    if bd.options.progress:
        print('\r' + ' ' * 90 + '\r')

    # except RuntimeError as err:
    #     # bad things happens, print a message and return no result
    #     print('unrecoverable error in evaluation: ', err)
    #     return None

    # pause until all graphics blocks close
    bd.done(block=block)
    # print(bd.count, ' integrator steps')

    return out
