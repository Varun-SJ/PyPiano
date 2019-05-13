from KeyboardConnection import MidiKeyboard
import time
import pygame.midi


class Test:
    keyboard = None

    def __init__(self):
        self.keyboard = MidiKeyboard(self.navigation_callback)

    def navigation_callback(self, key):
        print(key)

    def constant_read(self):
        try:
            while True:
                keys = self.keyboard.heldKeys
                if len(keys) > 0:
                    print(self.keyboard.heldKeys)
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.keyboard.close()
        except Exception as e:
            print(e)


def testing():
    pygame.midi.init()
    print(pygame.midi.get_count())
    for i in range(0, pygame.midi.get_count()):
        print(pygame.midi.get_device_info(i))
    d = pygame.midi.Input(1)
    while True:
        while d.poll():
            print(d.read(1))


test = Test()
test.constant_read()
# testing()
