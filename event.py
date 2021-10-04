from collections import defaultdict


class Event(object):
    def get_data(self):
        pass

    def __call__(self, *args, **kwargs):
        pass


class MoveEvent(Event):
    def __init__(self, key):
        self._key = key

    def get_data(self):
        return {'key': self._key}


class TickEvent(Event):
    def __init__(self):
        super(TickEvent, self).__init__()


class QuitEvent(Event):
    def __init__(self):
        super(QuitEvent, self).__init__()


class Listener(object):
    def __init__(self, event_mgr=None):
        if event_mgr:
            self._event_mgr = event_mgr
        else:
            raise AttributeError


class EventManager:
    """this object is responsible for coordinating most communication
    between the Model, View, and Controller."""

    def __init__(self):
        self._listeners = defaultdict()

    def add(self, event_class, listener_object):
        self._listeners.setdefault(event_class, list()).append(listener_object)
        print(self._listeners)

    def post(self, event):
        try:
            for listener in self._listeners[event.__class__]:
                listener(event)
        except KeyError:
            pass
