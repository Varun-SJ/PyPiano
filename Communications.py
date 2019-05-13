from threading import Thread
import pigpio
import time
import KeyboardConnection


class Communication_FGPA(Thread):
    def __init__(self, keyboard_connection):
        self.keyboardConnection = keyboard_connection
        super().__init__()
        self.pi = pigpio.pi()
        self.pi.write(11, 1)  # SCLK is high
        self.pi.write(9, 0)  # MISO is low
        self.pi.write(10, 1)  # MOSI is high
        self.pi.write(7, 0)  # SPI_CE1_N
        self.pi.write(8, 1)  # SPI_CE0_N

    def run(self):
        while self.keyboardConnection == True
