import weakref


class WeakBoundMethod(object):
    def __init__(self, method):
        self._self = weakref.ref(method.__self__)
        self._func = method.__func__

    def __call__(self, *args, **kwargs):
        self._func(self._self(), *args, **kwargs)


# todo refactor OrderedPair so that it won't have a list-like behavior OR replace with pygame.vector2
class OrderedPair(list):
    """
    Class that allows vector-like operations like list+list, list-list, list*list,
    list//list, etc. Implements strict list length as it can only contain 2 values;
    x and y values.
    """
    def __init__(self, *sequence):
        if len(sequence) == 2:
            super(OrderedPair, self).__init__(tuple(sequence))

        else:
            raise ValueError(f'Ordered Pairs only have exactly 2 values; {len(sequence)} were given instead')

    def __add__(self, other):
        if isinstance(other, OrderedPair):
            x = self[0] + other[0]
            y = self[1] + other[1]
            return OrderedPair(x, y)

        elif isinstance(other, int):
            x = self[0] + other
            y = self[1] + other
            return OrderedPair(x, y)

        else:
            raise TypeError('Only operations using OrderedPairs or integers are valid')

    def __sub__(self, other):
        if isinstance(other, OrderedPair):
            x = self[0] - other[0]
            y = self[1] - other[1]
            return OrderedPair(x, y)

        elif isinstance(other, int):
            x = self[0] - other
            y = self[1] - other
            return OrderedPair(x, y)

        else:
            raise TypeError('Only operations using OrderedPairs or integers are valid')

    def __mul__(self, other):
        if isinstance(other, OrderedPair):
            x = self[0] * other[0]
            y = self[1] * other[1]
            return OrderedPair(x, y)

        elif isinstance(other, int):
            x = self[0] * int(other)
            y = self[1] * int(other)
            return OrderedPair(x, y)

        else:
            raise TypeError('Only operations using OrderedPairs or integers are valid')

    def __floordiv__(self, other):
        if isinstance(other, OrderedPair):
            x = self[0] // other[0]
            y = self[1] // other[1]
            return OrderedPair(x, y)

        elif isinstance(other, int):
            x = self[0] // other
            y = self[1] // other
            return OrderedPair(x, y)

        else:
            raise TypeError('Only operations using OrderedPairs or integers are valid')

    def __truediv__(self, other):
        return self.__floordiv__(other)

    # todo implement __iadd__, __isub__, __imul__, __ifloordiv__, __itruediv__

    def get_list(self):
        return list(self)

    def get_tuple(self):
        return tuple(self)
