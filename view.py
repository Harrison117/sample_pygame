import pygame
from event import *
from helper.helper import WeakBoundMethod


class PygameWindow(Listener):
    def __init__(self, event_mgr, window=None, win_size=(600, 250)):
        super(PygameWindow, self).__init__(
            event_mgr=event_mgr)

        self._event_mgr.add(TickEvent, WeakBoundMethod(self.on_tick_event))

        self._window = window
        self.init_pygame_window(win_size)

    def init_pygame_window(self, win_size):
        pygame.init()

        # create the screen
        self._window = pygame.display.set_mode(win_size)

        # title and icon
        pygame.display.set_caption("Space Invaders")

    def on_tick_event(self, e):
        event = UpdateViewEvent(self._window)
        self._event_mgr.post(event)
        pygame.display.flip()

    def get_window_size(self):
        return self._window.get_size()


class LevelScene(Listener):
    def __init__(self, event_mgr, background=None):
        super(LevelScene, self).__init__(
            event_mgr=event_mgr)
        self._event_mgr.add(TickEvent, WeakBoundMethod(self.on_tick_event))
        self._event_mgr.add(UpdateViewEvent, WeakBoundMethod(self.update_view))
        self._event_mgr.add(TransformViewEvent, WeakBoundMethod(self.on_transform_scene_event))

        self.background = background

    def on_tick_event(self, e):
        pass

    def on_transform_scene_event(self, e):
        self.background.fill(e.get_data()['color'])

    def on_change_scene_event(self, e):
        pass

    def update_view(self, e):
        try:
            e.get_data()['window'].blit(self.background, (0, 0))

        except TypeError:
            print('Error: data not found...')

        except KeyError:
            print('Error: window not found...')


class EntitySprite(Listener, pygame.sprite.Sprite):
    def __init__(self, event_mgr, image=pygame.Surface((0, 0))):
        Listener.__init__(self, event_mgr=event_mgr)
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()

    def update_view(self, e):
        try:
            e.get_data()['window']
