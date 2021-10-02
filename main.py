"""
Icons made by Good Ware from https://www.flaticon.com/authors/good-ware
"""
from util.director import *
from controller import *


def main():
    # game loop
    # NOTE: every events present while focused on pygame window are recorded
    running = True
    while running:
        running = input_tick(PLAYER)

        if not running:
            break

        # fill(<RGB color tuple>)
        SCREEN.fill((100, 100, 100))
        """
        NOTE: drawing according to the position of the graphic depends on the 
        rect coordinates
        """
        enemy_sprite_group.update()
        enemy_sprite_group.draw(SCREEN)
        for enemy in enemy_sprite_group:
            pygame.draw.rect(SCREEN, enemy.get_hp_bar().get_color(), enemy.get_hp_bar())

        allied_sprite_group.update(enemy_sprite_group)
        allied_sprite_group.draw(SCREEN)
        for ally in allied_sprite_group:
            ally.get_weapon().get_bullet_stack().draw(SCREEN)


        # update screen display
        pygame.display.flip()
        CLOCK.tick(FPS)


def observer_test():



if __name__ == '__main__':
    main()
