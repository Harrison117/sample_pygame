"""
Icons made by Good Ware from https://www.flaticon.com/authors/good-ware
"""
from util.director import *
from util.pygame_config import SCREEN, CLOCK


LEFT=0; RIGHT=1
UP=2; DOWN=3
player_mov_dir_state = [False, False, False, False]
# game loop
# NOTE: every events present while focused on pygame window are recorded
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                PLAYER.update_x_accel(-1)
                PLAYER.set_movement_state(LEFT)
                # player_mov_dir_state[LEFT] = True
                # print("left pressed!")

            if event.key == pygame.K_RIGHT:
                PLAYER.update_x_accel(1)
                PLAYER.set_movement_state(RIGHT)
                # player_mov_dir_state[RIGHT] = True
                # print("right pressed!")

            if event.key == pygame.K_UP:
                PLAYER.update_y_accel(-1)
                PLAYER.set_movement_state(UP)
                # player_mov_dir_state[UP] = True
                # print("up pressed!")

            if event.key == pygame.K_DOWN:
                PLAYER.update_y_accel(1)
                PLAYER.set_movement_state(DOWN)
                # player_mov_dir_state[DOWN] = True
                # print("down pressed!")

            if event.key == pygame.K_SPACE:
                PLAYER.set_fire_state()
                # PLAYER.print_bullet_stack()

        if event.type == pygame.KEYUP:
            # print(f'Before: {player_mov_dir_state}')

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
                PLAYER.set_fire_state()

            # print(f'After: {player_mov_dir_state}\n')

        if event.type == pygame.QUIT:
            running = False

    # fill(<RGB color tuple>)
    SCREEN.fill((100, 100, 100))

    allied_sprite_group.update()

    # NOTE: position of the graphic depends on the rect coordinates
    allied_sprite_group.draw(SCREEN)

    enemy_sprite_group.update()

    # NOTE: position of the graphic depends on the rect coordinates
    enemy_sprite_group.draw(SCREEN)

    # update screen display
    # pygame.display.update()
    pygame.display.flip()
    # CLOCK.tick(1000)