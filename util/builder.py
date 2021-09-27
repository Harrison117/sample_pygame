from abc import ABC, abstractmethod

from util.entities import *
from util.pygame_config import SCREEN_WIDTH, SCREEN_HEIGHT


class EntityBuilder(ABC):

    @abstractmethod
    def set_name(self, name):
        raise NotImplementedError

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
        """

        :param str name:
        """
        self._entity.name = name

    def set_pygame_img(self, img):
        """
        todo DEPENDENCIES: requires initialized entity image
        :param pygame.Surface img:
        """
        self._entity.image = img

        # todo DEPRECATE x_mid/y_mid (due to minimal usage)
        self._entity.x_mid = self._entity.image.get_width()//2
        self._entity.y_mid = self._entity.image.get_height()//2

    def set_init_pos(self, x_pos=-1, y_pos=-1):
        """
        todo DEPENDENCIES: requires initialized entity x/y position offset
        :param int x_pos:
        :param int y_pos:
        """
        if x_pos < 0 and y_pos < 0:
            self._entity.x_pos = (SCREEN_WIDTH // self._entity.x_pos_off) - self._entity.x_mid
            self._entity.y_pos = (SCREEN_HEIGHT // self._entity.y_pos_off) - self._entity.y_mid
        else:
            self._entity.x_pos = x_pos
            self._entity.y_pos = y_pos
        # self._entity.x_pos = x_pos
        # self._entity.y_pos = y_pos

    def set_init_state(self, is_alive=True):
        """

        :param is_alive:
        """
        self._entity.is_alive = is_alive

    def set_init_pos_offset(self, pos_off):
        """

        :param tuple[int, int] pos_off:
        """
        self._entity.x_pos_off = pos_off[0]
        self._entity.y_pos_off = pos_off[1]

    def set_mov_spd(self, mov_spd):
        """

        :param float mov_spd:
        """
        self._entity.mov_spd = mov_spd

    def set_init_mov_accel(self, accel):
        """

        :param tuple[int, int] accel:
        """
        self._entity.x_accel = accel[0]
        self._entity.y_accel = accel[1]

    def set_bullet_factory(self, bullet_factory):
        """

        :param BulletCreator bullet_factory:
        """
        self._entity._bullet_factory = bullet_factory

    def set_hit_box(self):
        """
        todo DEPENDENCIES: requires an initialized entity image
        """
        self._entity.rect = self._entity.image.get_rect()
        self._entity.rect.center = [
            self._entity.x_pos + self._entity.x_mid,
            self._entity.y_pos + self._entity.y_mid]

    def setup_weapon(self, weapon_factory, default_weapon):
        self._entity.setup_weapon(
            weapon_factory.build_weapon(self._entity),
            default_weapon)

    def build(self):
        return self._entity


class EnemyBuilder(PlayerBuilder):
    def __init__(self):
        super().__init__()
        self._entity = Enemy()

    def setup_hp_bar(self, status_bar_creator):
        """

        :param StatusBarDirector status_bar_creator:
        """
        self._entity.set_hp_bar(
            status_bar_creator.build_hp_bar(self._entity))


class BulletBuilder(PlayerBuilder):
    def __init__(self):
        super().__init__()
        self._entity = Bullet()

    def set_owner(self, entity):
        """

        :param Entity entity:
        """
        self._entity.set_owner(entity)

    def set_init_pos(self, x_pos=-1, y_pos=-1):
        """
        todo DEPENDENCIES: requires initialized entity owner and image, entity owner's  x_pos, x_mid
        :param int x_pos:
        :param int y_pos:
        """
        if x_pos < 0 and y_pos < 0:
            self._entity.x_pos = \
                self._entity.get_owner().x_pos \
                + self._entity.get_owner().x_mid \
                - self._entity.image.get_width()//2

            self._entity.y_pos = \
                self._entity.get_owner().y_pos \
                + self._entity.get_owner().y_mid \
                - self._entity.image.get_height()//2
        else:
            self._entity.x_pos = x_pos
            self._entity.y_pos = y_pos

    def set_dmg(self, dmg):
        """

        :param float dmg:
        """
        self._entity.set_dmg(dmg)

    def set_atk_spd(self, atk_spd):
        """

        :param float atk_spd:
        """
        self._entity.set_bullet_atk_spd(atk_spd)

    def set_weapon_type(self, weapon_type):
        """

        :param WeaponType weapon_type:
        """
        self._entity.set_weapon_type(weapon_type)

    def set_sound(self, sound):
        """

        :param pygame.mixer.Sound sound:
        """
        self._entity.sound = sound

    def build(self):
        return self._entity


class WeaponBuilder(object):
    def __init__(self):
        self._entity = Weapon()

    def set_bullet_factory(self, bullet_factory):
        """

        :param BuilderCreator bullet_factory:
        """
        self._entity.set_bullet_factory(bullet_factory)

    def set_owner(self, owner):
        """

        :param Entity owner:
        """
        self._entity.set_owner(owner)

    def build(self):
        return self._entity


class StatBuilder(object):
    def __init__(self):
        self._entity = Stats()

    def set_init_hp(self, hp):
        """

        :param int hp:
        """
        self._entity.update_hp(hp)

    def set_init_sp(self, sp):
        """

        :param int sp:
        """
        self._entity.update_sp(sp)

    def set_init_atk(self, atk):
        """

        :param int atk:
        """
        self._entity.update_atk(atk)

    def set_init_def(self, df):
        """

        :param int df:
        """
        self._entity.update_def(df)

    def set_init_agi(self, agi):
        """

        :param int agi:
        """
        self._entity.update_agi(agi)

    def set_init_luck(self, luck):
        """

        :param int luck:
        """
        self._entity.update_luck(luck)

    def set_init_res(self, nat_res, for_res, elem_res):
        """

        :param float nat_res:
        :param float for_res:
        :param float elem_res:
        """
        self._entity.update_resistance(nat_res, for_res, elem_res)


class StatusBarBuilder(object):
    def __init__(self):
        self._status_bar = StatusBar()

    def set_color(self, color):
        """

        :param pygame.Color color:
        """
        self._status_bar.set_color(color)

    def set_size(self, size):
        """

        :param tuple[int, int] size:
        """
        self._status_bar.update(
            self._status_bar.topleft,
            size)

    def set_pos(self, pos, x_off=0, y_off=0):
        """

        :param tuple[int, int] pos:
        :param int x_off:
        :param int y_off:
        """
        self._status_bar.update(
            (pos[0] + x_off, pos[1] + y_off),
            self._status_bar.size)

    def set_owner(self, entity):
        """

        :param Entity entity:
        """
        self._status_bar.set_owner(entity)

    def build(self):
        return self._status_bar
