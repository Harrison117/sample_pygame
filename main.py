"""
Icons made by Good Ware from https://www.flaticon.com/authors/good-ware
"""
from util.director import *
from util.pygame_config import SCREEN, CLOCK, FPS
from util.enums import *

# from util.entities import StatusBar
#
# test_bar = StatusBar(
#     color=pygame.Color(0, 255, 0),
#     size=(32, 5))


# game loop
# NOTE: every events present while focused on pygame window are recorded
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_0:
                pass
                # test_bar.update_status_bar(-0.05)

            if event.key == pygame.K_LEFTBRACKET:
                FPS = 30

            if event.key == pygame.K_LEFT:
                PLAYER.update_x_accel(-1)
                PLAYER.set_movement_state(LEFT)
                # print("left pressed!")

            if event.key == pygame.K_RIGHT:
                PLAYER.update_x_accel(1)
                PLAYER.set_movement_state(RIGHT)
                # print("right pressed!")

            if event.key == pygame.K_UP:
                PLAYER.update_y_accel(-1)
                PLAYER.set_movement_state(UP)
                # print("up pressed!")

            if event.key == pygame.K_DOWN:
                PLAYER.update_y_accel(1)
                PLAYER.set_movement_state(DOWN)
                # print("down pressed!")

            if event.key == pygame.K_SPACE:
                PLAYER.set_weapon_firing_state()
                # PLAYER.print_bullet_stack()

        if event.type == pygame.KEYUP:
            # print(f'Before: {player_mov_dir_state}')

            if event.key == pygame.K_LEFTBRACKET:
                FPS = 60

            if event.key == pygame.K_1:
                PLAYER.switch_weapon(WeaponType.BASIC)

            if event.key == pygame.K_2:
                PLAYER.switch_weapon(WeaponType.MINI)

            if event.key == pygame.K_3:
                PLAYER.switch_weapon(WeaponType.MISSILE)

            if event.key == pygame.K_4:
                PLAYER.switch_weapon(WeaponType.LASER)

            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT) and \
                    not (PLAYER.is_moving(LEFT) and PLAYER.is_moving(RIGHT)):
                PLAYER.update_x_accel(0)
                # print("left/right released!")

            if event.key == pygame.K_LEFT:
                PLAYER.set_movement_state(LEFT)
                # print("left released!")

            if event.key == pygame.K_RIGHT:
                PLAYER.set_movement_state(RIGHT)
                # print("right released!")

            if (event.key == pygame.K_UP or event.key == pygame.K_DOWN) and \
                    not (PLAYER.is_moving(UP) and PLAYER.is_moving(DOWN)):
                PLAYER.update_y_accel(0)
                # print("up/down released!")

            if event.key == pygame.K_UP:
                PLAYER.set_movement_state(UP)
                # print("up released!")

            if event.key == pygame.K_DOWN:
                PLAYER.set_movement_state(DOWN)
                # print("down released!")

            if event.key == pygame.K_SPACE:
                # PLAYER.set_weapon_firing_state()
                pass
            # print(f'After: {player_mov_dir_state}\n')

        if event.type == pygame.QUIT:
            running = False

    SCREEN.fill((100, 100, 100))

    # update screen display
    pygame.display.flip()
    CLOCK.tick(FPS)
