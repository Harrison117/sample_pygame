from engine.model_entity import *
from engine.view import *
from engine.controller import *


def main():
    """..."""
    event_mgr = EventManager()

    keyboard = KeyboardController(event_mgr)
    spinner = CPUSpinnerController(event_mgr)
    pygame_view = PygameWindow(event_mgr)

    scene = pygame.Surface(pygame_view.get_window_size())
    scene.fill((100, 100, 100))

    pygame_level_view = LevelScene(
        event_mgr,
        background=scene)

    hp = 100
    sp = 0
    dmg = hp
    weapon = None
    player = Player(
        event_mgr, hp, sp, dmg, weapon,
        pos=OrderedPair(0, 0), off=OrderedPair(0, 0), angle=OrderedPair(0, 0), mov_spd=3)

    player_view = EntitySprite(
        event_mgr,
        image=pygame.image.load('./assets/sprites/player.png'))

    sprite_group = EntityGroup(event_mgr, player_view)

    # game = Game(event_mgr)

    spinner.run()


if __name__ == "__main__":
    main()
