import pygame
from GUI.Keyboard import BLACK_KEYS, WHITE_WIDTH, BLACK_WIDTH, PADDING, SPACING

BLACK_TRACK_COLOR = (96, 96, 96)
WHITE_TRACK_COLOR = (111, 111, 111)
NUMBER_OF_KEYS = 32


class NoteTracks:
    def __init__(self, top, bottom):
        self.trackPositions = [PADDING]
        self.whiteTracks = [pygame.Rect(PADDING, top, WHITE_WIDTH, bottom - top)]
        self.blackTracks = []
        for i in range(1, NUMBER_OF_KEYS):
            if i % 12 in BLACK_KEYS:
                left = self.whiteTracks[-1].x + WHITE_WIDTH + (SPACING - BLACK_WIDTH) / 2
                self.blackTracks.append(pygame.Rect(left, top, BLACK_WIDTH, bottom - top))
                self.trackPositions.append(left)
                # print(left)
            else:
                left = self.whiteTracks[-1].x + WHITE_WIDTH + SPACING
                self.whiteTracks.append(pygame.Rect(left, top, WHITE_WIDTH, bottom - top))
                if (i - 1) % 12 in BLACK_KEYS:
                    self.trackPositions.append(self.trackPositions[-1] + BLACK_WIDTH)
                else:
                    self.trackPositions.append(left)
                # print(left)

        if (NUMBER_OF_KEYS - 1) % 12 in BLACK_KEYS:
            self.trackPositions.append(self.blackTracks[-1].x + BLACK_WIDTH)
        else:
            self.trackPositions.append(self.whiteTracks[-1].x + WHITE_WIDTH)

    def draw(self, display):
        self.draw_white(display)
        self.draw_black(display)

    def draw_white(self, display):
        for track in self.whiteTracks:
            pygame.draw.rect(display, WHITE_TRACK_COLOR, track)

    def draw_black(self, display):
        for track in self.blackTracks:
            pygame.draw.rect(display, BLACK_TRACK_COLOR, track)
