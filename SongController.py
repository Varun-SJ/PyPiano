import os
from enum import Enum
from queue import Empty
from collections import deque
import pygame.time
from mido import MidiFile
from GUI.Keyboard import Keyboard
from GUI.NoteTracks import NoteTracks
from Experimental.TestSound import TestSound
# from PythonSound import PythonSound
from SPIConnection import SPIConnection
from Notes import Notes, NOTE_OFFSET
from KeyboardConnection import MidiKeyboard
from WorkerThread import SongWorker, WorkerThread

# from SPIConnection import SPIConnection
# from PythonSound import PythonSound

BACKGROUND_COLOR = (127, 127, 127)
ALLOWED_DELAY = 15  # time in milliseconds
TRACKS_TOP = 64
TRACKS_BOTTOM = KEYBOARD_TOP = 512 + 256
KEYBOARD_BOTTOM = 1024 - 4


# NOTE_VISIBILITY_TIME = 5000  # milliseconds


class AudioModes(Enum):
    # NONE = 0
    SONG_ONLY = 1
    KEYBOARD_ONLY = 2
    # HYBRID = 3
    # BOTH = 4


KEYBOARD_ON = [AudioModes.KEYBOARD_ONLY]
SEQUENCE_ON = [AudioModes.SONG_ONLY]


