from weakref import WeakKeyDictionary


class Event(object):
    def __init__(self):
        self.name = "Generic Event"


class EventManager(object):
    def __init__(self):
        self.listeners = WeakKeyDictionary()

    def register_listeners(self, listener):
        self.listeners[listener] = 1

    def unregister_listeners(self, listener):
        if listener in self.listeners.keys():
            del self.listeners[listener]

    # post the events in all listeners registered
    # todo targeted listeners
    def post(self, event):
        for listener in self.listeners.keys():
            listener.notify(event)
