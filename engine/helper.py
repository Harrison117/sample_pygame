import weakref


class WeakBoundMethod(object):
    def __init__(self, method):
        self._self = weakref.ref(method.__self__)
        self._func = method.__func__

    def __call__(self, *args, **kwargs):
        self._func(self._self(), *args, **kwargs)
