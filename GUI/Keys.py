import pygame

WHITE_COLOR = (255, 255, 255)
WHITE_PRESSED_COLOR = (127, 127, 255)

BLACK_COLOR = (0, 0, 0)
BLACK_PRESSED_COLOR = (0, 0, 64)


class WhiteKey:
    def __init__(self, x, y, width, height, id):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.id = id
        self.state = False
        self.isPressed = False
        self.falseColour = (255, 255, 255)
        self.trueColour = (255, 0, 0)
        self.colour = self.falseColour

    def update(self, state):
        if state:
            self.colour = self.trueColour
        else:
            self.colour = self.falseColour

        return None

    def draw(self, display):
        return pygame.draw.rect(display, WHITE_PRESSED_COLOR if self.isPressed else WHITE_COLOR,
                                self.rect)

    def enable_state(self):
        self.state = True
        return self.state

    def disable_state(self):
        self.state = False
        return self.state

    def set_pressed(self, is_pressed):
        self.isPressed = is_pressed


class BlackKey:
    def __init__(self, x, y, width, height, id):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.id = id
        self.state = False
        self.isPressed = False
        self.falseColour = (0, 0, 0)
        self.trueColour = (255, 0, 0)

    def draw(self, display):
        return pygame.draw.rect(display, BLACK_PRESSED_COLOR if self.isPressed else BLACK_COLOR,
                                self.rect)

    def enable_state(self):
        self.state = True
        return self.state

    def disable_state(self):
        self.state = False
        return self.state

    def set_pressed(self, is_pressed):
        self.isPressed = is_pressed
