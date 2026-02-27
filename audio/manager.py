import pygame
from audio.synth import generate_laser_fire


class SoundManager:
    def __init__(self):
        try:
            pygame.mixer.init()
            self.sounds: dict[str, pygame.mixer.Sound] = {
                "laser_fire": generate_laser_fire(),
            }
            self.enabled = True
        except pygame.error:
            self.sounds = {}
            self.enabled = False

    def play(self, event_name: str):
        if self.enabled and event_name in self.sounds:
            self.sounds[event_name].play()
