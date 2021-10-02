import pygame
from pygame.locals import *


class PygameView(object):

    def __init__(self, event_mgr, win_size=(600, 250)):
        self._event_mgr = event_mgr

        pygame.init()

        # create the screen
        self.window = pygame.display.set_mode(win_size)

        # title and icon
        pygame.display.set_caption("Space Invaders")

        self.background = pygame.Surface(self.window.get_size())
        self.background.fill((0, 0, 0))

        self.window.blit(self.background, (0,0))
        pygame.display.flip()

    def notify(self, event):
        pass
