import random
from util.pygame_config import *
from util.builder import *
from util.enums import WeaponType


class StatusBarDirector:
    SMALL_TYPE_HEIGHT = 3

    @staticmethod
    def build_hp_bar(entity):
        builder = StatusBarBuilder()
        builder.set_owner(entity)
        builder.set_color(pygame.Color(0, 255, 0))
        builder.set_pos(
            (entity.get_x_pos(), entity.get_y_pos()),
            y_off=-StatusBarDirector.SMALL_TYPE_HEIGHT)
        builder.set_size(
            (entity.get_width(), StatusBarDirector.SMALL_TYPE_HEIGHT))
        return builder.build()


class EntityDirector(object):
    @abstractmethod
    def build_entity_asset(self, *args, **kwargs):
        pass

    @abstractmethod
    def build_entity_properties(self, *args, **kwargs):
        pass


class PlayerDirector:
    @staticmethod
    def build_player():
        builder = PlayerBuilder()
        builder.set_name("player")
        builder.set_pygame_img(
            pygame.image.load(get_asset_path('sprites/player.png')))
        builder.set_init_pos_offset((6, 2))
        builder.set_init_pos()
        builder.set_init_mov_accel((0, 0))
        builder.set_mov_spd(3)
        builder.set_hit_box()
        builder.setup_weapon(WeaponCreator(), WeaponType.BASIC)
        return builder.build()


class EnemyCreator:
    @staticmethod
    def build_basic_enemy():
        img = pygame.image.load(
            get_asset_path('sprites/enemy.png'))
        img_x_mid = img.get_width() // 2
        pos_offset = (6, 2)
        builder = EnemyBuilder()
        builder.set_pygame_img(img)
        builder.set_init_pos_offset(pos_offset)
        builder.set_init_pos(
            x_pos=(SCREEN_WIDTH // pos_offset[0] - img_x_mid) * 5,
            y_pos=random.randint(0, SCREEN_HEIGHT - img.get_height()))
        builder.set_init_mov_accel(
            (0,
             random.choice([-1, 1])))
        builder.set_mov_spd(2)
        builder.set_hit_box()
        builder.setup_hp_bar(StatusBarDirector())
        return builder.build()


class WeaponCreator:
    @staticmethod
    def build_weapon(entity):
        builder = WeaponBuilder()
        builder.set_bullet_factory(BulletCreator())
        builder.set_owner(entity)
        return builder.build()


class BulletCreator:
    @staticmethod
    def build_player_basic_bullet(entity):
        builder = BulletBuilder()
        builder.set_owner(entity)
        builder.set_weapon_type(WeaponType.BASIC)
        builder.set_pygame_img(pygame.image.load(
            get_asset_path('sprites/player_basic_bullet.png')))
        builder.set_hit_box()
        builder.set_init_pos()
        builder.set_init_mov_accel((1, 0))
        builder.set_mov_spd(10.0)
        builder.set_init_state()
        builder.set_dmg(5.0)
        builder.set_atk_spd(0.2)
        builder.set_sound(pygame.mixer.Sound(
            get_asset_path('sounds/fire1.wav')))
        return builder.build()

    @staticmethod
    def build_player_mini_bullet(entity):
        builder = BulletBuilder()
        builder.set_owner(entity)
        builder.set_weapon_type(WeaponType.MINI)
        builder.set_pygame_img(
            pygame.image.load(get_asset_path('sprites/player_mini_bullet.png')))
        builder.set_init_pos()
        builder.set_init_mov_accel((1, 0))
        builder.set_mov_spd(20.0)
        builder.set_init_state()
        builder.set_dmg(1.0)
        builder.set_atk_spd(0.08)
        builder.set_hit_box()
        builder.set_sound(
            pygame.mixer.Sound(get_asset_path('sounds/fire2.wav')))
        return builder.build()

    @staticmethod
    def build_player_missile_bullet(entity):
        builder = BulletBuilder()
        builder.set_owner(entity)
        builder.set_weapon_type(WeaponType.MISSILE)
        builder.set_pygame_img(
            pygame.image.load(get_asset_path('sprites/player_missile_bullet.png')))
        builder.set_init_pos()
        builder.set_init_mov_accel((1, 0))
        builder.set_mov_spd(5.0)
        builder.set_init_state()
        builder.set_dmg(20)
        builder.set_atk_spd(0.6)
        builder.set_hit_box()
        builder.set_sound(
            pygame.mixer.Sound(get_asset_path('sounds/missile6.wav')))
        return builder.build()

    @staticmethod
    def build_player_laser_bullet(entity):
        builder = BulletBuilder()
        builder.set_owner(entity)
        builder.set_weapon_type(WeaponType.LASER)
        builder.set_pygame_img(
            pygame.image.load(get_asset_path('sprites/player_laser_bullet.png')))
        builder.set_init_pos()
        builder.set_init_mov_accel((1, 0))
        builder.set_mov_spd(25.0)
        builder.set_init_state()
        builder.set_dmg(0.5)
        builder.set_atk_spd(0.015)
        builder.set_hit_box()
        builder.set_sound(
            pygame.mixer.Sound(get_asset_path('sounds/laser8.wav')))
        return builder.build()

    def build_bullet_type(self, bullet_type, entity):
        if bullet_type == WeaponType.BASIC:
            return self.build_player_basic_bullet(entity)
        if bullet_type == WeaponType.MINI:
            return self.build_player_mini_bullet(entity)
        if bullet_type == WeaponType.MISSILE:
            return self.build_player_missile_bullet(entity)
        if bullet_type == WeaponType.LASER:
            return self.build_player_laser_bullet(entity)


PLAYER = PlayerDirector().build_player()
ENEMY = EnemyCreator().build_basic_enemy()

allied_sprite_group = pygame.sprite.Group()
allied_sprite_group.add(PLAYER)

enemy_sprite_group = pygame.sprite.Group()
enemy_sprite_group.add(
    EnemyCreator().build_basic_enemy())

# world_sprite_group = pygame.sprite.Group()
