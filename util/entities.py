import pygame
from util.pygame_config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN
from util.enums import WeaponType


class Entity(pygame.sprite.Sprite):
    def __init__(self, img=pygame.Surface((0, 0)), pos=(0, 0), is_alive=False, x_off=0, y_off=0, mov_spd=0.05, accel=0):
        super().__init__()
        """
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
        self.x_mid = 0
        self.y_mid = 0

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
            self.y_pos + self.y_mid
        ]

    def update(self, *args, **kwargs):
        self.update_movement()
        self.update_hit_box()


class Player(Entity):
    def __init__(self, atk_spd=1.0):
        super().__init__()
        self._move_direction_state = [False, False, False, False]

        self._base_atk_spd = atk_spd
        self._weapon = None
        self._current_weapon_type = None

    def fire(self):
        if self._weapon.firing():
            self._weapon.fire(self._base_atk_spd, self._current_weapon_type)

        self._weapon.update_bullets_fired()

    def switch_weapon(self, weapon_type):
        self._current_weapon_type = weapon_type

    def setup_weapon(self, weapon, default_weapon):
        self._weapon = weapon
        self._current_weapon_type = default_weapon

    def set_weapon_firing_state(self):
        self._weapon.set_firing_state()

    def set_movement_state(self, direction):
        self._move_direction_state[direction] = not self._move_direction_state[direction]

    def is_moving(self, direction):
        return self._move_direction_state[direction]

    def update(self):
        self.update_movement()
        self.update_hit_box()
        self.fire()


class Enemy(Entity):
    def __init__(self):
        super().__init__()

    def upper_bound_world_collide(self):
        return self.y_pos + (self.y_accel * self.mov_spd) <= 0

    def lower_bound_world_collide(self):
        return self.y_pos + (self.y_accel * self.mov_spd) >= SCREEN_HEIGHT - self.image.get_height()

    def y_accel_check(self):
        if self.upper_bound_world_collide():
            self.update_y_accel(1)

        elif self.lower_bound_world_collide():
            self.update_y_accel(-1)

    def update(self):
        self.y_accel_check()
        self.update_movement()
        self.update_hit_box()


class Bullet(Entity):
    def __init__(self, weapon_type=WeaponType.BASIC, atk_spd=1):
        super().__init__()
        self.sound = None
        self._weapon_type = weapon_type
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

    def get_bullet_atk_spd(self):
        return self._atk_spd

    def get_bullet_type(self):
        return self._weapon_type

    def set_weapon_type(self, weapon_type):
        self._weapon_type = weapon_type

    def set_bullet_atk_spd(self, atk_spd):
        self._atk_spd = atk_spd

    def set_owner(self, owner):
        self._owner = owner

    def get_owner(self):
        return self._owner


class Weapon:
    def __init__(self, atk_spd=0.25, dmg=10, atk_delay=1000):
        self._atk_spd = atk_spd
        # self._dmg = dmg

        self._atk_delay = atk_delay
        self._true_atk_delay = self._atk_delay
        self._last_shot_tick = pygame.time.get_ticks()

        self._owner = None
        self._bullet_factory = None
        self._bullet_stack = []
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
        self._bullet_stack.append(bullet)

    def bullet_stack_status(self):
        return self._bullet_stack

    def update_bullets_fired(self):
        new_stack = []
        for bullet in self._bullet_stack:
            if bullet.is_alive:
                new_stack.append(bullet)
                bullet.update_movement()
                bullet.draw_entity()
                bullet.check_bullet_state()

        self._bullet_stack = new_stack

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
