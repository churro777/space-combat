import pygame
from audio.synth import laser_harmonic_stutter, scan_wide_rising_pulse, contact_triple_rising_pulse


class SoundManager:
    def __init__(self):
        try:
            pygame.mixer.init()
            self.sounds: dict[str, pygame.mixer.Sound] = {
                "laser_fire": laser_harmonic_stutter(),
                "scan_pulse": scan_wide_rising_pulse(),
                "scan_contact": contact_triple_rising_pulse(),
            }
            self.enabled = True
        except pygame.error:
            self.sounds = {}
            self.enabled = False

    def play(self, event_name: str):
        if self.enabled and event_name in self.sounds:
            self.sounds[event_name].play()
