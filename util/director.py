import pygame
import random
from util.pygame_config import SCREEN_WIDTH, SCREEN_HEIGHT
from util.builder import PlayerBuilder, EnemyBuilder, BulletBuilder


class PlayerCreator:
    def build_player(self, builder):
        builder.set_name("player")
        builder.set_pygame_img(pygame.image.load('player.png'))
        builder.set_init_pos_offset((6, 2))
        builder.set_init_pos()
        builder.set_init_mov_accel((0, 0))
        builder.set_mov_spd(0.05)
        builder.set_bullet_factory(BulletCreator())
        builder.set_hit_box()
        return builder.build()


class EnemyCreator:
    def build_basic_enemy(self, builder):
        img = pygame.image.load('enemy.png')
        img_x_mid = img.get_width() // 2
        pos_offset = (6, 2)

        builder.set_pygame_img(img)
        builder.set_init_pos_offset(pos_offset)
        builder.set_init_pos(
            x_pos=(SCREEN_WIDTH // pos_offset[0] - img_x_mid) * 5,
            y_pos=random.randint(0, SCREEN_HEIGHT - img.get_height()))
        builder.set_init_mov_accel(
            (0,
             random.choice([-1, 1])))
        builder.set_mov_spd(0.02)
        builder.set_hit_box()
        return builder.build()


class BulletCreator:
    def fire_player_basic_bullet(self, entity):
        builder = BulletBuilder()
        builder.set_owner(entity)
        builder.set_pygame_img(pygame.image.load('player_basic_bullet.png'))
        builder.set_init_pos()
        builder.set_init_mov_accel((1, 0))
        builder.set_mov_spd(0.1)
        builder.set_init_state()
        builder.set_atk_spd(0.25)
        builder.set_sound(pygame.mixer.Sound('fire1.wav'))
        return builder.build()

    def fire_player_mini_bullet(self, entity):
        builder = BulletBuilder()
        builder.set_owner(entity)
        builder.set_pygame_img(pygame.image.load('player_mini_bullet.png'))
        builder.set_init_pos()
        builder.set_init_mov_accel((1, 0))
        builder.set_mov_spd(0.25)
        builder.set_init_state()
        builder.set_atk_spd(0.1)
        builder.set_sound(pygame.mixer.Sound('fire2.wav'))
        return builder.build()


PLAYER = PlayerCreator().build_player(PlayerBuilder())
ENEMY = EnemyCreator().build_basic_enemy(EnemyBuilder())


allied_sprite_group = pygame.sprite.Group()
allied_sprite_group.add(PLAYER)

enemy_sprite_group = pygame.sprite.Group()
enemy_sprite_group.add(
    EnemyCreator().build_basic_enemy(EnemyBuilder()))
#
# world_sprite_group = pygame.sprite.Group()
