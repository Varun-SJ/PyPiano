from os import listdir
from os.path import isfile, join
import pygame
import pygameMenu
from SongController import *
from pygameMenu.locals import *
from PythonSound import PythonSound
from SPIConnection import SPIConnection
import KeyboardConnection
import sys

SOUND = False
PSOUND = PythonSound()
SSUND = SPIConnection()
SPEED_mod = 1
AUDIO = AudioModes.KEYBOARD_ONLY


def set_device(bol, m):
    global SOUND
    SOUND = bol


def set_speed_mod(int, m):
    global SPEED_mod
    SPEED_mod = int


def set_audio(int, m):
    global AUDIO
    if int == 1:
        AUDIO = AudioModes.SONG_ONLY
    elif int == 2:
        AUDIO = AudioModes.KEYBOARD_ONLY


def play_game(screen, address, clock, keyboard, game):
    global SPEED_mod
    global SOUND
    global AUDIO

    load = Loading(screen, game)
    load.menu.draw()
    pygame.display.update()
    sound = PSOUND if SOUND else SSUND
    song = Song(screen, clock, address, keyboard, sound, SPEED_mod, AUDIO)
    score = song.start()

    done = False
    while not done:

        score_menu = ScoreMenu(screen, score, game)
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.KEYDOWN:
                done = True
                score_menu.menu.disable()
                break
        score_menu.menu.mainloop(events)
        pygame.display.update()
        screen.fill((127, 127, 127))


def back_ground_fill(display):
    display.fill((127, 127, 127))


def quit_game(keyboard):
    pygame.quit()
    keyboard.close()
    sys.exit()


class MainMenu:
    def __init__(self, display, game):
        self.windowW = 1024
        self.windowH = 1280
        self.display = display
        self.game = game
        self.event = None
        self.menu = pygameMenu.Menu(self.display,
                                    dopause=False,
                                    font=pygameMenu.fonts.FONT_NEVIS,
                                    menu_alpha=85,
                                    menu_color=(0, 0, 0),
                                    menu_color_title=(0, 0, 0),
                                    menu_height=int(self.windowH / 4),
                                    menu_width=int(self.windowW / 3),
                                    title='PyPiano',
                                    title_offsety=5,
                                    window_height=self.windowW,
                                    window_width=self.windowH,
                                    )
        self.set = Setting()
        self.settingsMenu = SettingsMenu(self.display, self.set)
        Songpages = SongPages(self.display, self.game, self.set)
        # Songpages.create_pagelist()
        Songpages.fill_pages()
        self.menu.add_option("Play", Songpages.menu.menu)
        self.menu.add_option("Settings", self.settingsMenu.setting_menu)
        self.menu.add_option("Exit", quit_game, self.game.keyboard)

    def menu_loop(self, events):
        self.menu.mainloop(events)


class SongPages:
    def __init__(self, display, game, settings):
        self.game = game
        self.display = display
        self.song_list = self.read_song_files()
        self.page_list = []
        self.NumberOfSongs = 0
        self.PageNumber = 0
        self.event = None
        self.settings = settings

    def read_song_files(self):
        path = "./Songs/"
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        combo = [(join(path, f), (f.rsplit(".", 1)[0])) for f in onlyfiles]
        return combo

    def fill_pages(self):
        global SPEED_mod
        global SOUND
        global AUDIO
        # print(SPEED_mod)
        self.PageNumber = self.PageNumber = + 1
        self.menu = SongMenu(self.display, self.game, self.PageNumber)
        int = 0
        for i in self.song_list:
            self.menu.menu.add_option(i[1], play_game,
                                      self.game.get_screen(),
                                      i[0],
                                      self.game.get_clock(),
                                      self.game.get_keyboard(),
                                      self.game
                                      )
            self.NumberOfSongs = self.NumberOfSongs + 1
            if self.NumberOfSongs == 10:
                int += 1
                self.NumberOfSongs = 0
                self.PageNumber = self.PageNumber = + 1

        self.menu.menu.add_option("Back", PYGAME_MENU_BACK)

    # def next_page(self, int):
    #     global page_list
    #     x = page_list[int].menu
    #     return x

    def return_first_page(self):
        return self.page_list[0].menu


class SongMenu:
    def __init__(self, display, game, pagenumber):
        self.windowW = 1024
        self.windowH = 1280
        self.display = display
        self.game = game
        self.page_number = pagenumber
        self.menu = self.create_menu(self.display)

    def create_menu(self, display):
        menu = pygameMenu.Menu(display,
                               dopause=False,
                               font=pygameMenu.fonts.FONT_NEVIS,
                               menu_alpha=85,
                               menu_color=(0, 0, 0),
                               menu_color_title=(0, 0, 0),
                               menu_height=int(self.windowH / 1.5),
                               menu_width=int(self.windowW / 2),
                               title='Song Select',
                               font_size_title=50,
                               title_offsety=5,
                               window_height=self.windowW,
                               window_width=self.windowH,
                               onclose=PYGAME_MENU_DISABLE_CLOSE,
                               )
        return menu


