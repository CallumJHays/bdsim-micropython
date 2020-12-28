# numpy compatability module to share a common API between
# CPython numpy and MicroPython ulab
from typing import List

try:
    _float = float  # type: ignore
    # see float assignment below
    from ulab import *
    import math

    _DType = int  # hidden by default from ulab export
    # use the original float class rather than the shadowing ulab dtype (an enum int)
    float: type = _float

    # def isfinite(a: array):
    #     if len(a) > 0:
    #         if isinstance(a[0], array):
    #             return array(isfinite(x) for x in a)  # type: ignore
    #             # because pylance doesn't understand the above type-guard if statement
    #         else:
    #             return array(math.isfinite(x) for x in a)  # type: ignore
    #             # same as above
    #     else:
    #         return array([])

    # this is a stripped down version of RClass (used by np.r_[...etc])
    # it doesn't include support for string arguments as the first index element
    class RClass:
        """
        Translates slice objects to concatenation along the first axis.
        This is a simple way to build up arrays quickly. There are two use cases.
        1. If the index expression contains comma separated arrays, then stack
        them along their first axis.
        2. If the index expression contains slice notation or scalars then create
        a 1-D array with a range indicated by the slice notation.
        If slice notation is used, the syntax ``start:stop:step`` is equivalent
        to ``np.arange(start, stop, step)`` inside of the brackets. However, if
        ``step`` is an imaginary number (i.e. 100j) then its integer portion is
        interpreted as a number-of-points desired and the start and stop are
        inclusive. In other words ``start:stop:stepj`` is interpreted as
        ``np.linspace(start, stop, step, endpoint=1)`` inside of the brackets.
        After expansion of slice notation, all comma separated sequences are
        concatenated together.

        Parameters
        ----------
        Not a function, so takes no parameters
        Returns
        -------
        A concatenated array or matrix.
        See Also
        --------
        concatenate : Join a sequence of arrays along an existing axis.
        c_ : Translates slice objects to concatenation along the second axis.
        Examples
        --------
        >>> np.r_[np.array([1,2,3]), 0, 0, np.array([4,5,6])]
        array([1, 2, 3, ..., 4, 5, 6])
        >>> np.r_[-1:1:6j, [0]*3, 5, 6]
        array([-1. , -0.6, -0.2,  0.2,  0.6,  1. ,  0. ,  0. ,  0. ,  5. ,  6. ])
        """

        def __getitem__(self, key):

            if not isinstance(key, tuple):
                key = (key,)

            objs: List[array] = []
            scalars: List[int] = []
            arraytypes: List[_DType] = []
            scalartypes: List[_DType] = []

            # these may get overridden in following loop
            axis = 0

            for idx, item in enumerate(key):
                scalar = False
                if isinstance(item, slice):
                    step = item.step
                    start = item.start
                    stop = item.stop
                    if start is None:
                        start = 0
                    if step is None:
                        step = 1
                    if isinstance(step, complex):
                        size = int(abs(step))
                        newobj = linspace(start, stop, num=size)
                    else:
                        newobj = arange(start, stop, step)

                # if is number
                elif isinstance(item, (int, float, complex)):
                    newobj = array([item])
                    scalars.append(len(objs))
                    scalar = True
                    scalartypes.append(newobj.dtype())

                else:
                    raise Exception("index object %s of type %s is not supported by r_[]" % (
                        str(item), type(item)))

                objs.append(newobj)
                if not scalar and isinstance(newobj, array):
                    arraytypes.append(newobj.dtype())

            # Ensure that scalars won't up-cast unless warranted
            # TODO: ensure that this actually works for dtype coercion
            # likelihood is we're going to have to do some funky logic for this
            final_dtype = max(arraytypes + scalartypes)
            if final_dtype is not None:
                for idx in scalars:
                    objs[idx] = array(objs[idx], dtype=final_dtype)

            res = concatenate(tuple(objs), axis=axis)

            return res

        # this seems weird - not sure what it's for
        def __len__(self):
            return 0

    r_ = RClass()

except ImportError:
    # from numpy import *  # type: ignore
    pass
