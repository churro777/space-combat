import array
import math
import pygame


def _make_sound(sample_rate: int, duration: float, sample_fn) -> pygame.mixer.Sound:
    """Build a Sound from a callback: sample_fn(t, progress) -> float in -1..1."""
    num_samples = int(sample_rate * duration)
    samples = array.array("h")  # signed 16-bit
    for i in range(num_samples):
        t = i / sample_rate
        progress = t / duration
        value = sample_fn(t, progress)
        sample = int(max(-1.0, min(1.0, value)) * 32767)
        samples.append(sample)
    return pygame.mixer.Sound(buffer=samples)


def laser_sine_sweep() -> pygame.mixer.Sound:
    """Short laser zap: high-freq sine sweep (800->200Hz) with quick decay."""
    def fn(t, progress):
        freq = 800 - 600 * progress
        amplitude = math.exp(-progress * 6)
        return amplitude * math.sin(2 * math.pi * freq * t)
    return _make_sound(22050, 0.15, fn)


def laser_square_buzz() -> pygame.mixer.Sound:
    """Square wave at ~400Hz, short decay, retro 8-bit feel."""
    def fn(t, progress):
        freq = 400
        amplitude = math.exp(-progress * 8)
        sine = math.sin(2 * math.pi * freq * t)
        return amplitude * (1.0 if sine >= 0 else -1.0)
    return _make_sound(22050, 0.12, fn)


def laser_noise_burst() -> pygame.mixer.Sound:
    """White noise shaped with a fast envelope, blaster sound."""
    import random
    rng = random.Random(42)  # deterministic for reproducibility

    def fn(t, progress):
        amplitude = math.exp(-progress * 12)
        return amplitude * (rng.random() * 2 - 1)
    return _make_sound(22050, 0.10, fn)


def laser_dual_tone() -> pygame.mixer.Sound:
    """Two detuned sines (~500Hz and ~520Hz) for wobble/phaser effect."""
    def fn(t, progress):
        amplitude = math.exp(-progress * 5)
        s1 = math.sin(2 * math.pi * 500 * t)
        s2 = math.sin(2 * math.pi * 520 * t)
        return amplitude * (s1 + s2) * 0.5
    return _make_sound(22050, 0.18, fn)


def laser_rising_chirp() -> pygame.mixer.Sound:
    """Upward sweep 200->1200Hz, sci-fi charge-up."""
    def fn(t, progress):
        freq = 200 + 1000 * progress
        amplitude = math.exp(-progress * 4)
        return amplitude * math.sin(2 * math.pi * freq * t)
    return _make_sound(22050, 0.15, fn)


def laser_hard_zap() -> pygame.mixer.Sound:
    """Steep drop 1500->100Hz with overdrive clipping — punchy arcade zap."""
    def fn(t, progress):
        freq = 1500 * (1 - progress) ** 2 + 100
        amplitude = math.exp(-progress * 8)
        raw = math.sin(2 * math.pi * freq * t) * 1.8
        return amplitude * max(-1.0, min(1.0, raw))  # hard clip
    return _make_sound(22050, 0.10, fn)


def laser_fm_bass() -> pygame.mixer.Sound:
    """FM synthesis: carrier modulated by a faster oscillator — thick, bassy laser."""
    def fn(t, progress):
        mod_freq = 600
        car_freq = 180
        mod_index = 8 * (1 - progress)  # modulation fades out
        amplitude = math.exp(-progress * 6)
        mod = math.sin(2 * math.pi * mod_freq * t)
        return amplitude * math.sin(2 * math.pi * car_freq * t + mod_index * mod)
    return _make_sound(22050, 0.14, fn)


def laser_double_tap() -> pygame.mixer.Sound:
    """Two rapid pulses — pew-pew, like a double-barreled shot."""
    def fn(t, progress):
        # Two bursts centered at ~0.03s and ~0.09s
        env1 = math.exp(-((t - 0.025) ** 2) / (2 * 0.008 ** 2))
        env2 = math.exp(-((t - 0.085) ** 2) / (2 * 0.008 ** 2)) * 0.7
        freq1 = 900 - 3000 * max(0, t - 0.01)
        freq2 = 800 - 3000 * max(0, t - 0.07)
        s1 = env1 * math.sin(2 * math.pi * max(freq1, 200) * t)
        s2 = env2 * math.sin(2 * math.pi * max(freq2, 200) * t)
        return s1 + s2
    return _make_sound(22050, 0.13, fn)


