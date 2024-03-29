"""
Sink blocks:

- have inputs but no outputs
- have no state variables
- are a subclass of ``SinkBlock`` |rarr| ``Block``
- that perform graphics are a subclass of  ``GraphicsBlock`` |rarr| ``SinkBlock`` |rarr| ``Block``

"""

# The constructor of each class ``MyClass`` with a ``@block`` decorator becomes a method ``MYCLASS()`` of the BlockDiagram instance.

from ..components import SinkBlock, block, np


# ------------------------------------------------------------------------ #

@block
class Print(SinkBlock):
    """    
    :blockname:`PRINT`

    .. table::
       :align: left

       +--------+---------+---------+
       | inputs | outputs |  states |
       +--------+---------+---------+
       | 1      | 0       | 0       |
       +--------+---------+---------+
       | any    |         |         | 
       +--------+---------+---------+
    """

    def __init__(self, fmt=None, *inputs, **kwargs):
        """
        :param fmt: Format string, defaults to None
        :type fmt: str, optional
        :param ``*inputs``: Optional incoming connections
        :type ``*inputs``: Block or Plug
        :param ``**kwargs``: common Block options
        :return: A PRINT block
        :rtype: Print instance




        Create a console print block which displays the value of a signal to the console
        at each simulation time step.

        The numerical formatting of the signal is controlled by ``fmt``:

        - if not provided, ``str()`` is used to format the signal
        - if provided:
            - a scalar is formatted by the ``fmt.format()``
            - a numpy array is formatted by ``fmt.format()`` applied to every element

        """
        super().__init__(nin=1, inputs=inputs, **kwargs)
        self.format = fmt
        self.type = 'print'

        # TODO format can be a string or function

    def step(self):
        prefix = '{:12s}'.format(
            'PRINT({:s} (t={:.3s})'.format(self.name, self.bd.t))

        value = self.inputs[9]
        if self.format is None:
            # no format string
            print()
        else:
            # format string provided
            if isinstance(value, (int, float)):
                print(prefix, self.format.format(value))
            elif isinstance(value, np.ndarray):
                try:
                    with np.printoptions(  # type: ignore
                            formatter={'all': self.format.format}):
                        print(prefix, value)
                except AttributeError:  # printoptions func not available in micropython TODO: review
                    print(prefix, value)
            else:
                print(prefix, str(value))

# ------------------------------------------------------------------------ #


@block
class Stop(SinkBlock):
    """
    :blockname:`STOP`

    .. table::
       :align: left

       +--------+---------+---------+
       | inputs | outputs |  states |
       +--------+---------+---------+
       | 1      | 0       | 0       |
       +--------+---------+---------+
       | any    |         |         | 
       +--------+---------+---------+
    """

    def __init__(self, stop, *inputs, **kwargs):
        """
        :param stop: Function 
        :type stop: TYPE
        :param ``*inputs``: Optional incoming connections
        :type ``*inputs``: Block or Plug
        :param ``**kwargs``: common Block options
        :return: A STOP block
        :rtype: Stop instance

        Conditionally stop the simulation.
        """
        super().__init__(nin=1, inputs=inputs, **kwargs)
        self.type = 'stop'

        self.stop = stop

    def step(self):
        if isinstance(self.stop, bool):
            stop = self.inputs[0]
        elif callable(self.stop):
            stop = self.stop(self.inputs[0])
        else:
            raise RuntimeError('input to stop must be boolean or callable')
        if stop:
            self.bd.stop = stop