class Song:
    def __init__(self, screen, clock, path_to_file, midi_keyboard, audio_generator=TestSound(), speed_modifier=1,
                 selected_input=AudioModes.KEYBOARD_ONLY):
        self.NOTE_VISIBILITY_TIME = 3000

        self.workerThreads = []

        self.screen = screen
        self.midiKeyboard = midi_keyboard
        # self.workerThreads.append(self.midiKeyboard)
        self.keyboard = Keyboard(KEYBOARD_TOP, KEYBOARD_BOTTOM)
        self.noteTracks = NoteTracks(TRACKS_TOP, TRACKS_BOTTOM)
        self.notes = Notes(self.noteTracks.trackPositions, TRACKS_TOP, TRACKS_BOTTOM, self.NOTE_VISIBILITY_TIME)
        self.clock = clock
        self.done = False

        # self.background = pygame.image.load("./GUI/Background.jpg")

        self.score = 0
        self.scoreDisplay = pygame.font.SysFont("Broadway", 32)

        self.key_presses = dict()
        self.note_starts = dict()

        self.key_releases = dict()
        self.note_ends = dict()

        self.playingNotes = set()
        # read in the midi file
        self.midi_file = MidiFile(path_to_file)

        self.timer = 0
        self.song = iter(self.midi_file)
        self.current_event = next(self.song, None)
        self.noteQueue = deque()
        # self.scheduled_note = None

        display = WorkerThread(self.draw)
        display.start()
        self.workerThreads.append(display)
        # display2 = WorkerThread(self.draw)
        # display2.start()
        # self.workerThreads.append(display2)

        self.speedMod = speed_modifier

        self.audioGenerator = audio_generator
        self.audioMode = selected_input

        # self.loop()

    def start(self):
        return self.loop()

    def process_pressed_keys(self):
        for key in self.midiKeyboard.get_pressed_keys():
            if self.audioMode in KEYBOARD_ON:
                self.audioGenerator.send_pygame_midi(key)
            note_number = key[0][1]
            if NOTE_OFFSET <= note_number < NOTE_OFFSET + 32:
                self.keyboard.press_key(note_number - NOTE_OFFSET)
                self.score += self.check_key_timing(note_number, self.note_starts, self.key_presses)

    def process_held_keys(self, dt):
        # temp = set()
        for key in self.midiKeyboard.get_held_keys():
            if key[0][1] in self.playingNotes and NOTE_OFFSET <= key[0][1] < NOTE_OFFSET + 32:
                self.score += dt
                # temp.add(key[0][1])
            # else:
            #     self.score -= dt
        # self.score -= dt * len(self.notes.playingNotes.difference(temp))

    def process_released_keys(self):
        for key in self.midiKeyboard.get_released_keys():
            if self.audioMode in KEYBOARD_ON:
                self.audioGenerator.send_pygame_midi(key)
            note_number = key[0][1]
            if NOTE_OFFSET <= note_number < NOTE_OFFSET + 32:
                self.keyboard.release_key(note_number - NOTE_OFFSET)
                self.score += self.check_key_timing(note_number, self.note_ends, self.key_releases)

    def create_new_note(self, midi_event, time):
        note_number = midi_event.note
        self.noteQueue.append((midi_event, time))
        if NOTE_OFFSET <= note_number < NOTE_OFFSET + 32:
            self.notes.start_new_note(note_number, time)
        # else:
        #     print("Can't start note off-screen, skipping")

    def end_new_note(self, midi_event, time):
        note_number = midi_event.note
        self.noteQueue.append((midi_event, time))
        if NOTE_OFFSET <= note_number < NOTE_OFFSET + 32:
            self.notes.end_new_note(note_number, time)
        # else:
        #     print("Can't end note off-screen, skipping")

    def update_playing_note(self):
        try:
            while True:
                (on, note) = self.notes.notePlayQueue.get(block=False)
                if on:
                    if self.audioMode in SEQUENCE_ON:
                        self.audioGenerator.send_note(note, state=1)
                    self.score += self.check_key_timing(note, self.key_presses, self.note_starts)
                else:
                    if self.audioMode in SEQUENCE_ON:
                        self.audioGenerator.send_note(note, state=0)
                    self.score += self.check_key_timing(note, self.key_releases, self.note_ends)
                self.notes.notePlayQueue.task_done()
        except Empty:
            pass

    @staticmethod
    def check_key_timing(note, check_dict, put_dict):
        if note in check_dict:
            return 250 - (pygame.time.get_ticks() - check_dict.pop(note))
        else:
            put_dict[note] = pygame.time.get_ticks()
            return 0

    def draw(self):
        # self.screen.blit(self.background, (0, 0))
        self.screen.fill(BACKGROUND_COLOR)
        self.noteTracks.draw(self.screen)
        self.notes.update_and_draw(pygame.time.get_ticks(), self.screen)
        self.keyboard.draw_keys(self.screen)
        # self.keyboard.draw_keys_optimized(self.screen)
        self.screen.blit(self.scoreDisplay.render("Score = " + repr(self.score), True, (0, 0, 0)), (16, 16))
        pygame.display.update()

    def loop(self):
        self.clock.tick()
        while not self.done:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.audioGenerator.send_stop()
                    for worker in self.workerThreads:
                        worker.close()
                    self.done = True
                    break
                elif e.type == pygame.KEYDOWN:
                    self.audioGenerator.send_stop()
                    for worker in self.workerThreads:
                        worker.close()
                    self.done = True
                    return self.score

            dt = self.clock.tick() * self.speedMod
            current_time = pygame.time.get_ticks()
            time = current_time + self.NOTE_VISIBILITY_TIME

            # load in new events
            self.timer -= dt / 1000
            if self.timer <= 0 and self.current_event is not None:
                first = True
                while self.current_event is not None and (first or self.current_event.time <= -self.timer):
                    first = False
                    if self.current_event.type == "note_on":
                        self.create_new_note(self.current_event, time + self.timer + self.current_event.time)
                    elif self.current_event.type == "note_off":
                        self.end_new_note(self.current_event, time + self.timer + self.current_event.time)

                    self.current_event = next(self.song, None)
                    if self.current_event is not None:
                        self.timer = self.current_event.time - self.timer

            elif self.current_event is None and len(self.notes.finishedNotes) <= 0 and len(self.note_ends) <= 0:
                self.audioGenerator.send_stop()
                for worker in self.workerThreads:
                    worker.close()
                self.done = True

            self.process_pressed_keys()

            self.process_held_keys(dt)

            self.process_released_keys()

            self.update_playing_note()

            # update currently playing notes based on sequence
            try:
                while self.noteQueue[0][1] <= current_time:
                    note = self.noteQueue.popleft()
                    if self.audioMode in SEQUENCE_ON:
                        self.audioGenerator.send_mido(note[0])
                    if note[0].type == "note_on":
                        self.score += self.check_key_timing(note[0].note, self.key_presses, self.note_starts)
                        self.playingNotes.add(note[0].note)
                    else:
                        self.score += self.check_key_timing(note[0].note, self.key_releases, self.note_ends)
                        self.playingNotes.discard(note[0].note)
            except IndexError:
                pass

            # remove all of the event times that have expired and are no longer relevant
            expiry_time = pygame.time.get_ticks() - 250
            self.key_presses = {i: v for (i, v) in self.key_presses.items() if v > expiry_time}
            self.key_releases = {i: v for (i, v) in self.key_releases.items() if v > expiry_time}
            self.note_starts = {i: v for (i, v) in self.note_starts.items() if v > expiry_time}
            self.note_ends = {i: v for (i, v) in self.note_ends.items() if v > expiry_time}

        return self.score


if __name__ == "__main__":
    # 1920 - 1280
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1920 - 1280, 0)
    keyboard = MidiKeyboard(lambda x: print(x))
    song = Song(pygame.display.set_mode((1280, 1024), pygame.NOFRAME), pygame.time.Clock(), "./Songs/Old_MacDonald.mid",
                keyboard, TestSound(), 1, AudioModes.SONG_ONLY)
    print(song.start())
