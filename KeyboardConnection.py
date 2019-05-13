from threading import Thread, Lock
import pygame.midi
import time
from NavigationKey import NavigationKey


class MidiKeyboard(Thread):
    heldKeys = dict()
    pressedKeys = dict()
    releasedKeys = dict()
    device = None
    done = False
    navigate = None

    def __init__(self, navigation_callback):
        super().__init__()
        self.navigate = navigation_callback
        self.start()
        self.lock = Lock()

    def run(self):
        self.device = self.find_device()
        print("Found device" + repr(self.device))
        self.read()

    @staticmethod
    def find_device():
        devices = []
        while True:
            pygame.midi.init()
            print("Searching for midi input")
            for i in range(0, pygame.midi.get_count()):
                if pygame.midi.get_device_info(i)[2] == 1:
                    devices.append(pygame.midi.Input(i))
            for i in range(0, 40):
                # print("searching")
                time.sleep(0.1)
                for d in devices:
                    if d.poll():
                        # print(d)
                        return d
            pygame.midi.quit()

    def read(self):
        while not self.done:
            if self.device.poll():
                midi_event = self.device.read(1)[0]
                if midi_event[0][0] == 144:
                    self.lock.acquire()
                    if midi_event[0][2] > 0:
                        self.heldKeys[midi_event[0][1]] = midi_event
                        self.pressedKeys[midi_event[0][1]] = midi_event
                    else:
                        # if self.heldKeys.get(midi_event[0][1]) is not None:
                        self.heldKeys.pop(midi_event[0][1], None)
                        self.releasedKeys[midi_event[0][1]] = midi_event
                    self.lock.release()
                elif midi_event[0][0] == 176 and midi_event[0][2] == 127:
                    if midi_event[0][1] == 19:
                        self.navigate(NavigationKey.UP)
                    elif midi_event[0][1] == 20:
                        self.navigate(NavigationKey.DOWN)
                    elif midi_event[0][1] == 21:
                        self.navigate(NavigationKey.RIGHT)
                    elif midi_event[0][1] == 22:
                        self.navigate(NavigationKey.LEFT)
                    elif midi_event[0][1] == 23:
                        self.navigate(NavigationKey.CENTER)
                    else:
                        print("Key not supported, " + repr(midi_event))
        self.device.close()
        pygame.midi.quit()

    def get_pressed_keys(self):
        self.lock.acquire()
        temp = self.pressedKeys.values()
        self.pressedKeys = dict()
        self.lock.release()
        return temp

    def get_held_keys(self):
        self.lock.acquire()
        temp = [v for v in self.heldKeys.values()]
        self.lock.release()
        return temp

    def get_released_keys(self):
        self.lock.acquire()
        temp = self.releasedKeys.values()
        self.releasedKeys = dict()
        self.lock.release()
        return temp

    def close(self):
        self.done = True

# 176
# 19 up
# 20 down
# 21 right
# 22 left
# 23 middle
# 144
# 48
# .r
# .
# .
# 79
