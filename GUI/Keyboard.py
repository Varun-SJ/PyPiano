from GUI.Keys import *

BLACK_KEYS = [1, 3, 6, 8, 10]
WHITE_WIDTH = 65
BLACK_WIDTH = 34
SPACING = 2
PADDING = 4
BLACK_WHITE_LENGTH_RATIO = 0.65


class Keyboard:
    def __init__(self, top, bottom):
        temp = WhiteKey(PADDING, top, WHITE_WIDTH, bottom - top, 0)
        self.whiteKeys = [temp]
        self.blackKeys = []
        self.keys = dict()
        self.keys[0] = temp

        for i in range(1, 32):
            if i % 12 in BLACK_KEYS:
                key = BlackKey(self.whiteKeys[-1].x + WHITE_WIDTH + (SPACING - BLACK_WIDTH) / 2, top, BLACK_WIDTH,
                               (bottom - top) * BLACK_WHITE_LENGTH_RATIO, i)
                self.blackKeys.append(key)
                self.keys[i] = key
            else:
                key = WhiteKey(self.whiteKeys[-1].x + WHITE_WIDTH + SPACING, top, WHITE_WIDTH, bottom - top, i)
                self.whiteKeys.append(key)
                self.keys[i] = key

        self.pressedWhiteKeys = dict()

    def draw_keys(self, screen):
        for key in self.whiteKeys:
            key.draw(screen)

        for key in self.blackKeys:
            key.draw(screen)

    def press_key(self, key):
        if key in self.keys:
            key_obj = self.keys.get(key)
            key_obj.set_pressed(True)
            if type(key_obj) is WhiteKey:
                self.pressedWhiteKeys[key] = key_obj

    def release_key(self, key):
        if key in self.keys:
            key_obj = self.keys.get(key)
            key_obj.set_pressed(False)
            if key in self.pressedWhiteKeys:
                del self.pressedWhiteKeys[key]

    def draw_keys_optimized(self, screen):
        overlaid = set()
        for key in self.pressedWhiteKeys.values():
            key.draw(screen)
            i = key.id
            if i % 12 in [4, 11] or i == 31:
                # no right
                overlaid.add(i - 1)
            elif i % 12 in [5, 0]:
                # no left
                overlaid.add(i + 1)
            else:
                # both
                overlaid.add(i - 1)
                overlaid.add(i + 1)

        for key_id in overlaid:
            key = self.keys[key_id]
            key.draw(screen)