class Setting:
    def __init__(self):
        self.SOUND = PythonSound()
        self.SPEED_mod = 1
        self.AUDIO = AudioModes.KEYBOARD_ONLY


class SettingsMenu:
    def __init__(self, display, set):
        self.windowW = 1024
        self.windowH = 1280
        self.display = display
        self.menu = set
        self.setting_menu = pygameMenu.TextMenu(display,
                                                dopause=False,
                                                font=pygameMenu.fonts.FONT_NEVIS,
                                                menu_alpha=85,
                                                menu_color=(0, 0, 0),
                                                menu_color_title=(0, 0, 0),
                                                menu_height=int(self.windowH / 3.5),
                                                menu_width=int(self.windowW / 1.5),
                                                title='Settings',
                                                title_offsety=5,
                                                window_height=self.windowW,
                                                window_width=self.windowH,
                                                bgfun=back_ground_fill(display)
                                                )
        self.setting_menu.add_selector('Sound From: ',
                                       [('Soc', False, self.menu),
                                        ('Pi', True, self.menu)],
                                       onchange=set_device,  # Action when changing element with left/right
                                       onreturn=None,  # Action when pressing return on a element
                                       # default=1,  # Optional parameter that sets default item of selector
                                       )
        self.setting_menu.add_selector('Sound Output: ',
                                       [('Keyboard', 2, self.menu),
                                        ('File', 1, self.menu)],
                                       onchange=set_audio,  # Action when changing element with left/right
                                       onreturn=None,  # Action when pressing return on a element
                                       # default=2,  # Optional parameter that sets default item of selector
                                       )

        self.setting_menu.add_selector('Speed Modifier: ',
                                       [('1.0', 1.0, self.menu),
                                        ('1.1', 1.1, self.menu), ('1.2', 1.2, self.menu), ('1.3', 1.3, self.menu),
                                        ('1.4', 1.4, self.menu), ('1.5', 1.5, self.menu),
                                        ('1.6', 1.6, self.menu), ('1.7', 1.7, self.menu), ('1.8', 1.8, self.menu),
                                        ('1.9', 1.9, self.menu), ('2.0', 2.0, self.menu),
                                        ('2.1', 2.1, self.menu), ('2.2', 2.2, self.menu), ('2.3', 2.3, self.menu),
                                        ('2.4', 2.4, self.menu), ('2.5', 2.5, self.menu),
                                        ('2.6', 2.6, self.menu), ('2.7', 2.7, self.menu), ('2.8', 2.8, self.menu),
                                        ('2.9', 2.9, self.menu), ('3.0', 3.0, self.menu), ('0.1', 0.1, self.menu),
                                        ('0.2', 0.2, self.menu),
                                        ('0.3', 0.3, self.menu),
                                        ('0.4', 0.4, self.menu), ('0.5', 0.5, self.menu),
                                        ('0.6', 0.6, self.menu), ('0.7', 0.7, self.menu), ('0.8', 0.8, self.menu),
                                        ('0.9', 0.9, self.menu), ],
                                       onchange=set_speed_mod,  # Action when changing element with left/right
                                       onreturn=None,  # Action when pressing return on a element
                                       # default=9  # Optional parameter that sets default item of selector
                                       # write_on_console=True  # Optional parameters to  function
                                       )
        self.setting_menu.add_option("Back", PYGAME_MENU_BACK)


class ScoreMenu:
    def __init__(self, display, score, game):
        self.windowW = 1024
        self.windowH = 1280
        self.display = display
        self.score = score
        self.game = game
        self.menu = pygameMenu.TextMenu(display,
                                        dopause=False,
                                        font=pygameMenu.fonts.FONT_NEVIS,
                                        menu_alpha=85,
                                        menu_color=(0, 0, 0),
                                        menu_color_title=(0, 0, 0),
                                        menu_height=int(self.windowH / 4),
                                        menu_width=int(self.windowW / 3),
                                        title='Game Over',
                                        title_offsety=5,
                                        window_height=self.windowW,
                                        window_width=self.windowH,
                                        bgfun=back_ground_fill(display),
                                        text_fontsize=30
                                        )
        self.menu.add_line("Your final score: " + self.score.__str__())
        menu = MainMenu(self.display, self.game)
        self.menu.add_option("Back", menu.menu)


class Loading:
    def __init__(self, display, game):
        self.windowW = 1024
        self.windowH = 1280
        self.display = display
        self.game = game
        self.menu = pygameMenu.TextMenu(display,
                                        dopause=False,
                                        font=pygameMenu.fonts.FONT_NEVIS,
                                        menu_alpha=100,
                                        menu_color=(0, 0, 0),
                                        menu_color_title=(0, 0, 0),
                                        menu_height=int(self.windowH / 20),
                                        menu_width=int(self.windowW / 3.3),
                                        title='LOADING...',
                                        title_offsety=0,
                                        window_height=self.windowW,
                                        window_width=self.windowH,
                                        bgfun=back_ground_fill(display),
                                        )
