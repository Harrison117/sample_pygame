import pygame
from util.pygame_config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN
from util.enums import WeaponType, DECREASE, INCREASE


class Stats(object):
    BASE_ATK = 0.1
    BASE_DEF = 0.1
    BASE_AGI = 0.1
    BASE_LUCK = 0.05

    def __init__(self, lvl=0, exp=0,
                 hp=100, sp=200, atk=10, df=10, agi=10, luck=10,
                 atk_spd=5, mov_spd=5,
                 nat_res=1, for_res=1, elem_res=1):
        self._level = lvl
        self._experience_points = exp

        self._health_points = hp
        self._shield_points = sp
        self._attack = atk
        self._defense = df
        self._agility = agi
        self._luck = luck
        self._attack_speed = atk_spd
        self._movement_speed = mov_spd

        self._natural_resistance = nat_res
        self._foreign_resistance = for_res
        self._element_resistance = elem_res

    def get_hp(self):
        return self._health_points

    def get_sp(self):
        return self._shield_points

    def get_atk(self):
        return self._health_points

    def get_def(self):
        return self._health_points

    def get_agi(self):
        return self._health_points

    def get_luck(self):
        return self._health_points

    def get_atk_spd(self):
        return self._attack_speed

    def get_mov_spd(self):
        return self._movement_speed

    def update_hp(self, hp):
        self._health_points = hp

    def update_sp(self, sp):
        self._shield_points = sp

    def update_atk(self, atk):
        self._attack = atk

    def update_def(self, df):
        self._defense = df

    def update_agi(self, agi):
        self._agility = agi

    def update_luck(self, luck):
        self._luck = luck

    def update_resistance(self, nat_res, for_res, elem_res):
        self._natural_resistance = nat_res
        self._foreign_resistance = for_res
        self._element_resistance = elem_res

    def calculate_damage(self):
        return Stats.BASE_ATK * self.get_atk()


class Entity(pygame.sprite.Sprite):
    def __init__(self,
                 img=pygame.Surface((0, 0)), pos=(0, 0),
                 is_alive=False, x_off=0, y_off=0, mov_spd=0.05, accel=0):
        super(Entity, self).__init__()
        """
        Base class for most visible objects in the game
        :param pygame.Surface img:
            pygame image reference of object.
            NOTE:
            Image position on the surface starts at the top-left corner of the image
        :param tuple pos:
            position of entity
        :param bool is_alive:
            state of the entity. Determines if affected by Bullet collision
        :param int x_off:
            x position offset of entity on the screen
        :param int y_off:
            y position offset of entity on the screen
        :param int mov_spd:
            movement speed of entity
        :param tuple accel:
            movement acceleration (magnitude and direction) of entity when moving
        """
        self.image = img
        self.rect = self.image.get_rect()

        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.x_pos_off = x_off
        self.y_pos_off = y_off
        self.mov_spd = mov_spd
        self.x_accel = accel
        self.y_accel = accel

        self.is_alive = is_alive

        # todo DEPRECATE
        self.img_x_mid = 0
        self.img_y_mid = 0
        self.x_mid = 0
        self.y_mid = 0

    # todo DEPRECATE (no need for manual blit-ing)
    def draw_entity(self):
        SCREEN.blit(self.image, (self.x_pos, self.y_pos))

    def update_x_pos(self):
        self.x_pos = self.x_pos + (self.x_accel * self.mov_spd)

    def update_y_pos(self):
        self.y_pos = self.y_pos + (self.y_accel * self.mov_spd)

    def update_x_accel(self, new_x_accel):
        self.x_accel = new_x_accel

    def update_y_accel(self, new_y_accel):
        self.y_accel = new_y_accel

    def get_x_pos(self):
        return self.x_pos

    def get_y_pos(self):
        return self.y_pos

    def get_x_mid(self):
        return self.x_mid

    def get_y_mid(self):
        return self.y_mid

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

    def x_pos_within_bounds(self):
        return 0 < self.x_pos + (self.x_accel * self.mov_spd) < SCREEN_WIDTH - self.image.get_width()

    def y_pos_within_bounds(self):
        return 0 < self.y_pos + (self.y_accel * self.mov_spd) < SCREEN_HEIGHT - self.image.get_height()

    def update_movement(self):
        if self.x_pos_within_bounds():
            self.update_x_pos()

        if self.y_pos_within_bounds():
            self.update_y_pos()

    def update_hit_box(self):
        self.rect.center = [
            self.x_pos + self.x_mid,
            self.y_pos + self.y_mid]

    def update(self, *args, **kwargs):
        self.update_movement()
        self.update_hit_box()


