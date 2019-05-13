import pygame
import pygame.time
import sys

sharpKeys = [1, 3, 6, 8, 10]
START_POS = 0

sequence = [(1, 1, 0),  # for testing
            (3, 1, 0),
            (5, 1, 0),
            (1, 0, 1),
            (2, 1, 1),
            (2, 0, 1),
            (3, 0, 0),
            (3, 1, 1),
            (3, 0, 1),
            (4, 1, 1),
            (4, 0, 1),
            (5, 0, 0)]

TRACK_TIME_LENGTH = 5000  # milliseconds


class Rectangle:
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


class Note:
    hasStarted = False
    hasEnded = False
    pressTimestamp = pygame.time.get_ticks() + TRACK_TIME_LENGTH

    def __init__(self, note):
        self.note = note
        self.isBlack = note % 12 in sharpKeys
        self.rectangle = Rectangle(64 + (64 + 10) * note, START_POS, 64, 0)

    def start(self):
        self.hasStarted = True
        return self

    def end(self):
        self.hasEnded = True
        return self

    def tick(self, dt, speed):
        # self.timeUntilPress -= dt / 1000
        if self.hasEnded:
            self.rectangle.move(0, dt * speed)
        elif self.hasStarted:
            self.rectangle.grow(0, dt * speed)

    def get_rectangle(self):
        return self.rectangle.rectangle

    # def get_timing(self):
    #     return self.timeUntilPress


class Tracks:
    # def __init__(self):

    @staticmethod
    def start():
        pygame.init()

        speed = 0.1  # px/millisecond
        size = 1024, 720

        screen = pygame.display.set_mode(size)

        timer = 0
        seq_length = len(sequence)
        seq_pointer = 0
        spawned_notes = dict()
        notes = set()
        temp = sequence[seq_pointer]
        clock = pygame.time.Clock()
        # clock.tick()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            dt = clock.tick()
            timer -= dt / 1000
            # print(timer)
            if timer <= 0 and seq_pointer < seq_length:
                # print(temp[2], timer, seq_pointer)
                first = True
                while (first or temp[2] <= -timer) and seq_pointer < seq_length:
                    first = False
                    # print(temp, spawned_notes.get(temp[0]))
                    if temp[1] > 0 and spawned_notes.get(temp[0]) is None:
                        spawned_notes[temp[0]] = (Note(temp[0]).start())
                    else:
                        notes.add(spawned_notes.pop(temp[0]).end())
                    seq_pointer += 1
                    if seq_pointer < seq_length:
                        temp = sequence[seq_pointer]
                        timer = temp[2] - timer
                    # print(seq_pointer)

            elif seq_pointer >= seq_length and len(notes) == 0:
                sys.exit()

            screen.fill((20, 20, 20))
            pygame.draw.rect(screen, (200, 0, 0), pygame.Rect(700, 500, 60, 60))

            to_update = []

            for note in spawned_notes.values():
                note.tick(dt, speed)
                pygame.draw.rect(screen, (0, 200, 0), note.get_rectangle())
                to_update.append(note.get_rectangle())

            for note in notes:
                note.tick(dt, speed)
                pygame.draw.rect(screen, (0, 200, 0), note.get_rectangle())
                to_update.append(note.get_rectangle())

            pygame.display.update(to_update)


Tracks.start()
