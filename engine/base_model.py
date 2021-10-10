from util.enums import *
from helper.helper import *


class Static(object):
    def __init__(self, pos=OrderedPair(0, 0).get_def(), off=OrderedPair(0, 0).get_def()):
        self._position = pos
        self._offset = off


class Movable(Static):
    def __init__(self, angle=OrderedPair(0, 0).get_def(), mov_spd=0, **static_properties):
        super(Movable, self).__init__(**static_properties)
        self._angle_vector = angle
        self._move_speed = mov_spd

    def update_position(self, *args, **kwargs):
        raise NotImplementedError

    def update_angle(self, *args, **kwargs):
        raise NotImplementedError


class Controllable(Movable):
    def __init__(self, **movable_properties):
        super(Controllable, self).__init__(**movable_properties)
        self._move_state = {
            LEFT: False,
            RIGHT: False,
            UP: False,
            DOWN: False,
        }

    def update_position(self):
        self._position = self._position + self._angle_vector * self._move_speed

    def update_angle(self, direction, magnitude):
        # to prevent move cancellation, a special case is defined
        if magnitude == STOP:
            if (direction == LEFT or direction == RIGHT) and \
                    not (self._move_state[LEFT] or self._move_state[RIGHT]):
                self._angle_vector[X_AXIS] = magnitude

            elif (direction == UP or direction == DOWN) and \
                    not (self._move_state[UP] or self._move_state[DOWN]):
                self._angle_vector[Y_AXIS] = magnitude

        else:
            if direction == LEFT or direction == RIGHT:
                self._angle_vector[X_AXIS] = magnitude

            elif direction == UP or direction == DOWN:
                self._angle_vector[Y_AXIS] = magnitude

    def set_move_state(self, direction):
        self._move_state[direction] = not self._move_state[direction]


class Projectile(object):
    def __init__(self, dmg=0.0):
        self._damage = dmg

    def calculate_damage(self):
        pass


class Destructible(object):
    def __init__(self, hp=100, sp=0):
        self._health_points = hp
        self._shield_points = sp

    def update_health_points(self, value, operation=1):
        self._health_points += value * operation

    def update_shield_points(self, value, operation=1):
        if value < self._shield_points:
            self._shield_points += value, operation
        else:
            self.update_health_points(value-self._shield_points, operation=operation)
            self._shield_points = 0


class Shooter(object):
    def __init__(self, weapon=None, bullet_type=None):
        self._weapon = weapon
        self._bullet_type = bullet_type

    def fire(self):
        if self._weapon:
            pass
