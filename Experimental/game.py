# Import pygame and libraries
from pygame.locals import *
from random import randrange
import os
import pygame

# Import pygameMenu
import pygameMenu
from pygameMenu.locals import *

from GUI.MenuItems import *
from pygame.locals import *

import pygame

import pygameMenu
from pygameMenu.locals import *


def input(events):
    for event in events:
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                menu.enable()


display_width = 1280
display_height = 1024

pygame.init()
pygame.display.set_caption("GUI")
Display = pygame.display.set_mode((display_width, display_height))
Display.fill((155, 155, 155))
clock = pygame.time.Clock()

# keyboard = Keyboard(200)
# keyboard.draw_keys(Display)

menu = MainMenu(Display)

while True:
    events = pygame.event.get()
    Display.fill((155, 155, 155))
    input(events)
    menu.menu_loop(events)
    pygame.display.update()
