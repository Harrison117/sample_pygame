from abc import ABC, abstractmethod

from util.entities import *
from util.pygame_config import SCREEN_WIDTH, SCREEN_HEIGHT


class EntityBuilder(ABC):
    @abstractmethod
    def set_name(self, name):
        pass

    @abstractmethod
    def set_pygame_img(self, img):
        pass

    @abstractmethod
    def set_init_pos(self):
        pass

    @abstractmethod
    def set_init_state(self):
        pass

    @abstractmethod
    def set_init_pos_offset(self, pos_off):
        pass

    @abstractmethod
    def set_mov_spd(self, default_mov_spd):
        pass

    @abstractmethod
    def set_init_mov_accel(self, default_accel):
        pass

    @abstractmethod
    def set_bullet_factory(self, bullet_factory):
        pass

    @abstractmethod
    def set_hit_box(self):
        pass

    @abstractmethod
    def build(self):
        pass


class PlayerBuilder(EntityBuilder):

    def __init__(self):
        self._entity = Player()

    def set_name(self, name):
        self._entity.name = name
        return self

    def set_pygame_img(self, img):
        self._entity.image = img

        self._entity.x_mid = self._entity.image.get_width()//2
        self._entity.y_mid = self._entity.image.get_height()//2
        return self

    def set_init_pos(self, x_pos=-1, y_pos=-1):
        if x_pos < 0 and y_pos < 0:
            self._entity.x_pos = (SCREEN_WIDTH // self._entity.x_pos_off) - self._entity.x_mid
            self._entity.y_pos = (SCREEN_HEIGHT // self._entity.y_pos_off) - self._entity.y_mid
        else:
            self._entity.x_pos = x_pos
            self._entity.y_pos = y_pos
        return self

    def set_init_state(self, is_alive=True):
        self._entity.is_alive = is_alive
        return self

    def set_init_pos_offset(self, pos_off):
        self._entity.x_pos_off = pos_off[0]
        self._entity.y_pos_off = pos_off[1]
        return self

    def set_mov_spd(self, mov_spd):
        self._entity.mov_spd = mov_spd
        return self

    def set_init_mov_accel(self, accel):
        self._entity.x_accel = accel[0]
        self._entity.y_accel = accel[1]
        return self

    def set_bullet_factory(self, bullet_factory):
        self._entity._bullet_factory = bullet_factory

    def set_hit_box(self):
        self._entity.rect = self._entity.image.get_rect()
        self._entity.rect.center = [
            self._entity.x_pos + self._entity.x_mid,
            self._entity.y_pos + self._entity.y_mid
        ]

    def build(self):
        return self._entity


class EnemyBuilder(PlayerBuilder):
    def __init__(self):
        super().__init__()
        self._entity = Enemy()


class BulletBuilder(PlayerBuilder):
    def __init__(self):
        super().__init__()
        self._entity = Bullet()
        self._owner = None

    def set_owner(self, entity):
        self._owner = entity

    def set_init_pos(self, x_pos=-1, y_pos=-1):
        if x_pos < 0 and y_pos < 0:
            self._entity.x_pos = self._owner.x_pos + self._owner.x_mid - self._entity.image.get_width()//2
            self._entity.y_pos = self._owner.y_pos + self._owner.y_mid - self._entity.image.get_height()//2
        else:
            self._entity.x_pos = x_pos
            self._entity.y_pos = y_pos

    def set_sound(self, sound):
        self._entity.sound = sound

    def set_atk_spd(self, atk_spd):
        self._entity.update_bullet_atk_spd(atk_spd)

    def build(self):
        return self._entity
