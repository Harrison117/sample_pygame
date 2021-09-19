import pygame
from util.pygame_config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN


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
    def __init__(self):
        super().__init__()
        self._move_direction_state = [False, False, False, False]

        # in percentage
        self._atk_spd = 0.1

        # in ticks
        self._atk_delay = 1000
        self._true_atk_delay = self._atk_delay * self._atk_spd
        self._last_shot_tick = pygame.time.get_ticks()

        self._bullet_factory = None
        self._bullet_stack = []
        self._firing = False
        self._weapon = Weapon()

    def fire(self):
        if self._firing:
            curr_shot_tick = pygame.time.get_ticks()
            if curr_shot_tick - self._last_shot_tick >= self._true_atk_delay:
                # bullet = self._bullet_factory.fire_player_basic_bullet(self)
                bullet = self._bullet_factory.fire_player_mini_bullet(self)
                bullet.sound.play()
                self.add_to_bullet_stack(bullet)
                self._last_shot_tick = curr_shot_tick

    def set_fire_state(self):
        self._firing = not self._firing

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

    def set_movement_state(self, direction):
        self._move_direction_state[direction] = not self._move_direction_state[direction]

    def is_moving(self, direction):
        return self._move_direction_state[direction]

    def print_bullet_stack(self):
        print(self._bullet_stack)

    def update(self):
        self.update_movement()
        self.update_hit_box()

        self.fire()
        self.update_bullets_fired()


class Enemy(Entity):
    def __init__(self):
        super().__init__()

    def upper_bound_world_collide(self):
        return self.y_pos + (self.y_accel * self.mov_spd) < 0

    def lower_bound_world_collide(self):
        return self.y_pos + (self.y_accel * self.mov_spd) > SCREEN_HEIGHT - self.image.get_height()

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
    def __init__(self):
        super().__init__()
        self.sound = None

    def out_of_right_bounds(self):
        return self.x_pos + (self.x_accel * self.mov_spd) >= SCREEN_WIDTH - self.image.get_width()

    def check_bullet_state(self):
        if self.out_of_right_bounds():
            self.is_alive = False


class Weapon:
    def __init__(self, bullet_type=0, atk_spd=0.25, dmg=10, atk_delay=1000):
        self._bullet_type = bullet_type
        self._atk_spd = atk_spd
        self._dmg = dmg
        self._atk_delay = atk_delay

        self._owner = None
        self._bullet_factory = None
        self._bullet_stack = []

    def update_bullet_atk_spd(self, atk_spd):
        self._atk_spd = atk_spd

    def add_to_bullet_stack(self, bullet):
        self._bullet_stack.append(bullet)

    def bullet_stack_status(self):
        return self._bullet_stack

    def update_bullets_fired(self):
        pass

    def set_firing_state(self):
        pass

    def fire(self):
        pass

