from util.pygame_config import *
from util.enums import *


def input_tick(player):
    for event in pygame.event.get():
        if event.type == QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                return False

            if event.key == K_0:
                pass

            if event.key == K_LEFTBRACKET:
                FPS = 30

            if event.key == K_LEFT:
                player.update_x_accel(-1)
                player.set_movement_state(LEFT)
                # print("left pressed!")

            if event.key == K_RIGHT:
                player.update_x_accel(1)
                player.set_movement_state(RIGHT)
                # print("right pressed!")

            if event.key == K_UP:
                player.update_y_accel(-1)
                player.set_movement_state(UP)
                # print("up pressed!")

            if event.key == K_DOWN:
                player.update_y_accel(1)
                player.set_movement_state(DOWN)
                # print("down pressed!")

            if event.key == K_SPACE:
                player.set_weapon_firing_state()
                # PLAYER.print_bullet_stack()

        if event.type == KEYUP:
            # print(f'Before: {player_mov_dir_state}')

            if event.key == K_LEFTBRACKET:
                FPS = 60

            if event.key == K_1:
                player.switch_weapon(WeaponType.BASIC)

            if event.key == K_2:
                player.switch_weapon(WeaponType.MINI)

            if event.key == K_3:
                player.switch_weapon(WeaponType.MISSILE)

            if event.key == K_4:
                player.switch_weapon(WeaponType.LASER)

            if (event.key == K_LEFT or event.key == K_RIGHT) and \
                    not (player.is_moving(LEFT) and player.is_moving(RIGHT)):
                player.update_x_accel(0)
                # print("left/right released!")

            if event.key == K_LEFT:
                player.set_movement_state(LEFT)
                # print("left released!")

            if event.key == K_RIGHT:
                player.set_movement_state(RIGHT)
                # print("right released!")

            if (event.key == K_UP or event.key == K_DOWN) and \
                    not (player.is_moving(UP) and player.is_moving(DOWN)):
                player.update_y_accel(0)
                # print("up/down released!")

            if event.key == K_UP:
                player.set_movement_state(UP)
                # print("up released!")

            if event.key == K_DOWN:
                player.set_movement_state(DOWN)
                # print("down released!")

            if event.key == K_SPACE:
                # PLAYER.set_weapon_firing_state()
                pass
            # print(f'After: {player_mov_dir_state}\n')

    return True
