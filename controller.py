from event import *
from helper.helper import WeakBoundMethod

import pygame
from pygame.locals import *


class KeyboardController(object):
    """KeyboardController takes Pygame events generated by the
    keyboard and uses them to control the model, by sending Requests
    or to control the Pygame display directly, as with the QuitEvent
    """
    def __init__(self, event_mgr):
        self.event_mgr = event_mgr
        self.event_mgr.register_listener(self)

    def notify(self, event):
        if isinstance(event, TickEvent):
            #Handle Input Events
            for event in pygame.event.get():
                e = None
                specific_classes = list()
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    e = QuitEvent
                    specific_classes.append(CPUSpinnerController)
                elif event.type == KEYDOWN and event.key == K_UP:
                    pass
                elif event.type == KEYDOWN and event.key == K_DOWN:
                    pass
                elif event.type == KEYDOWN and event.key == K_LEFT:
                    pass
                elif event.type == KEYDOWN and event.key == K_RIGHT:
                    pass

                if e:
                    self.event_mgr.post(e, *specific_classes)


class CPUSpinnerController(Listener):
    def __init__(self, event_mgr):
        super(CPUSpinnerController, self).__init__(event_mgr=event_mgr)
        self.event_mgr = event_mgr
        self.running = True

    def run(self):
        while self.running:
            event = TickEvent()
            self.event_mgr.post(event)

    def on_exit(self):
        self.running = False

    def notify(self, event):
        event.execute()
