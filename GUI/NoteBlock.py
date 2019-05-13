import pygame


class Block:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rectangle = pygame.Rect(x, y, width, height)

    def move(self, x, y):
        self.x += x
        self.y += y
        self.rectangle.topleft = self.x, self.y

    def grow(self, dw, dh):
        self.width += dw
        self.height += dh
        self.rectangle.size = self.width, self.height

    def bottom(self):
        return self.y + self.height

    def set_vertical_pos(self, top, height):
        self.y = top
        self.height = height
        self.rectangle.y = self.y
        self.rectangle.height = self.height
        return self.rectangle
