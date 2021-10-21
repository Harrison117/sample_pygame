from typing import Dict, Any
from util.enums import *
from data_struct import OrderedPair


class Static(object):
    def __init__(self,
                 pos: OrderedPair = OrderedPair(0, 0).get_tuple(),
                 off: OrderedPair = OrderedPair(0, 0).get_tuple()):
        # todo director will dictate the actual params; default to None
        self._position = pos
        self._offset = off


class Movable(Static):
    def __init__(self,
                 angle: OrderedPair = OrderedPair(0, 0).get_tuple(),
                 mov_spd: int = 0,
                 **static_properties):
        # todo director will dictate the actual params; default to None
        super(Movable, self).__init__(**static_properties)
        self._angle_vector = angle
        self._move_speed = mov_spd

    def update_position(self, *args, **kwargs):
        raise NotImplementedError

    def update_angle(self, *args, **kwargs):
        raise NotImplementedError


class Controllable(Movable):
    def __init__(self,
                 move_state: Dict[Enum, bool] = None,
                 **movable_properties):
        super(Controllable, self).__init__(**movable_properties)
        # todo director will dictate the actual params; default to None
        # self._move_state = move_state
        self._move_state = {
            LEFT: False,
            RIGHT: False,
            UP: False,
            DOWN: False,
        }

    def update_position(self):
        self._position = self._position + self._angle_vector * self._move_speed

    def update_angle(self, direction, magnitude):
        # to prevent move cancellation when stopping, a special case is defined
        if magnitude == STOP:
            if self._moving_along_x(direction) and \
                    self._already_moving_along_x_axis():
                self._angle_vector[X_AXIS] = magnitude

            elif self._moving_along_y(direction) and \
                    self._already_moving_along_y_axis():
                self._angle_vector[Y_AXIS] = magnitude

        else:
            if self._moving_along_x(direction):
                self._angle_vector[X_AXIS] = magnitude

            elif self._moving_along_y(direction):
                self._angle_vector[Y_AXIS] = magnitude

    def set_move_state(self, direction):
        self._move_state[direction] = not self._move_state[direction]

    @staticmethod
    def _moving_along_x(direction):
        return direction == LEFT or direction == RIGHT

    def _already_moving_along_x_axis(self):
        return not (self._move_state[LEFT] or self._move_state[RIGHT])

    @staticmethod
    def _moving_along_y(direction):
        return direction == UP or direction == DOWN

    def _already_moving_along_y_axis(self):
        return not (self._move_state[UP] or self._move_state[DOWN])


class Projectile(object):
    def __init__(self, dmg=0.0):
        self._damage = dmg

    def calculate_damage(self):
        pass


class Destructible(object):
    def __init__(self,
                 hp: int = 100,
                 sp: int = 0,
                 max_hp: int = 100,
                 max_sp: int = 0,):
        # todo director will dictate the actual params; default to None
        # todo realistically, not all entities have shields; separate
        #   shield functionality
        self._health_points = hp
        self._max_hp = max_hp

        self._shield_points = sp
        self._max_sp = max_sp

    def update_health_points(self, value, operation=1):
        if 0 >= self._health_points + value * operation <= self._max_hp:
            self._health_points += value * operation

        else:
            if self._health_points + value * operation < 0:
                self._health_points = 0

            elif self._health_points + value * operation > self._max_hp:
                self._health_points = self._max_hp

    def update_shield_points(self, value, operation=1):
        if 0 >= self._shield_points + value * operation <= self._max_sp:
            self._shield_points += value * operation

        else:
            if self._shield_points + value * operation < 0:
                self.update_health_points(value-self._shield_points, operation=operation)
                self._shield_points = 0

            elif self._shield_points + value * operation > self._max_sp:
                self._shield_points = self._max_sp


class Shooter(object):
    def __init__(self,
                 weapon: Any = None,
                 bullet_type: Enum = None):
        self._weapon = weapon
        self._bullet_type = bullet_type

    def fire_weapon(self, **kwargs):
        raise NotImplementedError
