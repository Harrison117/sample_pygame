import pygame

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 250

# initialize pygame
pygame.init()

# create the screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

CLOCK = pygame.time.Clock()