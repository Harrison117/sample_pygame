from collections import defaultdict


class Listener(object):
    def __init__(self, event_mgr=None):
        if event_mgr:
            self._event_mgr = event_mgr
        else:
            raise AttributeError(f'EventManager expected; got {event_mgr.__class__.__name__} instead')


class Event(object):
    def get_data(self):
        raise NotImplementedError


class UpdateViewEvent(Event):
    def __init__(self, window=None):
        self._window = window

    def get_data(self):
        return {
            'window': self._window,
        }


class TransformViewEvent(Event):
    def __init__(self, color=None):
        self._color = color

    def get_data(self):
        return {
            'color': self._color,
        }


class DrawSpriteEvent(Event):
    def __init__(self, window=None):
        self._window = window

    def get_data(self):
        return {
            'window': self._window,
        }


class UpdateSpritePosEvent(Event):
    def __init__(self, pos=None):
        self._pos = pos

    def get_data(self):
        return {
            'pos': self._pos,
        }


class InputEvent(Event):
    def __init__(self, movement_vector=None, firing=False, auto_firing=False):
        self._movement_vector = movement_vector
        self._firing = firing
        self._auto_firing = auto_firing

    def get_data(self):
        return {
            'movement_vector': self._movement_vector,
            'firing': self._firing,
            'auto_firing': self._auto_firing,
        }


class TickEvent(Event):
    def __init__(self, ms_per_frame=None):
        self._ms_per_frame = ms_per_frame

    def get_data(self):
        return {
            'ms_per_frame': self._ms_per_frame,
        }


class QuitEvent(Event):
    def get_data(self):
        pass


class EventManager(object):
    """this object is responsible for coordinating most communication
    between the Model, View, and Controller."""

    def __init__(self):
        self._listeners = defaultdict()

    def add(self, event_class, listener_object):
        self._listeners.setdefault(event_class, list()).append(listener_object)

    def post(self, event):
        try:
            for listener in self._listeners[event.__class__]:
                listener(event)
        except KeyError:
            pass
