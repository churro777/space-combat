import array
import math
import pygame


def generate_laser_fire() -> pygame.mixer.Sound:
    """Synthesize a short laser zap: high-freq sine sweep (800→200Hz) with quick decay."""
    sample_rate = 22050
    duration = 0.15
    num_samples = int(sample_rate * duration)

    samples = array.array("h")  # signed 16-bit
    for i in range(num_samples):
        t = i / sample_rate
        progress = t / duration

        # Frequency sweeps from 800Hz down to 200Hz
        freq = 800 - 600 * progress

        # Quick exponential decay
        amplitude = 32767 * math.exp(-progress * 6)

        sample = int(amplitude * math.sin(2 * math.pi * freq * t))
        sample = max(-32767, min(32767, sample))
        samples.append(sample)

    return pygame.mixer.Sound(buffer=samples)
