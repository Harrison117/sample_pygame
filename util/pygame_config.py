import pygame
from pygame.locals import *
import os

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 250

FPS = 60

ASSET_PATH = os.path.join(
    os.path.dirname(__file__),
    '..\\assets')


def get_asset_path(filename, base_path=ASSET_PATH):
    path = os.path.join(base_path, filename)
    # print(path)
    return path


# initialize pygame
pygame.init()

# create the screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(get_asset_path('ufo.png'))
pygame.display.set_icon(icon)

CLOCK = pygame.time.Clock()