from queue import Queue, Empty
import pygame
from GUI.NoteBlock import Block
from GUI.Keyboard import BLACK_KEYS

NOTE_OFFSET = 48
BLACK_NOTE_COLOR = (0, 150, 0)
WHITE_NOTE_COLOR = (0, 200, 0)
SPEED_MODIFIER = 0.1


class Notes:
    def __init__(self, track_positions, top, bottom, visible_time):
        self.trackPositions = track_positions
        self.top = top
        self.bottom = bottom
        self.totalDuration = visible_time
        self.speed = (bottom - top) / visible_time
        self.newNotes = dict()
        self.finishedNotes = set()
        self.noteDisplayQueue = Queue()
        self.notePlayQueue = Queue()
        self.playingNotes = set()

    def actually_start_new_note(self, note, time):
        if note not in self.newNotes:
            self.newNotes[note] = Note(note, self.trackPositions[note - NOTE_OFFSET],
                                       self.trackPositions[note - NOTE_OFFSET + 1], self.top, self.bottom,
                                       self.speed).start(time)
        else:
            print("Overlaying same notes detected")

    def actually_end_new_note(self, note, time):
        if note in self.newNotes:
            self.finishedNotes.add(self.newNotes.pop(note).end(time))
        else:
            print("No new note to end")

    def start_new_note(self, note, time):
        self.noteDisplayQueue.put((True, note, time), block=False)

    def end_new_note(self, note, time):
        self.noteDisplayQueue.put((False, note, time), block=False)

    def tick(self, dt):
        self.update_notes()

        distance = dt * self.speed
        time = pygame.time.get_ticks()
        for note in self.newNotes.values():
            (time_until_start, time_until_end) = note.tick(distance, time)
            if time_until_start <= 0 and note.note not in self.playingNotes:
                # note started
                self.playingNotes.add(note.note)
                self.notePlayQueue.put((True, note.note), block=False)
            # else:
            #     note did not start yet

        new_finished = set()
        for note in self.finishedNotes:
            (time_until_start, time_until_end) = note.tick(distance, time)
            # print(time_until_start, time_until_end)
            if time_until_end <= 0:
                self.playingNotes.discard(note.note)
                self.notePlayQueue.put((False, note.note), block=False)
            elif time_until_start <= 0 and note.note not in self.playingNotes:
                self.playingNotes.add(note.note)
                self.notePlayQueue.put((True, note.note), block=False)
                new_finished.add(note)
            else:
                new_finished.add(note)

        self.finishedNotes = new_finished

    def update_and_draw(self, time, screen):
        self.update_notes()
        for note in self.newNotes.values():
            note.draw(time, screen)

        new_finished = set()
        for note in self.finishedNotes:
            if note.draw(time, screen):
                new_finished.add(note)

        self.finishedNotes = new_finished

    def update_notes(self):
        try:
            while True:
                (On, note, time) = self.noteDisplayQueue.get(block=False)
                if On:
                    self.actually_start_new_note(note, time)
                else:
                    self.actually_end_new_note(note, time)
                self.noteDisplayQueue.task_done()
        except Empty:
            pass

    def draw(self, display):
        for note in self.newNotes.values():
            pygame.draw.rect(display, BLACK_NOTE_COLOR if note.isBlack else WHITE_NOTE_COLOR, note.get_rectangle())

        for note in self.finishedNotes:
            pygame.draw.rect(display, BLACK_NOTE_COLOR if note.isBlack else WHITE_NOTE_COLOR, note.get_rectangle())


class Note:
    hasStarted = False
    hasEnded = False
    startTime = 0
    endTime = 0

    def __init__(self, note, left, right, beginning, finish, speed):
        self.note = note
        self.beginning = beginning
        self.finish = finish
        self.speed = speed
        self.left = left
        self.right = right
        self.width = right - left
        self.isBlack = note % 12 in BLACK_KEYS
        self.rectangle = Block(left, beginning, right - left, 0)

    def start(self, start_time):
        self.hasStarted = True
        self.startTime = start_time
        return self

    def end(self, end_time):
        self.hasEnded = True
        self.endTime = end_time
        return self

    def tick(self, distance, time):
        if self.rectangle.bottom() > self.finish:
            self.rectangle.move(0, distance)
            self.rectangle.grow(0, -distance)
        elif self.hasEnded:
            self.rectangle.move(0, distance)
        elif self.hasStarted:
            self.rectangle.grow(0, distance)
        return self.startTime - time, self.endTime - time

    def get_rectangle(self):
        return self.rectangle.rectangle

    def draw(self, time, screen):
        (top, bottom) = self.get_vertical_position(time)
        height = bottom - top
        if height > 0:
            pygame.draw.rect(screen, BLACK_NOTE_COLOR if self.isBlack else WHITE_NOTE_COLOR,
                             self.rectangle.set_vertical_pos(top, height))
            pygame.draw.rect(screen, (0, 255, 0),
                             self.rectangle.rectangle, 5)
            return True
        else:
            return False

    def get_vertical_position(self, time):
        if self.startTime == 0:
            return self.beginning, self.beginning
        elif self.endTime == 0:
            if time <= self.startTime:
                return self.beginning, self.finish - (self.startTime - time) * self.speed
            else:
                return self.beginning, self.finish
        if time > self.endTime:
            return self.finish, self.finish
        elif time > self.startTime:
            return self.finish - (self.endTime - time) * self.speed, self.finish
        else:
            return self.finish - (self.endTime - time) * self.speed, self.finish - (self.startTime - time) * self.speed
