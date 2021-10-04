from enum import Enum


class WeaponType(Enum):
    NONE = 0
    BASIC = 1
    MINI = 2
    MISSILE = 3
    LASER = 4


LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

STOP = 0
DECREASE = LEFT_MAGNITUDE = UP_MAGNITUDE = -1
INCREASE = RIGHT_MAGNITUDE = DOWN_MAGNITUDE = 1

X_AXIS = 0
Y_AXIS = 1
