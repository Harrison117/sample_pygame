from enum import Enum


class WeaponType(Enum):
    NONE = 0
    BASIC = 1
    MINI = 2
    MISSILE = 3
    LASER = 4


class ShipType(Enum):
    COMMON = 0
    ELITE = 1
    BOSS = 2
    PLAYER = 3


class EntityCategory(Enum):
    MECH = 0
    NATURE = 1


class Status(Enum):
    BURNING = 0
    BLAZING = 1
    SLOW = 2
    FREEZING = 3
    RES_UP = 4
    RES_DOWN = 5
    ATK_UP = 6
    ATK_DOWN = 7


LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

STOP = 0
DECREASE = LEFT_MAGNITUDE = UP_MAGNITUDE = -1
INCREASE = RIGHT_MAGNITUDE = DOWN_MAGNITUDE = 1

X_AXIS = 0
Y_AXIS = 1