def laser_sine_noise_blend() -> pygame.mixer.Sound:
    """Sine sweep blended with filtered noise — gritty sci-fi blaster."""
    import random
    rng = random.Random(99)
    noise_table = [rng.random() * 2 - 1 for _ in range(4000)]

    def fn(t, progress):
        freq = 1000 - 700 * progress
        amplitude = math.exp(-progress * 7)
        tone = math.sin(2 * math.pi * freq * t)
        # Sample noise from table for consistency
        idx = int(t * 22050) % len(noise_table)
        noise = noise_table[idx]
        blend = 0.3 + 0.5 * progress  # more noise toward the end
        return amplitude * (tone * (1 - blend) + noise * blend)
    return _make_sound(22050, 0.12, fn)


def laser_resonant_ping() -> pygame.mixer.Sound:
    """Sharp attack, resonant ring at ~1kHz — metallic ping laser."""
    def fn(t, progress):
        freq = 1000 + 200 * math.sin(2 * math.pi * 3 * t)  # slight vibrato
        # Sharp attack: instant to full, then ring out
        amplitude = math.exp(-progress * 10)
        return amplitude * math.sin(2 * math.pi * freq * t)
    return _make_sound(22050, 0.12, fn)


def laser_steep_pew() -> pygame.mixer.Sound:
    """Steep sine sweep 1400->200Hz, fast decay — classic pew."""
    def fn(t, progress):
        freq = 1400 - 1200 * progress
        amplitude = math.exp(-progress * 9)
        return amplitude * math.sin(2 * math.pi * freq * t)
    return _make_sound(22050, 0.10, fn)


def laser_bounce_sweep() -> pygame.mixer.Sound:
    """Sine sweep down then back up — bwip sound."""
    def fn(t, progress):
        # V-shaped frequency: 1000 -> 200 -> 800
        if progress < 0.5:
            freq = 1000 - 1600 * progress
        else:
            freq = 200 + 1200 * (progress - 0.5)
        amplitude = math.exp(-progress * 5)
        return amplitude * math.sin(2 * math.pi * freq * t)
    return _make_sound(22050, 0.14, fn)


def laser_triple_tap() -> pygame.mixer.Sound:
    """Three rapid sine pulses — pew-pew-pew burst fire."""
    def fn(t, progress):
        total = 0.0
        for i, (center, vol) in enumerate([(0.02, 1.0), (0.06, 0.8), (0.10, 0.6)]):
            env = math.exp(-((t - center) ** 2) / (2 * 0.006 ** 2))
            freq = 1000 - 4000 * max(0, t - (center - 0.01))
            freq = max(freq, 250)
            total += env * vol * math.sin(2 * math.pi * freq * t)
        return total * 0.7
    return _make_sound(22050, 0.14, fn)


def laser_wide_sweep() -> pygame.mixer.Sound:
    """Extra wide sine sweep 2000->150Hz — dramatic sci-fi pew."""
    def fn(t, progress):
        freq = 2000 - 1850 * progress
        amplitude = math.exp(-progress * 7)
        return amplitude * math.sin(2 * math.pi * freq * t)
    return _make_sound(22050, 0.13, fn)


def laser_harmonic_sweep() -> pygame.mixer.Sound:
    """Fundamental + octave sine sweep — richer tone, still clean."""
    def fn(t, progress):
        freq = 900 - 600 * progress
        amplitude = math.exp(-progress * 6)
        fundamental = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.3
        return amplitude * (fundamental + octave) * 0.75
    return _make_sound(22050, 0.15, fn)