class Player(Entity):
    def __init__(self, atk_spd=1.0):
        super(Player, self).__init__()
        self._move_direction_state = [False, False, False, False]

        self._base_atk_spd = atk_spd
        self._weapon = None
        self._current_weapon_type = None

    def fire(self, enemy_group):
        if self._weapon.firing():
            self._weapon.fire_weapon(self._base_atk_spd, self._current_weapon_type)

        self._weapon.update_bullets_fired()
        self._weapon.check_bullet_collision(enemy_group)

    def switch_weapon(self, weapon_type):
        self._current_weapon_type = weapon_type

    def setup_weapon(self, weapon, default_weapon):
        self._weapon = weapon
        self._current_weapon_type = default_weapon

    def get_weapon(self):
        return self._weapon

    def set_weapon_firing_state(self):
        self._weapon.set_firing_state()

    def set_movement_state(self, direction):
        self._move_direction_state[direction] = not self._move_direction_state[direction]

    def is_moving(self, direction):
        return self._move_direction_state[direction]

    def update(self, enemy_group):
        self.update_movement()
        self.update_hit_box()
        self.fire(enemy_group)


class Enemy(Entity):
    def __init__(self,
                 stats=Stats(), hp_bar=None):
        super(Enemy, self).__init__()
        # self._stats = stats
        self._hp = 100.0
        self._max_hp = 100.0
        self._hp_bar = hp_bar

    def y_accel_check(self):
        if self.upper_bound_world_collide():
            self.update_y_accel(1)

        elif self.lower_bound_world_collide():
            self.update_y_accel(-1)

    def get_hp_bar(self):
        return self._hp_bar

    def get_hp(self):
        return self._hp

    def get_max_hp(self):
        return self._max_hp

    def set_hp_bar(self, hp_bar):
        self._hp_bar = hp_bar

    # todo transfer to Stat Class
    def update_hp(self, value, sign):
        self._hp += (value * sign)

    def upper_bound_world_collide(self):
        return self.y_pos + (self.y_accel * self.mov_spd) <= 0

    def lower_bound_world_collide(self):
        return self.y_pos + (self.y_accel * self.mov_spd) >= SCREEN_HEIGHT - self.image.get_height()

    def update(self):
        self.y_accel_check()
        self.update_movement()
        self.update_hit_box()
        self.get_hp_bar().update_status_bar(status_value=self._hp)


class Bullet(Entity):
    def __init__(self, weapon_type=WeaponType.BASIC, dmg=1, atk_spd=1):
        super(Bullet, self).__init__()
        self.sound = None
        self._weapon_type = weapon_type
        self._dmg = dmg
        self._atk_spd = atk_spd

        self._owner = None

    def update_bullet_atk_spd(self, atk_spd):
        self._atk_spd = atk_spd

    def update_y_pos(self):
        if self._weapon_type != WeaponType.LASER:
            self.y_pos = self.y_pos + (self.y_accel * self.mov_spd)
        else:
            self.y_pos = self._owner.get_y_pos() + self._owner.get_y_mid()

    def out_of_right_bounds(self):
        return self.x_pos + (self.x_accel * self.mov_spd) >= SCREEN_WIDTH - self.image.get_width()

    def check_bullet_state(self):
        if self.out_of_right_bounds():
            self.is_alive = False
            self.kill()

    def get_bullet_atk_spd(self):
        return self._atk_spd

    def get_bullet_type(self):
        return self._weapon_type

    def set_weapon_type(self, weapon_type):
        self._weapon_type = weapon_type

    def set_dmg(self, dmg):
        self._dmg = dmg

    def set_bullet_atk_spd(self, atk_spd):
        self._atk_spd = atk_spd

    def set_owner(self, owner):
        self._owner = owner

    def get_owner(self):
        return self._owner

    def get_dmg(self):
        return self._dmg

    def update(self):
        self.update_movement()
        self.update_hit_box()
        self.check_bullet_state()


