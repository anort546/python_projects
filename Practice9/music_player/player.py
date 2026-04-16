import pygame
import os


class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()

        self.tracks = [
            "music/track1.mp3",
            "music/track2.mp3"
        ]
        self.index = 0

    def play(self):
        pygame.mixer.music.load(self.tracks[self.index])
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        self.index = (self.index + 1) % len(self.tracks)
        self.play()

    def prev(self):
        self.index = (self.index - 1) % len(self.tracks)
        self.play()