import pygame


class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()

        self.tracks = [
            ("Ayesha Erotica - Vacation Bible School", "music/track1.mp3"),
            ("Lightris - Kwik Trip", "music/track2.mp3")
        ]

        self.index = 0
        self.start_time = 0

    def play(self):
        pygame.mixer.music.load(self.tracks[self.index][1])
        pygame.mixer.music.play()
        self.start_time = pygame.time.get_ticks()

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        self.index = (self.index + 1) % len(self.tracks)
        self.play()

    def prev(self):
        self.index = (self.index - 1) % len(self.tracks)
        self.play()

    def get_current_track(self):
        return self.tracks[self.index][0]

    def get_position(self):
        if pygame.mixer.music.get_busy():
            return (pygame.time.get_ticks() - self.start_time) // 1000
        return 0