def laser_charge_fire() -> pygame.mixer.Sound:
    """Quick rising chirp into a falling sweep — charge then fire."""
    def fn(t, progress):
        if progress < 0.3:
            # Charge up phase
            p = progress / 0.3
            freq = 300 + 900 * p
            amplitude = p * 0.6
        else:
            # Fire phase — the satisfying part
            p = (progress - 0.3) / 0.7
            freq = 1200 - 900 * p
            amplitude = math.exp(-p * 5)
        return amplitude * math.sin(2 * math.pi * freq * t)
    return _make_sound(22050, 0.18, fn)


def laser_double_sweep() -> pygame.mixer.Sound:
    """Two overlapping sine sweeps at different rates — thick laser."""
    def fn(t, progress):
        freq1 = 1000 - 700 * progress
        freq2 = 700 - 400 * progress
        amplitude = math.exp(-progress * 6)
        s1 = math.sin(2 * math.pi * freq1 * t)
        s2 = math.sin(2 * math.pi * freq2 * t) * 0.5
        return amplitude * (s1 + s2) * 0.65
    return _make_sound(22050, 0.15, fn)


def laser_stutter_sweep() -> pygame.mixer.Sound:
    """Sine sweep with amplitude stutter — rapid tremolo laser."""
    def fn(t, progress):
        freq = 900 - 600 * progress
        amplitude = math.exp(-progress * 6)
        tremolo = 0.5 + 0.5 * math.sin(2 * math.pi * 60 * t)
        return amplitude * tremolo * math.sin(2 * math.pi * freq * t)
    return _make_sound(22050, 0.15, fn)


def laser_harmonic_wide_sweep() -> pygame.mixer.Sound:
    """Wide sweep (2000->200Hz) with octave harmonic — dramatic and rich."""
    def fn(t, progress):
        freq = 2000 - 1800 * progress
        amplitude = math.exp(-progress * 6)
        fundamental = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.25
        fifth = math.sin(2 * math.pi * freq * 1.5 * t) * 0.15
        return amplitude * (fundamental + octave + fifth) * 0.7
    return _make_sound(22050, 0.16, fn)


def laser_bounce_chirp() -> pygame.mixer.Sound:
    """Rising chirp that bounces back down — zwip-zwop."""
    def fn(t, progress):
        if progress < 0.4:
            p = progress / 0.4
            freq = 200 + 1400 * p
        else:
            p = (progress - 0.4) / 0.6
            freq = 1600 - 1200 * p
        amplitude = math.exp(-progress * 4)
        return amplitude * math.sin(2 * math.pi * freq * t)
    return _make_sound(22050, 0.16, fn)


def laser_triple_chirp() -> pygame.mixer.Sound:
    """Three rising chirp pulses — sci-fi burst with upward energy."""
    def fn(t, progress):
        total = 0.0
        for center, vol in [(0.02, 1.0), (0.065, 0.85), (0.11, 0.7)]:
            env = math.exp(-((t - center) ** 2) / (2 * 0.007 ** 2))
            local_t = t - (center - 0.015)
            freq = 300 + 6000 * max(0, local_t)
            freq = min(freq, 1500)
            total += env * vol * math.sin(2 * math.pi * freq * t)
        return total * 0.65
    return _make_sound(22050, 0.15, fn)


def laser_charge_burst() -> pygame.mixer.Sound:
    """Longer charge-up into a wide harmonic burst — powerful shot."""
    def fn(t, progress):
        if progress < 0.35:
            p = progress / 0.35
            freq = 200 + 600 * p
            amplitude = p * 0.4
            return amplitude * math.sin(2 * math.pi * freq * t)
        else:
            p = (progress - 0.35) / 0.65
            freq = 1800 - 1400 * p
            amplitude = math.exp(-p * 4)
            fundamental = math.sin(2 * math.pi * freq * t)
            octave = math.sin(2 * math.pi * freq * 2 * t) * 0.3
            return amplitude * (fundamental + octave) * 0.75
    return _make_sound(22050, 0.22, fn)


def laser_warble_sweep() -> pygame.mixer.Sound:
    """Wide sweep with pitch wobble — vibrato laser beam."""
    def fn(t, progress):
        base_freq = 1800 - 1500 * progress
        wobble = 80 * math.sin(2 * math.pi * 25 * t)  # 25Hz vibrato
        freq = base_freq + wobble
        amplitude = math.exp(-progress * 5)
        return amplitude * math.sin(2 * math.pi * freq * t)
    return _make_sound(22050, 0.16, fn)


