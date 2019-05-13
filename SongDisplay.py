from threading import Thread
import pygame


class SongDisplay(Thread):
    def __init__(self, draw):
        super().__init__()
        self.done = False
        self.draw = draw

    def run(self):
        while not self.done:
            self.draw()
