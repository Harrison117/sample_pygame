import pygame
from event import *
from helper.helper import WeakBoundMethod


class PygameView(Listener):

    def __init__(self, event_mgr, window=None, background=None, win_size=(600, 250)):
        super(PygameView, self).__init__(
            event_mgr=event_mgr)

        self._event_mgr.add(TickEvent, WeakBoundMethod(self.on_tick_event))

        self.window = window
        self.background = background
        self.init_pygame_window(win_size)

    def init_pygame_window(self, win_size):
        pygame.init()

        # create the screen
        self.window = pygame.display.set_mode(win_size)

        # title and icon
        pygame.display.set_caption("Space Invaders")

        self.background = pygame.Surface(self.window.get_size())
        self.background.fill((0, 0, 0))

        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

    def on_tick_event(self, event):
        self.update_view()

    def update_view(self):
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()