def laser_harmonic_stutter() -> pygame.mixer.Sound:
    """Harmonic sweep with tremolo — rich stuttering laser."""
    def fn(t, progress):
        freq = 1200 - 800 * progress
        amplitude = math.exp(-progress * 5)
        tremolo = 0.4 + 0.6 * math.sin(2 * math.pi * 50 * t)
        fundamental = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.3
        return amplitude * tremolo * (fundamental + octave) * 0.7
    return _make_sound(22050, 0.16, fn)


def laser_wide_bounce_tap() -> pygame.mixer.Sound:
    """Two wide-sweep pulses with bounce — dramatic double shot."""
    def fn(t, progress):
        total = 0.0
        for center, vol in [(0.03, 1.0), (0.11, 0.75)]:
            env = math.exp(-((t - center) ** 2) / (2 * 0.012 ** 2))
            local_p = max(0, t - (center - 0.02)) / 0.04
            if local_p < 0.5:
                freq = 1800 - 2400 * local_p
            else:
                freq = 600 + 800 * (local_p - 0.5)
            freq = max(freq, 300)
            total += env * vol * math.sin(2 * math.pi * freq * t)
        return total * 0.65
    return _make_sound(22050, 0.17, fn)


def laser_slow_charge_beam() -> pygame.mixer.Sound:
    """Slow rising charge into sustained harmonic beam — heavy weapon feel."""
    def fn(t, progress):
        if progress < 0.4:
            p = progress / 0.4
            freq = 150 + 500 * p * p  # accelerating rise
            amplitude = p * 0.5
            return amplitude * math.sin(2 * math.pi * freq * t)
        else:
            p = (progress - 0.4) / 0.6
            freq = 1400 - 600 * p
            amplitude = math.exp(-p * 3)
            fundamental = math.sin(2 * math.pi * freq * t)
            octave = math.sin(2 * math.pi * freq * 2 * t) * 0.25
            tremolo = 0.7 + 0.3 * math.sin(2 * math.pi * 35 * t)
            return amplitude * tremolo * (fundamental + octave) * 0.7
    return _make_sound(22050, 0.25, fn)


def laser_harmonic_chirp() -> pygame.mixer.Sound:
    """Rising chirp with harmonics — richer version of the rising chirp."""
    def fn(t, progress):
        freq = 200 + 1200 * progress
        amplitude = math.exp(-progress * 4)
        fundamental = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.3
        fifth = math.sin(2 * math.pi * freq * 1.5 * t) * 0.15
        return amplitude * (fundamental + octave + fifth) * 0.7
    return _make_sound(22050, 0.16, fn)


def laser_fast_charge_snap() -> pygame.mixer.Sound:
    """Very quick charge into a sharp harmonic snap — snappy shot."""
    def fn(t, progress):
        if progress < 0.2:
            p = progress / 0.2
            freq = 300 + 1200 * p * p
            amplitude = p * 0.7
            return amplitude * math.sin(2 * math.pi * freq * t)
        else:
            p = (progress - 0.2) / 0.8
            freq = 1500 - 800 * p
            amplitude = math.exp(-p * 8)
            fundamental = math.sin(2 * math.pi * freq * t)
            octave = math.sin(2 * math.pi * freq * 2 * t) * 0.25
            return amplitude * (fundamental + octave) * 0.8
    return _make_sound(22050, 0.12, fn)


def laser_rising_triple_burst() -> pygame.mixer.Sound:
    """Three rising chirp pulses, each higher pitched — escalating burst."""
    def fn(t, progress):
        total = 0.0
        for i, (center, vol, base) in enumerate([
            (0.025, 1.0, 250), (0.07, 0.9, 400), (0.115, 0.8, 550)
        ]):
            env = math.exp(-((t - center) ** 2) / (2 * 0.008 ** 2))
            local_t = max(0, t - (center - 0.015))
            freq = base + 5000 * local_t
            freq = min(freq, base + 1000)
            fundamental = math.sin(2 * math.pi * freq * t)
            octave = math.sin(2 * math.pi * freq * 2 * t) * 0.2
            total += env * vol * (fundamental + octave) * 0.8
        return total * 0.6
    return _make_sound(22050, 0.16, fn)


