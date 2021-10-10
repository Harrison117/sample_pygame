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


class InputMoveEvent(Event):
    def __init__(self, direction=None, magnitude=None, is_player=False):
        self._is_player = is_player
        self._direction = direction
        self._magnitude = magnitude

    def get_data(self):
        return {
            'is_player': self._is_player,
            'direction': self._direction,
            'magnitude': self._magnitude,
        }


class TickEvent(Event):
    def get_data(self):
        pass


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
