from abc import ABC, abstractmethod
from engine.model_entity import *


class EntityBuilder(ABC):
    @abstractmethod
    def build(self):
        pass


class StaticBuilder(ABC):
    @abstractmethod
    def set_init_position(self, pos):
        pass

    @abstractmethod
    def set_init_position_offset(self, off):
        pass


class MovableBuilder(ABC, StaticBuilder):
    @abstractmethod
    def set_init_angle(self, angle):
        pass

    @abstractmethod
    def set_init_move_speed(self, mov_spd):
        pass


class ControllableBuilder(ABC, MovableBuilder):
    pass


class BulletEntityBuilder(EntityBuilder):

    def __init__(self, event_mgr):
        self._entity = BulletEntity(event_mgr)

    def set_static_properties(self, position, offset):
        pass

    def set_movable_properties(self, angle, mov_spd):
        pass

    def build(self):
        pass
