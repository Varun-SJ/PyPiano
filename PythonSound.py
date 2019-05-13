import mido
from mingus.midi import fluidsynth


class PythonSound:
    def __init__(self, rate=16000):
        fluidsynth.init('/usr/share/sounds/sf2/FluidR3_GM.sf2', "alsa")

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

        if state and volume:
            fluidsynth.play_Note(note, 0, volume)
        else:
            fluidsynth.stop_Note(note, 0)

    def send_stop(self):
        fluidsynth.stop_everything()

    @staticmethod
    def encode(note, state=0, volume=0):
        first = 16 if state else 0
        first += volume
        second = 128
        second += note
        print(first, second)
        return first, second