class Weapon(object):
    def __init__(self, atk_spd=0.25, atk_delay=1000):
        self._atk_spd = atk_spd

        self._atk_delay = atk_delay
        self._true_atk_delay = self._atk_delay
        self._last_shot_tick = pygame.time.get_ticks()

        self._owner = None
        self._bullet_factory = None
        self._bullet_stack = pygame.sprite.Group()
        self._is_firing = False

    def fire(self, base_atk_spd, bullet_type):
        bullet = self._bullet_factory.build_bullet_type(bullet_type, self._owner)
        self.update_bullet_atk_spd(base_atk_spd, bullet.get_bullet_atk_spd())

        curr_shot_tick = pygame.time.get_ticks()
        if self.within_attack_delay(curr_shot_tick):
            bullet.sound.play()
            self.add_to_bullet_stack(bullet)
            self._last_shot_tick = curr_shot_tick

    def firing(self):
        return self._is_firing

    def add_to_bullet_stack(self, bullet):
        self._bullet_stack.add(bullet)

    def get_bullet_stack(self):
        return self._bullet_stack

    def update_bullets_fired(self):
        self._bullet_stack.update()

    def check_bullet_collision(self, enemy_group):
        for bullet in self._bullet_stack:
            #   note that dmg value on StatusBar will be normalized:
            #       normalized dmg value = width of enemy img/dmg value
            #   which will then be multiplied to the status bar width
            collided = pygame.sprite.spritecollide(bullet, enemy_group, False)
            if collided:
                for enemy in collided:
                    # todo implement stat methods
                    # todo implement stat methods
                    # enemy.get_stats().update_hp(
                    #   self.calculate_and_return_dmg(bullet.get_dmg()),
                    #   DECREASE)

                    enemy.update_hp(
                        self.calculate_and_return_dmg(bullet.get_dmg()),
                        DECREASE)

                    # print(enemy.get_hp())
                bullet.kill()

    def calculate_and_return_dmg(self, bullet_dmg):
        return bullet_dmg

    def update_bullet_atk_spd(self, base_atk_spd, bullet_atk_spd):
        self._atk_spd = bullet_atk_spd
        self._true_atk_delay = self._atk_delay * self._atk_spd * base_atk_spd

    def set_firing_state(self):
        self._is_firing = not self._is_firing

    def set_bullet_factory(self, bullet_factory):
        self._bullet_factory = bullet_factory

    def set_owner(self, owner):
        self._owner = owner

    def print_bullet_stack(self):
        print(self._bullet_stack)

    def within_attack_delay(self, curr_shot_tick):
        return curr_shot_tick - self._last_shot_tick >= self._true_atk_delay


# abstract class for movement and attack pattern of AI
class Pattern(object):
    pass


class StatusBar(pygame.rect.Rect):
    def __init__(self, pos=(0, 0), size=(0, 0),
                 owner=None, color=pygame.Color(0, 0, 0)):
        """
        :param tuple[int, int] pos:
        :param tuple[int, int] size:
        :param Entity owner:
        :param pygame.Color color:
        """
        super(StatusBar, self).__init__(pos, size)
        self._owner = owner
        self._color = color

    def update_status_bar(self, status_value=0, owner_type=None):
        # todo update rect based on enemy type (eg. common, elite, etc...)
        self.update(
            (self._owner.get_x_pos(), self._owner.get_y_pos() - self.height),
            (max(
                min(
                    status_value/self._owner.get_max_hp() * self._owner.get_width(),
                    self._owner.get_width()),
                0),
             self.height))

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color

    def set_owner(self, owner):
        self._owner = owner
