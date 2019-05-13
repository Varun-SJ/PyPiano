class TestSound:
    def __init__(self, rate=16000):
        pass

    def send_mido(self, msg):
        print(msg)
        pass

    def send_pygame_midi(self, msg):
        print(msg)
        pass

    def send_note(self, note, state=1, volume=127):
        print(note, state, volume)
        pass

    def send_stop(self):
        print("reset played notes")

    @staticmethod
    def encode(note, state=0, volume=0):
        pass
