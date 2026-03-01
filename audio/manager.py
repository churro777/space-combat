import pygame
from audio.synth import (
    laser_harmonic_stutter, scan_wide_rising_pulse,
    contact_triple_rising_pulse, missile_sustained_burn,
    explosion_massive_blast, shield_thump_ring,
    shield_recharge_pulse_rise, destroy_fire_crackle,
    music_intro_arpeggio, music_loop_combat_pulse,
)


class SoundManager:
    def __init__(self):
        try:
            pygame.mixer.init()
            self.sounds: dict[str, pygame.mixer.Sound] = {
                "laser_fire": laser_harmonic_stutter(),
                "scan_pulse": scan_wide_rising_pulse(),
                "scan_contact": contact_triple_rising_pulse(),
                "missile_launch": missile_sustained_burn(),
                "missile_explosion": explosion_massive_blast(),
                "shield_hit": shield_thump_ring(),
                "shield_recharge": shield_recharge_pulse_rise(),
                "ship_destroy": destroy_fire_crackle(),
            }
            self.music_intro = music_intro_arpeggio()
            self.music_loop = music_loop_combat_pulse()
            self._music_channel = pygame.mixer.Channel(7)
            self.enabled = True
        except pygame.error:
            self.sounds = {}
            self.music_intro = None
            self.music_loop = None
            self._music_channel = None
            self.enabled = False

    def play(self, event_name: str):
        if self.enabled and event_name in self.sounds:
            self.sounds[event_name].play()

    def play_music_intro(self):
        if self.enabled and self._music_channel and self.music_intro:
            self._music_channel.play(self.music_intro, loops=-1)

    def transition_to_game(self):
        if self.enabled and self._music_channel and self.music_loop:
            self._music_channel.play(self.music_loop, loops=-1)

    def stop_music(self):
        if self.enabled and self._music_channel:
            self._music_channel.stop()
