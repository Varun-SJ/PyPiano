from threading import Thread
import pygame.time
import psutil


class WorkerThread(Thread):
    def __init__(self, function_to_perform):
        super().__init__()
        self.done = False
        self.work = function_to_perform
        p = psutil.Process()
        p.nice(-20)

    def run(self):
        while not self.done:
            self.work()

    def close(self):
        self.done = True


class SongWorker(Thread):
    def __init__(self, tick, draw):
        super().__init__()
        self.done = False
        self.tick = tick
        self.draw = draw
        self.clock = pygame.time.Clock()

    def run(self):
        while not self.done:
            self.tick(self.clock.tick())
            self.draw()

    def close(self):
        self.done = True