def laser_charge_harmonic_beam() -> pygame.mixer.Sound:
    """Medium charge into rich sustained harmonic chirp — heavy beam weapon."""
    def fn(t, progress):
        if progress < 0.3:
            p = progress / 0.3
            freq = 180 + 800 * p * p
            amplitude = p * 0.5
            return amplitude * math.sin(2 * math.pi * freq * t)
        else:
            p = (progress - 0.3) / 0.7
            # Slowly rising freq in the beam phase
            freq = 1000 + 400 * p
            amplitude = math.exp(-p * 2.5)
            fundamental = math.sin(2 * math.pi * freq * t)
            octave = math.sin(2 * math.pi * freq * 2 * t) * 0.3
            fifth = math.sin(2 * math.pi * freq * 1.5 * t) * 0.15
            stutter = 0.5 + 0.5 * math.sin(2 * math.pi * 45 * t)
            return amplitude * stutter * (fundamental + octave + fifth) * 0.6
    return _make_sound(22050, 0.22, fn)


def laser_chirp_bounce_tap() -> pygame.mixer.Sound:
    """Two chirp pulses that rise then dip — bouncy double chirp."""
    def fn(t, progress):
        total = 0.0
        for center, vol in [(0.03, 1.0), (0.10, 0.8)]:
            env = math.exp(-((t - center) ** 2) / (2 * 0.01 ** 2))
            local_t = t - (center - 0.015)
            if local_t < 0.015:
                freq = 300 + 80000 * max(0, local_t)  # rising
            else:
                freq = 1500 - 30000 * (local_t - 0.015)  # dip back
                freq = max(freq, 400)
            total += env * vol * math.sin(2 * math.pi * freq * t)
        return total * 0.7
    return _make_sound(22050, 0.15, fn)


def laser_swell_shot() -> pygame.mixer.Sound:
    """Smooth swell up with harmonics, quick release — whomp."""
    def fn(t, progress):
        # Bell-curve amplitude peaking at 40%
        amplitude = math.exp(-((progress - 0.4) ** 2) / (2 * 0.15 ** 2))
        freq = 300 + 1000 * progress
        fundamental = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.3
        return amplitude * (fundamental + octave) * 0.75
    return _make_sound(22050, 0.18, fn)


def laser_ascending_rings() -> pygame.mixer.Sound:
    """Four rapid ascending tones — musical rising arpeggio laser."""
    def fn(t, progress):
        total = 0.0
        freqs = [400, 600, 900, 1350]
        for i, (center, base_freq) in enumerate(
            zip([0.02, 0.05, 0.08, 0.11], freqs)
        ):
            env = math.exp(-((t - center) ** 2) / (2 * 0.006 ** 2))
            fundamental = math.sin(2 * math.pi * base_freq * t)
            octave = math.sin(2 * math.pi * base_freq * 2 * t) * 0.2
            total += env * (1.0 - i * 0.1) * (fundamental + octave)
        return total * 0.55
    return _make_sound(22050, 0.15, fn)


def laser_quick_charge_chirp() -> pygame.mixer.Sound:
    """Tiny charge blip into a fast rising harmonic chirp — zippy."""
    def fn(t, progress):
        if progress < 0.15:
            p = progress / 0.15
            freq = 200 + 300 * p
            amplitude = p * 0.4
            return amplitude * math.sin(2 * math.pi * freq * t)
        else:
            p = (progress - 0.15) / 0.85
            freq = 500 + 1200 * p
            amplitude = math.exp(-p * 5)
            fundamental = math.sin(2 * math.pi * freq * t)
            octave = math.sin(2 * math.pi * freq * 2 * t) * 0.25
            return amplitude * (fundamental + octave) * 0.8
    return _make_sound(22050, 0.14, fn)


# Backwards compat alias
generate_laser_fire = laser_sine_sweep
