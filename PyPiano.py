import os
import pygame
from KeyboardConnection import MidiKeyboard
from SongController import Song
from pygame.locals import *
from GUI.MenuItems import *
from NavigationKey import NavigationKey

SCREEN_SIZE = 1280, 1024


class PyPiano:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PyPiano")
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.NOFRAME)
        self.keyboard = MidiKeyboard(self.nav_callback)
        self.done = False
        self.clock = pygame.time.Clock()
        self.start()

    def get_screen(self):
        return self.screen

    def get_clock(self):
        return self.clock

    def get_keyboard(self):
        return self.keyboard

    def nav_callback(self, key):
        if key == NavigationKey.UP:
            pygame.event.post(pygame.event.Event(KEYDOWN, {'unicode': '', 'key': 273, 'mod': 0, 'scancode': 72}))
        elif key == NavigationKey.DOWN:
            pygame.event.post(pygame.event.Event(KEYDOWN, {'unicode': '', 'key': 274, 'mod': 0, 'scancode': 80}))
        elif key == NavigationKey.RIGHT:
            pygame.event.post(pygame.event.Event(KEYDOWN, {'unicode': '', 'key': 275, 'mod': 0, 'scancode': 77}))
        elif key == NavigationKey.LEFT:
            pygame.event.post(pygame.event.Event(KEYDOWN, {'unicode': '', 'key': 276, 'mod': 0, 'scancode': 75}))
        elif key == NavigationKey.CENTER:
            pygame.event.post(pygame.event.Event(KEYDOWN, {'unicode': '\r', 'key': 13, 'mod': 0, 'scancode': 28}))

    def start(self):
        menu = MainMenu(self.screen, self)
        while not self.done:

            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    self.done = True
                    break

            menu.menu_loop(events)
            pygame.display.update()
            self.screen.fill((127, 127, 127))


if __name__ == "__main__":
    PyPiano().start()
