import pigpio
import mido
from math import floor


class SPIConnection:
    def __init__(self, rate=50000):
        self.pi = pigpio.pi()
        self.handler = self.pi.spi_open(0, rate, 0)

    def send_mido(self, msg: mido.messages):
        if msg.type == "note_off":
            self.send_note(note=msg.note, state=0)
        elif msg.type == "note_on":
            state = 1
            if hasattr(msg, "velocity"):
                volume = msg.velocity
                if hasattr(msg, "note"):
                    note = msg.note
                    self.send_note(note, state, volume)

    def send_pygame_midi(self, msg):
        note = msg[0][1]
        volume = msg[0][2]
        self.send_note(note=note, volume=volume)

    def send_note(self, note, state=1, volume=127):
        note = note % 128
        if not state:
            volume = 0
        else:
            if volume == 0:
                state = 0

        first, second = self.encode(note, state, volume)
        self.pi.spi_write(0, (first, second))

    def send_stop(self):
        # 0011, 0101, 24, 80
        self.pi.spi_write(0, (48, 0))
        # self.pi.spi_write(0, (80, 0))
        for x in range(48, 80):
            self.send_note(x, 0)

    @staticmethod
    def encode(note, state=0, volume=0):
        first = 16 if state else 0
        first += floor(volume / 8)
        second = 128
        second += note
        # print(first, second)
        return first, second
