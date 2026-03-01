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


# --- Scan pulse sounds ---

def scan_sonar_ping() -> pygame.mixer.Sound:
    """Classic sonar ping — single clean tone with long ring-out."""
    def fn(t, progress):
        freq = 1200
        amplitude = math.exp(-progress * 4)
        return amplitude * math.sin(2 * math.pi * freq * t)
    return _make_sound(22050, 0.35, fn)


def scan_rising_ping() -> pygame.mixer.Sound:
    """Quick rising tone that rings out — radar sweep feel."""
    def fn(t, progress):
        if progress < 0.15:
            freq = 600 + 4000 * (progress / 0.15)
        else:
            freq = 1200
        amplitude = math.exp(-progress * 3.5)
        return amplitude * math.sin(2 * math.pi * freq * t)
    return _make_sound(22050, 0.35, fn)


def scan_double_ping() -> pygame.mixer.Sound:
    """Two quick pings at different pitches — bip-bip."""
    def fn(t, progress):
        env1 = math.exp(-((t - 0.03) ** 2) / (2 * 0.015 ** 2))
        env2 = math.exp(-((t - 0.12) ** 2) / (2 * 0.015 ** 2)) * 0.7
        s1 = env1 * math.sin(2 * math.pi * 1000 * t)
        s2 = env2 * math.sin(2 * math.pi * 1400 * t)
        return s1 + s2
    return _make_sound(22050, 0.25, fn)


def scan_harmonic_ping() -> pygame.mixer.Sound:
    """Sonar ping with octave harmonic — richer, fuller ping."""
    def fn(t, progress):
        freq = 1000
        amplitude = math.exp(-progress * 3.5)
        fundamental = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.3
        fifth = math.sin(2 * math.pi * freq * 1.5 * t) * 0.15
        return amplitude * (fundamental + octave + fifth) * 0.7
    return _make_sound(22050, 0.4, fn)


def scan_chirp_ping() -> pygame.mixer.Sound:
    """Fast upward chirp into a ringing tone — electronic radar."""
    def fn(t, progress):
        if progress < 0.1:
            p = progress / 0.1
            freq = 400 + 1000 * p * p
            amplitude = p
        else:
            freq = 1400
            p = (progress - 0.1) / 0.9
            amplitude = math.exp(-p * 4)
        return amplitude * math.sin(2 * math.pi * freq * t)
    return _make_sound(22050, 0.3, fn)


def scan_sweep_ring() -> pygame.mixer.Sound:
    """Downward sweep into a sustained ring — sonar broadcast."""
    def fn(t, progress):
        if progress < 0.2:
            p = progress / 0.2
            freq = 2000 - 1000 * p
        else:
            freq = 1000
        amplitude = math.exp(-progress * 3)
        return amplitude * math.sin(2 * math.pi * freq * t)
    return _make_sound(22050, 0.35, fn)


def scan_pulse_wave() -> pygame.mixer.Sound:
    """Pulsing tone that fades — like a radar dish rotating."""
    def fn(t, progress):
        freq = 1100
        amplitude = math.exp(-progress * 3)
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 12 * t)
        return amplitude * pulse * math.sin(2 * math.pi * freq * t)
    return _make_sound(22050, 0.35, fn)


def scan_harmonic_chirp_ping() -> pygame.mixer.Sound:
    """Rising chirp with harmonics into a ring — rich electronic ping."""
    def fn(t, progress):
        if progress < 0.12:
            p = progress / 0.12
            freq = 300 + 900 * p * p
            amplitude = p * 0.8
        else:
            freq = 1200
            p = (progress - 0.12) / 0.88
            amplitude = math.exp(-p * 3.5)
        fundamental = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.25
        return amplitude * (fundamental + octave) * 0.8
    return _make_sound(22050, 0.35, fn)


def scan_pulse_chirp() -> pygame.mixer.Sound:
    """Pulsing tone with rising chirp intro — radar powering up."""
    def fn(t, progress):
        if progress < 0.1:
            p = progress / 0.1
            freq = 400 + 700 * p * p
            amplitude = p * 0.7
        else:
            freq = 1100
            p = (progress - 0.1) / 0.9
            amplitude = math.exp(-p * 3)
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 14 * t)
        fundamental = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.2
        return amplitude * pulse * (fundamental + octave) * 0.8
    return _make_sound(22050, 0.4, fn)


def scan_slow_pulse() -> pygame.mixer.Sound:
    """Slower, deeper pulsing tone — ominous scanning feel."""
    def fn(t, progress):
        freq = 900
        amplitude = math.exp(-progress * 2.5)
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 8 * t)
        fundamental = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.25
        return amplitude * pulse * (fundamental + octave) * 0.75
    return _make_sound(22050, 0.45, fn)


def scan_harmonic_pulse_sweep() -> pygame.mixer.Sound:
    """Pulsing harmonic tone with slowly rising pitch — scanning upward."""
    def fn(t, progress):
        freq = 800 + 500 * progress
        amplitude = math.exp(-progress * 2.5)
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 10 * t)
        fundamental = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.3
        fifth = math.sin(2 * math.pi * freq * 1.5 * t) * 0.15
        return amplitude * pulse * (fundamental + octave + fifth) * 0.65
    return _make_sound(22050, 0.4, fn)


def scan_chirp_pulse_ring() -> pygame.mixer.Sound:
    """Rising chirp into a pulsing harmonic ring — electronic sonar."""
    def fn(t, progress):
        if progress < 0.15:
            p = progress / 0.15
            freq = 300 + 800 * p * p
            amplitude = p * 0.8
            pulse = 1.0
        else:
            freq = 1100
            p = (progress - 0.15) / 0.85
            amplitude = math.exp(-p * 3)
            pulse = 0.4 + 0.6 * math.sin(2 * math.pi * 12 * t)
        fundamental = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.3
        return amplitude * pulse * (fundamental + octave) * 0.75
    return _make_sound(22050, 0.4, fn)


def scan_fast_pulse_harmonic() -> pygame.mixer.Sound:
    """Faster pulsing with rich harmonics — urgent scan."""
    def fn(t, progress):
        freq = 1200
        amplitude = math.exp(-progress * 3.5)
        pulse = 0.4 + 0.6 * math.sin(2 * math.pi * 18 * t)
        fundamental = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.25
        fifth = math.sin(2 * math.pi * freq * 1.5 * t) * 0.15
        return amplitude * pulse * (fundamental + octave + fifth) * 0.65
    return _make_sound(22050, 0.3, fn)


def scan_dual_pulse() -> pygame.mixer.Sound:
    """Two pulsing tones at different frequencies — wide scan."""
    def fn(t, progress):
        amplitude = math.exp(-progress * 3)
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 11 * t)
        s1 = math.sin(2 * math.pi * 1000 * t)
        s2 = math.sin(2 * math.pi * 1300 * t) * 0.6
        octave = math.sin(2 * math.pi * 2000 * t) * 0.2
        return amplitude * pulse * (s1 + s2 + octave) * 0.5
    return _make_sound(22050, 0.4, fn)


def scan_rising_dual_pulse() -> pygame.mixer.Sound:
    """Two rising tones pulsing together — expanding scan wave."""
    def fn(t, progress):
        freq1 = 700 + 600 * progress
        freq2 = 1000 + 500 * progress
        amplitude = math.exp(-progress * 2.5)
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 11 * t)
        s1 = math.sin(2 * math.pi * freq1 * t)
        s2 = math.sin(2 * math.pi * freq2 * t) * 0.6
        octave = math.sin(2 * math.pi * freq1 * 2 * t) * 0.2
        return amplitude * pulse * (s1 + s2 + octave) * 0.5
    return _make_sound(22050, 0.4, fn)


def scan_triple_tone_sweep() -> pygame.mixer.Sound:
    """Three rising tones pulsing — wide harmonic scan."""
    def fn(t, progress):
        freq1 = 600 + 500 * progress
        freq2 = 900 + 400 * progress
        freq3 = 1200 + 300 * progress
        amplitude = math.exp(-progress * 2.5)
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 10 * t)
        s1 = math.sin(2 * math.pi * freq1 * t)
        s2 = math.sin(2 * math.pi * freq2 * t) * 0.7
        s3 = math.sin(2 * math.pi * freq3 * t) * 0.4
        return amplitude * pulse * (s1 + s2 + s3) * 0.45
    return _make_sound(22050, 0.4, fn)


def scan_accelerating_pulse_sweep() -> pygame.mixer.Sound:
    """Rising dual tones with accelerating pulse rate — scan intensifying."""
    def fn(t, progress):
        freq1 = 800 + 600 * progress
        freq2 = 1100 + 500 * progress
        amplitude = math.exp(-progress * 2.5)
        pulse_rate = 8 + 15 * progress  # speeds up
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * pulse_rate * t)
        s1 = math.sin(2 * math.pi * freq1 * t)
        s2 = math.sin(2 * math.pi * freq2 * t) * 0.6
        return amplitude * pulse * (s1 + s2) * 0.6
    return _make_sound(22050, 0.4, fn)


def scan_wide_rising_pulse() -> pygame.mixer.Sound:
    """Wide-spaced dual tones rising with pulse — big open scan."""
    def fn(t, progress):
        freq1 = 500 + 700 * progress
        freq2 = 1200 + 400 * progress
        amplitude = math.exp(-progress * 2.5)
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 9 * t)
        s1 = math.sin(2 * math.pi * freq1 * t)
        s2 = math.sin(2 * math.pi * freq2 * t) * 0.5
        octave = math.sin(2 * math.pi * freq2 * 2 * t) * 0.15
        return amplitude * pulse * (s1 + s2 + octave) * 0.55
    return _make_sound(22050, 0.45, fn)


def scan_converging_pulse() -> pygame.mixer.Sound:
    """Two tones that converge in pitch while pulsing — locking on."""
    def fn(t, progress):
        freq1 = 600 + 500 * progress
        freq2 = 1500 - 400 * progress
        amplitude = math.exp(-progress * 2.5)
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 11 * t)
        s1 = math.sin(2 * math.pi * freq1 * t)
        s2 = math.sin(2 * math.pi * freq2 * t) * 0.6
        return amplitude * pulse * (s1 + s2) * 0.6
    return _make_sound(22050, 0.4, fn)


def scan_harmonic_rising_spread() -> pygame.mixer.Sound:
    """Harmonics that spread apart while rising and pulsing — expanding wave."""
    def fn(t, progress):
        base = 800 + 400 * progress
        spread = 1.0 + 0.5 * progress  # harmonics widen
        amplitude = math.exp(-progress * 2.5)
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 10 * t)
        s1 = math.sin(2 * math.pi * base * t)
        s2 = math.sin(2 * math.pi * base * spread * t) * 0.5
        s3 = math.sin(2 * math.pi * base * spread * 1.5 * t) * 0.25
        return amplitude * pulse * (s1 + s2 + s3) * 0.55
    return _make_sound(22050, 0.4, fn)


# --- Scan contact sounds ---

def contact_rising_blip() -> pygame.mixer.Sound:
    """Quick rising two-tone blip — target acquired."""
    def fn(t, progress):
        freq = 800 + 1200 * progress
        amplitude = math.exp(-progress * 6)
        fundamental = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.25
        return amplitude * (fundamental + octave) * 0.8
    return _make_sound(22050, 0.12, fn)


def contact_double_blip() -> pygame.mixer.Sound:
    """Two short rising blips — bip-bip confirmation."""
    def fn(t, progress):
        total = 0.0
        for center, vol, base in [(0.02, 1.0, 900), (0.07, 0.8, 1200)]:
            env = math.exp(-((t - center) ** 2) / (2 * 0.008 ** 2))
            local_t = max(0, t - (center - 0.01))
            freq = base + 3000 * local_t
            freq = min(freq, base + 600)
            fundamental = math.sin(2 * math.pi * freq * t)
            octave = math.sin(2 * math.pi * freq * 2 * t) * 0.2
            total += env * vol * (fundamental + octave)
        return total * 0.7
    return _make_sound(22050, 0.12, fn)


def contact_harmonic_chime() -> pygame.mixer.Sound:
    """Short harmonic chime — rich detection alert."""
    def fn(t, progress):
        freq = 1200 + 400 * progress
        amplitude = math.exp(-progress * 7)
        s1 = math.sin(2 * math.pi * freq * t)
        s2 = math.sin(2 * math.pi * freq * 1.5 * t) * 0.3
        s3 = math.sin(2 * math.pi * freq * 2 * t) * 0.2
        return amplitude * (s1 + s2 + s3) * 0.65
    return _make_sound(22050, 0.15, fn)


def contact_pulse_blip() -> pygame.mixer.Sound:
    """Rising blip with quick pulse — urgent detection."""
    def fn(t, progress):
        freq = 900 + 800 * progress
        amplitude = math.exp(-progress * 5)
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 25 * t)
        fundamental = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.2
        return amplitude * pulse * (fundamental + octave) * 0.8
    return _make_sound(22050, 0.12, fn)


def contact_ascending_chime() -> pygame.mixer.Sound:
    """Three quick ascending tones — musical detection alert."""
    def fn(t, progress):
        total = 0.0
        for center, freq in [(0.015, 800), (0.045, 1100), (0.075, 1500)]:
            env = math.exp(-((t - center) ** 2) / (2 * 0.006 ** 2))
            fundamental = math.sin(2 * math.pi * freq * t)
            octave = math.sin(2 * math.pi * freq * 2 * t) * 0.2
            total += env * (fundamental + octave)
        return total * 0.55
    return _make_sound(22050, 0.12, fn)


def contact_dual_tone_rise() -> pygame.mixer.Sound:
    """Two tones rising together — wide harmonic detection blip."""
    def fn(t, progress):
        freq1 = 800 + 600 * progress
        freq2 = 1100 + 500 * progress
        amplitude = math.exp(-progress * 6)
        s1 = math.sin(2 * math.pi * freq1 * t)
        s2 = math.sin(2 * math.pi * freq2 * t) * 0.6
        octave = math.sin(2 * math.pi * freq1 * 2 * t) * 0.15
        return amplitude * (s1 + s2 + octave) * 0.6
    return _make_sound(22050, 0.12, fn)


def contact_spread_chime() -> pygame.mixer.Sound:
    """Harmonics that spread apart quickly — sparkling detection."""
    def fn(t, progress):
        base = 1000 + 500 * progress
        spread = 1.0 + 0.8 * progress
        amplitude = math.exp(-progress * 6)
        s1 = math.sin(2 * math.pi * base * t)
        s2 = math.sin(2 * math.pi * base * spread * t) * 0.4
        s3 = math.sin(2 * math.pi * base * spread * 1.5 * t) * 0.2
        return amplitude * (s1 + s2 + s3) * 0.65
    return _make_sound(22050, 0.13, fn)


def contact_triple_rising_pulse() -> pygame.mixer.Sound:
    """Three rising pulsed blips — escalating alert."""
    def fn(t, progress):
        total = 0.0
        for center, vol, base in [(0.02, 1.0, 700), (0.055, 0.9, 1000), (0.09, 0.8, 1350)]:
            env = math.exp(-((t - center) ** 2) / (2 * 0.007 ** 2))
            local_t = max(0, t - (center - 0.01))
            freq = base + 4000 * local_t
            freq = min(freq, base + 500)
            pulse = 0.6 + 0.4 * math.sin(2 * math.pi * 30 * t)
            fundamental = math.sin(2 * math.pi * freq * t)
            octave = math.sin(2 * math.pi * freq * 2 * t) * 0.2
            total += env * vol * pulse * (fundamental + octave)
        return total * 0.5
    return _make_sound(22050, 0.13, fn)


def contact_major_chord() -> pygame.mixer.Sound:
    """Quick major chord — happy discovery ding."""
    def fn(t, progress):
        amplitude = math.exp(-progress * 7)
        # C-E-G major triad
        root = math.sin(2 * math.pi * 1047 * t)       # C6
        third = math.sin(2 * math.pi * 1319 * t) * 0.7  # E6
        fifth = math.sin(2 * math.pi * 1568 * t) * 0.5  # G6
        return amplitude * (root + third + fifth) * 0.45
    return _make_sound(22050, 0.15, fn)


def contact_rising_major() -> pygame.mixer.Sound:
    """Two quick notes rising a major third — bip-BING!"""
    def fn(t, progress):
        env1 = math.exp(-((t - 0.02) ** 2) / (2 * 0.008 ** 2))
        env2 = math.exp(-((t - 0.07) ** 2) / (2 * 0.012 ** 2))
        s1 = env1 * math.sin(2 * math.pi * 1047 * t)       # C6
        s2 = env2 * math.sin(2 * math.pi * 1319 * t) * 0.9  # E6
        # Add octave shimmer to second note
        s2 += env2 * math.sin(2 * math.pi * 2638 * t) * 0.2
        return (s1 + s2) * 0.7
    return _make_sound(22050, 0.14, fn)


def contact_arp_up() -> pygame.mixer.Sound:
    """Fast three-note upward arpeggio — C E G, cheerful ping."""
    def fn(t, progress):
        total = 0.0
        for center, freq in [(0.015, 1047), (0.04, 1319), (0.07, 1568)]:
            env = math.exp(-((t - center) ** 2) / (2 * 0.008 ** 2))
            fundamental = math.sin(2 * math.pi * freq * t)
            shimmer = math.sin(2 * math.pi * freq * 2 * t) * 0.15
            total += env * (fundamental + shimmer)
        return total * 0.55
    return _make_sound(22050, 0.12, fn)


def contact_bell_ping() -> pygame.mixer.Sound:
    """Bell-like ping with harmonics — clear bright ding."""
    def fn(t, progress):
        freq = 1400
        amplitude = math.exp(-progress * 5)
        # Bell harmonics: fundamental, 2x, 3x with different decays
        s1 = math.sin(2 * math.pi * freq * t)
        s2 = math.sin(2 * math.pi * freq * 2.0 * t) * 0.5 * math.exp(-progress * 7)
        s3 = math.sin(2 * math.pi * freq * 3.0 * t) * 0.25 * math.exp(-progress * 9)
        return amplitude * (s1 + s2 + s3) * 0.55
    return _make_sound(22050, 0.18, fn)


def contact_success_ding() -> pygame.mixer.Sound:
    """Classic two-tone success sound — low-high ding-DING."""
    def fn(t, progress):
        env1 = math.exp(-((t - 0.025) ** 2) / (2 * 0.01 ** 2))
        env2 = math.exp(-((t - 0.09) ** 2) / (2 * 0.015 ** 2))
        # Perfect fifth jump
        s1 = env1 * math.sin(2 * math.pi * 880 * t)   # A5
        s2 = env2 * math.sin(2 * math.pi * 1320 * t)  # E6
        s2 += env2 * math.sin(2 * math.pi * 2640 * t) * 0.2  # shimmer
        return (s1 + s2) * 0.7
    return _make_sound(22050, 0.16, fn)


def contact_sparkle_ping() -> pygame.mixer.Sound:
    """Bright sparkle — fast ascending harmonics that ring out."""
    def fn(t, progress):
        total = 0.0
        for i, (center, freq) in enumerate(
            [(0.01, 1200), (0.025, 1500), (0.04, 1900), (0.055, 2400)]
        ):
            env = math.exp(-((t - center) ** 2) / (2 * 0.005 ** 2))
            ring = math.exp(-max(0, t - center) * 8) * 0.3  # lingering ring
            total += (env + ring) * math.sin(2 * math.pi * freq * t) * (1.0 - i * 0.15)
        return total * 0.45
    return _make_sound(22050, 0.14, fn)


def contact_octave_ping() -> pygame.mixer.Sound:
    """Quick octave jump ping — low to high, clean and bright."""
    def fn(t, progress):
        env1 = math.exp(-((t - 0.02) ** 2) / (2 * 0.007 ** 2))
        env2 = math.exp(-((t - 0.065) ** 2) / (2 * 0.012 ** 2))
        s1 = env1 * math.sin(2 * math.pi * 800 * t)
        s2 = env2 * math.sin(2 * math.pi * 1600 * t)
        s2 += env2 * math.sin(2 * math.pi * 2400 * t) * 0.2  # fifth above octave
        return (s1 + s2) * 0.7
    return _make_sound(22050, 0.13, fn)


def contact_pulse_arp() -> pygame.mixer.Sound:
    """Rising arpeggio with subtle pulse — detected and tracking."""
    def fn(t, progress):
        total = 0.0
        for center, freq in [(0.015, 880), (0.04, 1100), (0.07, 1400)]:
            env = math.exp(-((t - center) ** 2) / (2 * 0.008 ** 2))
            pulse = 0.7 + 0.3 * math.sin(2 * math.pi * 25 * t)
            fundamental = math.sin(2 * math.pi * freq * t)
            octave = math.sin(2 * math.pi * freq * 2 * t) * 0.15
            total += env * pulse * (fundamental + octave)
        return total * 0.55
    return _make_sound(22050, 0.12, fn)


# --- Missile launch sounds ---

def missile_low_whoosh() -> pygame.mixer.Sound:
    """Low rising whoosh — heavy projectile launching."""
    import random
    rng = random.Random(77)
    noise = [rng.random() * 2 - 1 for _ in range(6000)]

    def fn(t, progress):
        freq = 80 + 200 * progress
        amplitude = math.exp(-((progress - 0.3) ** 2) / (2 * 0.25 ** 2))
        tone = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.3
        # Shaped noise for the whoosh texture
        idx = int(t * 22050) % len(noise)
        n = noise[idx] * 0.4 * amplitude
        return amplitude * (tone + octave) * 0.6 + n
    return _make_sound(22050, 0.35, fn)


def missile_charge_thrust() -> pygame.mixer.Sound:
    """Rising charge into a sustained low thrust — powering up and away."""
    import random
    rng = random.Random(88)
    noise = [rng.random() * 2 - 1 for _ in range(6000)]

    def fn(t, progress):
        if progress < 0.25:
            p = progress / 0.25
            freq = 60 + 100 * p * p
            amplitude = p * 0.6
        else:
            p = (progress - 0.25) / 0.75
            freq = 160 + 150 * p
            amplitude = math.exp(-p * 2)
        tone = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.25
        idx = int(t * 22050) % len(noise)
        n = noise[idx] * 0.3 * amplitude
        return amplitude * (tone + octave) * 0.6 + n
    return _make_sound(22050, 0.4, fn)


def missile_rumble_launch() -> pygame.mixer.Sound:
    """Deep rumble building into launch — heavy ordnance."""
    import random
    rng = random.Random(55)
    noise = [rng.random() * 2 - 1 for _ in range(6000)]

    def fn(t, progress):
        freq = 50 + 250 * progress * progress
        amplitude = progress * math.exp(-progress * 1.5) * 2.5
        tone = math.sin(2 * math.pi * freq * t)
        sub = math.sin(2 * math.pi * freq * 0.5 * t) * 0.4
        idx = int(t * 22050) % len(noise)
        n = noise[idx] * 0.35 * amplitude
        tremolo = 0.7 + 0.3 * math.sin(2 * math.pi * 20 * t)
        return amplitude * tremolo * (tone + sub) * 0.5 + n
    return _make_sound(22050, 0.4, fn)


def missile_swoosh_rise() -> pygame.mixer.Sound:
    """Fast rising swoosh — missile streaking away."""
    import random
    rng = random.Random(33)
    noise = [rng.random() * 2 - 1 for _ in range(6000)]

    def fn(t, progress):
        freq = 100 + 400 * progress
        amplitude = math.exp(-progress * 3)
        tone = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.2
        idx = int(t * 22050) % len(noise)
        n = noise[idx] * 0.5 * amplitude * (1 - progress)  # noise fades
        return amplitude * (tone + octave) * 0.5 + n
    return _make_sound(22050, 0.3, fn)


def missile_harmonic_thrust() -> pygame.mixer.Sound:
    """Rising harmonics with thrust rumble — sci-fi missile."""
    import random
    rng = random.Random(44)
    noise = [rng.random() * 2 - 1 for _ in range(6000)]

    def fn(t, progress):
        freq = 80 + 300 * progress
        amplitude = math.exp(-((progress - 0.35) ** 2) / (2 * 0.2 ** 2))
        fundamental = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.3
        fifth = math.sin(2 * math.pi * freq * 1.5 * t) * 0.2
        idx = int(t * 22050) % len(noise)
        n = noise[idx] * 0.3 * amplitude
        return amplitude * (fundamental + octave + fifth) * 0.5 + n
    return _make_sound(22050, 0.35, fn)


def missile_pulse_launch() -> pygame.mixer.Sound:
    """Pulsing low tone that rises — thruster ignition."""
    import random
    rng = random.Random(66)
    noise = [rng.random() * 2 - 1 for _ in range(6000)]

    def fn(t, progress):
        freq = 70 + 250 * progress
        amplitude = math.exp(-((progress - 0.3) ** 2) / (2 * 0.25 ** 2))
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 15 * t)
        tone = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.25
        idx = int(t * 22050) % len(noise)
        n = noise[idx] * 0.25 * amplitude
        return amplitude * pulse * (tone + octave) * 0.6 + n
    return _make_sound(22050, 0.35, fn)


def missile_dual_tone_thrust() -> pygame.mixer.Sound:
    """Two rising tones with noise — fat engine burn."""
    import random
    rng = random.Random(22)
    noise = [rng.random() * 2 - 1 for _ in range(6000)]

    def fn(t, progress):
        freq1 = 80 + 200 * progress
        freq2 = 120 + 300 * progress
        amplitude = math.exp(-((progress - 0.35) ** 2) / (2 * 0.22 ** 2))
        s1 = math.sin(2 * math.pi * freq1 * t)
        s2 = math.sin(2 * math.pi * freq2 * t) * 0.6
        octave = math.sin(2 * math.pi * freq2 * 2 * t) * 0.15
        idx = int(t * 22050) % len(noise)
        n = noise[idx] * 0.35 * amplitude
        return amplitude * (s1 + s2 + octave) * 0.45 + n
    return _make_sound(22050, 0.35, fn)


def missile_charge_whoosh() -> pygame.mixer.Sound:
    """Quick charge then whooshing away — launch sequence."""
    import random
    rng = random.Random(11)
    noise = [rng.random() * 2 - 1 for _ in range(6000)]

    def fn(t, progress):
        if progress < 0.2:
            p = progress / 0.2
            freq = 200 + 400 * p * p
            amplitude = p * 0.5
            idx = int(t * 22050) % len(noise)
            n = noise[idx] * 0.1 * amplitude
            return amplitude * math.sin(2 * math.pi * freq * t) * 0.7 + n
        else:
            p = (progress - 0.2) / 0.8
            freq = 100 + 300 * p
            amplitude = math.exp(-p * 2.5)
            tone = math.sin(2 * math.pi * freq * t)
            octave = math.sin(2 * math.pi * freq * 2 * t) * 0.25
            idx = int(t * 22050) % len(noise)
            n = noise[idx] * 0.45 * amplitude
            return amplitude * (tone + octave) * 0.5 + n
    return _make_sound(22050, 0.4, fn)


def missile_deep_rocket() -> pygame.mixer.Sound:
    """Deep sub-bass rocket ignition — ground-shaking launch."""
    import random
    rng = random.Random(101)
    noise = [rng.random() * 2 - 1 for _ in range(10000)]

    def fn(t, progress):
        # Sub-bass fundamental that slowly rises
        freq = 30 + 40 * progress
        amplitude = min(progress * 4, 1.0) * math.exp(-max(0, progress - 0.7) * 4)
        sub = math.sin(2 * math.pi * freq * t)
        sub2 = math.sin(2 * math.pi * freq * 2 * t) * 0.5
        # Heavy noise layer
        idx = int(t * 22050) % len(noise)
        n = noise[idx] * 0.6 * amplitude
        return amplitude * (sub + sub2) * 0.5 + n
    return _make_sound(22050, 0.6, fn)


def missile_ignition_roar() -> pygame.mixer.Sound:
    """Ignition click then roaring thrust — realistic rocket."""
    import random
    rng = random.Random(102)
    noise = [rng.random() * 2 - 1 for _ in range(10000)]

    def fn(t, progress):
        if progress < 0.08:
            # Ignition click/snap
            p = progress / 0.08
            amplitude = math.exp(-p * 3)
            return amplitude * math.sin(2 * math.pi * 400 * t) * 0.5
        else:
            p = (progress - 0.08) / 0.92
            freq = 25 + 50 * p
            # Slow ramp up to full power
            ramp = min(p * 3, 1.0)
            amplitude = ramp * math.exp(-max(0, p - 0.6) * 3)
            sub = math.sin(2 * math.pi * freq * t)
            sub2 = math.sin(2 * math.pi * freq * 1.5 * t) * 0.4
            sub3 = math.sin(2 * math.pi * freq * 3 * t) * 0.15
            idx = int(t * 22050) % len(noise)
            n = noise[idx] * 0.65 * amplitude
            tremolo = 0.8 + 0.2 * math.sin(2 * math.pi * 8 * t)
            return amplitude * tremolo * (sub + sub2 + sub3) * 0.45 + n
    return _make_sound(22050, 0.7, fn)


def missile_thunder_launch() -> pygame.mixer.Sound:
    """Thunderous low-end launch — massive bass with crackling."""
    import random
    rng = random.Random(103)
    noise = [rng.random() * 2 - 1 for _ in range(10000)]
    # Pre-generate crackle (sparse noise hits)
    crackle = [rng.random() for _ in range(10000)]

    def fn(t, progress):
        freq = 25 + 30 * progress
        ramp = min(progress * 5, 1.0)
        amplitude = ramp * math.exp(-max(0, progress - 0.6) * 3)
        sub = math.sin(2 * math.pi * freq * t)
        sub2 = math.sin(2 * math.pi * freq * 2 * t) * 0.5
        idx = int(t * 22050) % len(noise)
        n = noise[idx] * 0.55 * amplitude
        # Crackle layer — sparse pops
        c = crackle[idx]
        crack = (1.0 if c > 0.95 else 0.0) * amplitude * 0.4
        return amplitude * (sub + sub2) * 0.5 + n + crack
    return _make_sound(22050, 0.6, fn)


def missile_deep_pulse_rocket() -> pygame.mixer.Sound:
    """Pulsing sub-bass rocket — rhythmic deep thrust."""
    import random
    rng = random.Random(104)
    noise = [rng.random() * 2 - 1 for _ in range(10000)]

    def fn(t, progress):
        freq = 28 + 35 * progress
        ramp = min(progress * 4, 1.0)
        amplitude = ramp * math.exp(-max(0, progress - 0.65) * 3)
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 6 * t)
        sub = math.sin(2 * math.pi * freq * t)
        sub2 = math.sin(2 * math.pi * freq * 2 * t) * 0.45
        idx = int(t * 22050) % len(noise)
        n = noise[idx] * 0.5 * amplitude
        return amplitude * pulse * (sub + sub2) * 0.55 + n
    return _make_sound(22050, 0.6, fn)


def missile_booster_separation() -> pygame.mixer.Sound:
    """Two-stage: deep ignition then higher boost phase — staging rocket."""
    import random
    rng = random.Random(105)
    noise = [rng.random() * 2 - 1 for _ in range(10000)]

    def fn(t, progress):
        if progress < 0.45:
            p = progress / 0.45
            freq = 25 + 30 * p
            ramp = min(p * 3, 1.0)
            amplitude = ramp * 0.9
        else:
            p = (progress - 0.45) / 0.55
            freq = 55 + 80 * p
            amplitude = math.exp(-p * 2.5)
        sub = math.sin(2 * math.pi * freq * t)
        sub2 = math.sin(2 * math.pi * freq * 2 * t) * 0.4
        sub3 = math.sin(2 * math.pi * freq * 0.5 * t) * 0.3
        idx = int(t * 22050) % len(noise)
        n = noise[idx] * 0.6 * amplitude
        return amplitude * (sub + sub2 + sub3) * 0.4 + n
    return _make_sound(22050, 0.7, fn)


def missile_sustained_burn() -> pygame.mixer.Sound:
    """Long sustained deep burn — heavy engine at full power."""
    import random
    rng = random.Random(106)
    noise = [rng.random() * 2 - 1 for _ in range(10000)]

    def fn(t, progress):
        freq = 30 + 20 * progress
        # Fast attack, long sustain, gradual fade
        if progress < 0.1:
            amplitude = progress / 0.1
        else:
            amplitude = math.exp(-(progress - 0.1) * 1.5)
        sub = math.sin(2 * math.pi * freq * t)
        sub2 = math.sin(2 * math.pi * freq * 2 * t) * 0.5
        sub3 = math.sin(2 * math.pi * freq * 3 * t) * 0.2
        idx = int(t * 22050) % len(noise)
        n = noise[idx] * 0.7 * amplitude
        tremolo = 0.85 + 0.15 * math.sin(2 * math.pi * 5 * t)
        return amplitude * tremolo * (sub + sub2 + sub3) * 0.4 + n
    return _make_sound(22050, 0.7, fn)


def missile_shockwave_launch() -> pygame.mixer.Sound:
    """Initial shockwave pop then deep rumble — explosive launch."""
    import random
    rng = random.Random(107)
    noise = [rng.random() * 2 - 1 for _ in range(10000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.05:
            # Shockwave — loud burst
            p = progress / 0.05
            amplitude = math.exp(-p * 2)
            return amplitude * noise[idx] * 0.9
        else:
            p = (progress - 0.05) / 0.95
            freq = 25 + 45 * p
            ramp = min(p * 2.5, 1.0)
            amplitude = ramp * math.exp(-max(0, p - 0.5) * 3)
            sub = math.sin(2 * math.pi * freq * t)
            sub2 = math.sin(2 * math.pi * freq * 2 * t) * 0.45
            n = noise[idx] * 0.55 * amplitude
            return amplitude * (sub + sub2) * 0.5 + n
    return _make_sound(22050, 0.65, fn)


def missile_pressure_wave() -> pygame.mixer.Sound:
    """Building pressure then release — like a cannon firing a rocket."""
    import random
    rng = random.Random(108)
    noise = [rng.random() * 2 - 1 for _ in range(10000)]

    def fn(t, progress):
        if progress < 0.3:
            # Pressure building
            p = progress / 0.3
            freq = 20 + 15 * p
            amplitude = p * p * 0.7
            sub = math.sin(2 * math.pi * freq * t)
            idx = int(t * 22050) % len(noise)
            n = noise[idx] * 0.3 * amplitude
            return amplitude * sub * 0.6 + n
        else:
            # Release and thrust
            p = (progress - 0.3) / 0.7
            freq = 35 + 60 * p
            amplitude = math.exp(-p * 2)
            sub = math.sin(2 * math.pi * freq * t)
            sub2 = math.sin(2 * math.pi * freq * 2 * t) * 0.5
            sub3 = math.sin(2 * math.pi * freq * 3 * t) * 0.2
            idx = int(t * 22050) % len(noise)
            n = noise[idx] * 0.65 * amplitude
            return amplitude * (sub + sub2 + sub3) * 0.45 + n
    return _make_sound(22050, 0.65, fn)


# --- Missile explosion sounds ---

def explosion_deep_boom() -> pygame.mixer.Sound:
    """Deep bass boom with long rumble tail."""
    import random
    rng = random.Random(201)
    noise = [rng.random() * 2 - 1 for _ in range(12000)]

    def fn(t, progress):
        freq = 40 * math.exp(-progress * 3)  # pitch drops
        amplitude = math.exp(-progress * 2)
        sub = math.sin(2 * math.pi * freq * t)
        sub2 = math.sin(2 * math.pi * freq * 2 * t) * 0.4
        idx = int(t * 22050) % len(noise)
        n = noise[idx] * 0.7 * amplitude
        return amplitude * (sub + sub2) * 0.5 + n
    return _make_sound(22050, 0.7, fn)


def explosion_shockwave_boom() -> pygame.mixer.Sound:
    """Loud noise shockwave then deep rumbling decay."""
    import random
    rng = random.Random(202)
    noise = [rng.random() * 2 - 1 for _ in range(12000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.08:
            # Initial shockwave blast
            p = progress / 0.08
            amplitude = math.exp(-p * 1.5)
            return amplitude * noise[idx] * 0.95
        else:
            p = (progress - 0.08) / 0.92
            freq = 35 * math.exp(-p * 2)
            amplitude = math.exp(-p * 2)
            sub = math.sin(2 * math.pi * freq * t)
            sub2 = math.sin(2 * math.pi * freq * 2 * t) * 0.45
            n = noise[idx] * 0.6 * amplitude
            return amplitude * (sub + sub2) * 0.5 + n
    return _make_sound(22050, 0.8, fn)


def explosion_crackle_boom() -> pygame.mixer.Sound:
    """Explosion with crackling debris — messy detonation."""
    import random
    rng = random.Random(203)
    noise = [rng.random() * 2 - 1 for _ in range(12000)]
    crackle = [rng.random() for _ in range(12000)]

    def fn(t, progress):
        freq = 45 * math.exp(-progress * 2.5)
        amplitude = math.exp(-progress * 1.8)
        sub = math.sin(2 * math.pi * freq * t)
        sub2 = math.sin(2 * math.pi * freq * 2 * t) * 0.4
        idx = int(t * 22050) % len(noise)
        n = noise[idx] * 0.6 * amplitude
        c = (1.0 if crackle[idx] > 0.92 else 0.0) * amplitude * 0.5
        return amplitude * (sub + sub2) * 0.45 + n + c
    return _make_sound(22050, 0.8, fn)


def explosion_double_boom() -> pygame.mixer.Sound:
    """Two-stage explosion — initial blast then secondary detonation."""
    import random
    rng = random.Random(204)
    noise = [rng.random() * 2 - 1 for _ in range(12000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        # First blast
        env1 = math.exp(-((progress - 0.05) ** 2) / (2 * 0.03 ** 2))
        # Second blast
        env2 = math.exp(-((progress - 0.3) ** 2) / (2 * 0.06 ** 2)) * 0.8
        amplitude = env1 + env2
        # Rumble tail
        tail = math.exp(-max(0, progress - 0.3) * 2.5) * 0.4
        freq = 30 + 15 * (1 - progress)
        sub = math.sin(2 * math.pi * freq * t)
        sub2 = math.sin(2 * math.pi * freq * 2 * t) * 0.4
        n = noise[idx] * 0.65 * (amplitude + tail)
        return (amplitude + tail) * (sub + sub2) * 0.4 + n
    return _make_sound(22050, 0.8, fn)


def explosion_rumble_fade() -> pygame.mixer.Sound:
    """Sustained low rumble that slowly fades — lingering explosion."""
    import random
    rng = random.Random(205)
    noise = [rng.random() * 2 - 1 for _ in range(12000)]

    def fn(t, progress):
        freq = 30 + 10 * math.sin(2 * math.pi * 2 * t)  # wobbling pitch
        if progress < 0.05:
            amplitude = progress / 0.05
        else:
            amplitude = math.exp(-(progress - 0.05) * 1.5)
        sub = math.sin(2 * math.pi * freq * t)
        sub2 = math.sin(2 * math.pi * freq * 2 * t) * 0.5
        sub3 = math.sin(2 * math.pi * freq * 3 * t) * 0.2
        idx = int(t * 22050) % len(noise)
        n = noise[idx] * 0.65 * amplitude
        tremolo = 0.8 + 0.2 * math.sin(2 * math.pi * 4 * t)
        return amplitude * tremolo * (sub + sub2 + sub3) * 0.4 + n
    return _make_sound(22050, 0.9, fn)


def explosion_punch_boom() -> pygame.mixer.Sound:
    """Hard initial punch then fast decay — tight explosion."""
    import random
    rng = random.Random(206)
    noise = [rng.random() * 2 - 1 for _ in range(12000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.03:
            return noise[idx] * 0.9
        p = (progress - 0.03) / 0.97
        freq = 50 * math.exp(-p * 4)
        amplitude = math.exp(-p * 3)
        sub = math.sin(2 * math.pi * freq * t)
        sub2 = math.sin(2 * math.pi * freq * 2 * t) * 0.5
        n = noise[idx] * 0.55 * amplitude
        return amplitude * (sub + sub2) * 0.5 + n
    return _make_sound(22050, 0.5, fn)


def explosion_pulse_rumble() -> pygame.mixer.Sound:
    """Pulsing deep rumble — rhythmic explosion aftershock."""
    import random
    rng = random.Random(207)
    noise = [rng.random() * 2 - 1 for _ in range(12000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.05:
            return noise[idx] * 0.85 * (progress / 0.05)
        p = (progress - 0.05) / 0.95
        freq = 35 * math.exp(-p * 2)
        amplitude = math.exp(-p * 1.8)
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 5 * t)
        sub = math.sin(2 * math.pi * freq * t)
        sub2 = math.sin(2 * math.pi * freq * 2 * t) * 0.45
        n = noise[idx] * 0.6 * amplitude
        return amplitude * pulse * (sub + sub2) * 0.5 + n
    return _make_sound(22050, 0.8, fn)


def explosion_massive_blast() -> pygame.mixer.Sound:
    """Massive blast — shockwave, sub-bass, and long noisy tail."""
    import random
    rng = random.Random(208)
    noise = [rng.random() * 2 - 1 for _ in range(15000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.06:
            p = progress / 0.06
            return noise[idx] * 0.95 * math.exp(-p * 0.5)
        p = (progress - 0.06) / 0.94
        freq = 25 + 20 * math.exp(-p * 3)
        amplitude = math.exp(-p * 1.5)
        sub = math.sin(2 * math.pi * freq * t)
        sub2 = math.sin(2 * math.pi * freq * 2 * t) * 0.5
        sub3 = math.sin(2 * math.pi * freq * 0.5 * t) * 0.3
        n = noise[idx] * 0.7 * amplitude
        tremolo = 0.85 + 0.15 * math.sin(2 * math.pi * 3 * t)
        return amplitude * tremolo * (sub + sub2 + sub3) * 0.35 + n
    return _make_sound(22050, 1.0, fn)


# --- Ship destruction sounds (small explosion + pilot scream) ---

def _scream_formant(t, freq, vibrato_hz=6, vibrato_depth=30):
    """Generate a scream-like tone with vibrato and formant harmonics."""
    vib = vibrato_depth * math.sin(2 * math.pi * vibrato_hz * t)
    f = freq + vib
    # Vowel-like formants: fundamental + nasally harmonics
    s1 = math.sin(2 * math.pi * f * t)
    s2 = math.sin(2 * math.pi * f * 2.3 * t) * 0.4   # odd harmonic for nasal
    s3 = math.sin(2 * math.pi * f * 3.1 * t) * 0.2
    s4 = math.sin(2 * math.pi * f * 4.7 * t) * 0.1
    return (s1 + s2 + s3 + s4) * 0.5


def destroy_scream_falling() -> pygame.mixer.Sound:
    """Small boom then falling-pitch scream — classic death cry."""
    import random
    rng = random.Random(301)
    noise = [rng.random() * 2 - 1 for _ in range(8000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        # Small explosion at start
        if progress < 0.1:
            p = progress / 0.1
            boom = math.exp(-p * 3) * 0.8
            return boom * (math.sin(2 * math.pi * 50 * t) + noise[idx] * 0.7)
        # Scream: high pitch falling
        p = (progress - 0.1) / 0.9
        freq = 900 - 400 * p
        amplitude = math.exp(-p * 2)
        scream = _scream_formant(t, freq, vibrato_hz=7, vibrato_depth=40)
        n = noise[idx] * 0.15 * amplitude
        return amplitude * scream + n
    return _make_sound(22050, 0.8, fn)


def destroy_scream_rising() -> pygame.mixer.Sound:
    """Boom then rising panicked scream that cuts off."""
    import random
    rng = random.Random(302)
    noise = [rng.random() * 2 - 1 for _ in range(8000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.08:
            p = progress / 0.08
            boom = math.exp(-p * 3) * 0.8
            return boom * (math.sin(2 * math.pi * 55 * t) + noise[idx] * 0.6)
        p = (progress - 0.08) / 0.92
        freq = 600 + 500 * p
        # Cuts off suddenly near end
        if p > 0.8:
            amplitude = (1.0 - p) / 0.2
        else:
            amplitude = math.exp(-p * 1.5)
        scream = _scream_formant(t, freq, vibrato_hz=8, vibrato_depth=50)
        n = noise[idx] * 0.1 * amplitude
        return amplitude * scream + n
    return _make_sound(22050, 0.7, fn)


def destroy_scream_warble() -> pygame.mixer.Sound:
    """Boom then wobbling scream — frantic vibrato."""
    import random
    rng = random.Random(303)
    noise = [rng.random() * 2 - 1 for _ in range(8000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.1:
            p = progress / 0.1
            boom = math.exp(-p * 3) * 0.7
            return boom * (math.sin(2 * math.pi * 45 * t) + noise[idx] * 0.65)
        p = (progress - 0.1) / 0.9
        freq = 800 - 200 * p
        amplitude = math.exp(-p * 2)
        scream = _scream_formant(t, freq, vibrato_hz=12, vibrato_depth=80)
        n = noise[idx] * 0.12 * amplitude
        return amplitude * scream + n
    return _make_sound(22050, 0.75, fn)


def destroy_scream_doppler() -> pygame.mixer.Sound:
    """Boom then scream with doppler-like pitch drop — flying past."""
    import random
    rng = random.Random(304)
    noise = [rng.random() * 2 - 1 for _ in range(8000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.08:
            p = progress / 0.08
            boom = math.exp(-p * 3) * 0.8
            return boom * (math.sin(2 * math.pi * 50 * t) + noise[idx] * 0.7)
        p = (progress - 0.08) / 0.92
        # Fast doppler drop
        freq = 1000 * math.exp(-p * 2)
        freq = max(freq, 200)
        amplitude = math.exp(-p * 2.5)
        scream = _scream_formant(t, freq, vibrato_hz=6, vibrato_depth=35)
        n = noise[idx] * 0.12 * amplitude
        return amplitude * scream + n
    return _make_sound(22050, 0.7, fn)


def destroy_scream_stutter() -> pygame.mixer.Sound:
    """Boom then stuttering broken scream — radio breaking up."""
    import random
    rng = random.Random(305)
    noise = [rng.random() * 2 - 1 for _ in range(8000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.1:
            p = progress / 0.1
            boom = math.exp(-p * 3) * 0.75
            return boom * (math.sin(2 * math.pi * 48 * t) + noise[idx] * 0.65)
        p = (progress - 0.1) / 0.9
        freq = 850 - 300 * p
        amplitude = math.exp(-p * 2)
        # Stuttering on/off
        stutter = 1.0 if math.sin(2 * math.pi * 15 * t) > -0.2 else 0.1
        scream = _scream_formant(t, freq, vibrato_hz=7, vibrato_depth=45)
        n = noise[idx] * 0.1 * amplitude
        return amplitude * stutter * scream + n
    return _make_sound(22050, 0.8, fn)


def destroy_scream_echo() -> pygame.mixer.Sound:
    """Boom then scream that fades with echo-like repeats."""
    import random
    rng = random.Random(306)
    noise = [rng.random() * 2 - 1 for _ in range(8000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.08:
            p = progress / 0.08
            boom = math.exp(-p * 3) * 0.8
            return boom * (math.sin(2 * math.pi * 52 * t) + noise[idx] * 0.6)
        p = (progress - 0.08) / 0.92
        freq = 800 - 250 * p
        # Main scream + delayed quieter "echoes"
        env1 = math.exp(-p * 2.5)
        env2 = math.exp(-max(0, p - 0.3) * 3) * 0.4
        env3 = math.exp(-max(0, p - 0.55) * 4) * 0.2
        amplitude = env1 + env2 + env3
        scream = _scream_formant(t, freq, vibrato_hz=7, vibrato_depth=35)
        n = noise[idx] * 0.1 * amplitude
        return amplitude * scream + n
    return _make_sound(22050, 0.9, fn)


def destroy_boom_scream_fade() -> pygame.mixer.Sound:
    """Bigger boom blended with scream that slowly dies out."""
    import random
    rng = random.Random(307)
    noise = [rng.random() * 2 - 1 for _ in range(10000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        # Explosion layer — persists longer
        boom_env = math.exp(-progress * 3)
        boom_freq = 40 * math.exp(-progress * 2)
        boom = boom_env * (math.sin(2 * math.pi * boom_freq * t) * 0.4 + noise[idx] * 0.5)
        # Scream layer — fades in slightly then out
        if progress < 0.05:
            scream_env = progress / 0.05 * 0.7
        else:
            scream_env = 0.7 * math.exp(-(progress - 0.05) * 2)
        freq = 750 - 200 * progress
        scream = scream_env * _scream_formant(t, freq, vibrato_hz=8, vibrato_depth=45)
        return boom + scream
    return _make_sound(22050, 0.85, fn)


def destroy_scream_v2_sustained() -> pygame.mixer.Sound:
    """Boom then long sustained 'aaaah' scream — 3 seconds, slow fade."""
    import random
    rng = random.Random(321)
    noise = [rng.random() * 2 - 1 for _ in range(70000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.03:
            p = progress / 0.03
            boom = math.exp(-p * 3) * 0.8
            return boom * (math.sin(2 * math.pi * 45 * t) + noise[idx] * 0.7)
        p = (progress - 0.03) / 0.97
        freq = 320 + 15 * math.sin(2 * math.pi * 4.5 * t)
        amplitude = math.exp(-p * 0.8)
        formants = _AH_FORMANTS
        scream = _voice(t, freq, formants, breathiness=0.25, noise_val=noise[idx])
        return amplitude * scream
    return _make_sound(22050, 3.0, fn)


def destroy_scream_v2_falling() -> pygame.mixer.Sound:
    """Boom then 'aaaah' slowly falling in pitch over 3 seconds."""
    import random
    rng = random.Random(322)
    noise = [rng.random() * 2 - 1 for _ in range(70000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.03:
            p = progress / 0.03
            boom = math.exp(-p * 3) * 0.8
            return boom * (math.sin(2 * math.pi * 45 * t) + noise[idx] * 0.7)
        p = (progress - 0.03) / 0.97
        base = 350 - 150 * p
        freq = base + 12 * math.sin(2 * math.pi * 5 * t)
        amplitude = math.exp(-p * 0.7)
        formants = _lerp_formants(_AH_FORMANTS, _OH_FORMANTS, p)
        scream = _voice(t, freq, formants, breathiness=0.2 + 0.2 * p, noise_val=noise[idx])
        return amplitude * scream
    return _make_sound(22050, 3.0, fn)


def destroy_scream_v2_rising_cut() -> pygame.mixer.Sound:
    """Boom then rising panicked scream that abruptly cuts off at 2.5s."""
    import random
    rng = random.Random(323)
    noise = [rng.random() * 2 - 1 for _ in range(70000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.03:
            p = progress / 0.03
            boom = math.exp(-p * 3) * 0.8
            return boom * (math.sin(2 * math.pi * 45 * t) + noise[idx] * 0.7)
        p = (progress - 0.03) / 0.97
        base = 250 + 200 * p
        freq = base + 18 * math.sin(2 * math.pi * 6 * t)
        if p > 0.83:
            amplitude = max(0, (1.0 - p) / 0.17) ** 3
        else:
            amplitude = 0.9
        formants = _lerp_formants(_AH_FORMANTS, _EH_FORMANTS, p * 0.5)
        scream = _voice(t, freq, formants, breathiness=0.15 + 0.15 * p, noise_val=noise[idx])
        return amplitude * scream
    return _make_sound(22050, 3.0, fn)


def destroy_scream_v2_breathy() -> pygame.mixer.Sound:
    """Boom then breathy gasping scream — lots of air, 3 seconds."""
    import random
    rng = random.Random(324)
    noise = [rng.random() * 2 - 1 for _ in range(70000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.03:
            p = progress / 0.03
            boom = math.exp(-p * 3) * 0.8
            return boom * (math.sin(2 * math.pi * 45 * t) + noise[idx] * 0.7)
        p = (progress - 0.03) / 0.97
        freq = 300 - 80 * p + 20 * math.sin(2 * math.pi * 4 * t)
        amplitude = math.exp(-p * 0.7)
        formants = _AH_FORMANTS
        scream = _voice(t, freq, formants, breathiness=0.5 + 0.2 * p, noise_val=noise[idx])
        return amplitude * scream
    return _make_sound(22050, 3.0, fn)


def destroy_scream_v2_boom_blend() -> pygame.mixer.Sound:
    """Sustained boom rumble blended with long scream throughout."""
    import random
    rng = random.Random(325)
    noise = [rng.random() * 2 - 1 for _ in range(70000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        boom_env = math.exp(-progress * 1.5)
        boom_freq = 35 * math.exp(-progress * 1.5)
        boom = boom_env * (math.sin(2 * math.pi * boom_freq * t) * 0.3
                           + math.sin(2 * math.pi * boom_freq * 2 * t) * 0.15
                           + noise[idx] * 0.4)
        if progress < 0.05:
            scream_env = progress / 0.05
        else:
            scream_env = math.exp(-(progress - 0.05) * 0.6)
        freq = 300 - 80 * progress + 15 * math.sin(2 * math.pi * 5 * t)
        formants = _lerp_formants(_AH_FORMANTS, _OH_FORMANTS, progress * 0.6)
        scream = scream_env * _voice(t, freq, formants, breathiness=0.25, noise_val=noise[idx])
        return boom + scream
    return _make_sound(22050, 3.0, fn)


def destroy_scream_v2_vibrato() -> pygame.mixer.Sound:
    """Boom then agonized scream with deepening vibrato — 3 seconds."""
    import random
    rng = random.Random(326)
    noise = [rng.random() * 2 - 1 for _ in range(70000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.03:
            p = progress / 0.03
            boom = math.exp(-p * 3) * 0.8
            return boom * (math.sin(2 * math.pi * 45 * t) + noise[idx] * 0.7)
        p = (progress - 0.03) / 0.97
        vib_depth = 20 + 40 * p
        vib_rate = 5 + 2 * p
        freq = 310 - 60 * p + vib_depth * math.sin(2 * math.pi * vib_rate * t)
        amplitude = math.exp(-p * 0.7)
        formants = _AH_FORMANTS
        scream = _voice(t, freq, formants, breathiness=0.2 + 0.1 * p, noise_val=noise[idx])
        return amplitude * scream
    return _make_sound(22050, 3.0, fn)


def destroy_scream_v2_radio_die() -> pygame.mixer.Sound:
    """Boom then scream over radio that breaks up and dies — 3 seconds."""
    import random
    rng = random.Random(327)
    noise = [rng.random() * 2 - 1 for _ in range(70000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.03:
            p = progress / 0.03
            boom = math.exp(-p * 3) * 0.8
            return boom * (math.sin(2 * math.pi * 45 * t) + noise[idx] * 0.7)
        p = (progress - 0.03) / 0.97
        freq = 300 - 80 * p + 15 * math.sin(2 * math.pi * 5 * t)
        amplitude = math.exp(-p * 0.6)
        formants = _AH_FORMANTS
        scream = _voice(t, freq, formants, breathiness=0.2, noise_val=noise[idx])
        dropout_rate = 3 + 8 * p
        threshold = -0.5 + 1.3 * p
        on = 1.0 if math.sin(2 * math.pi * dropout_rate * t) > threshold else 0.0
        static = noise[idx] * 0.2 * amplitude * (1 - on)
        return amplitude * on * scream + static
    return _make_sound(22050, 3.0, fn)


def destroy_scream_v2_doppler() -> pygame.mixer.Sound:
    """Boom then long doppler scream — pitch drops like falling into space."""
    import random
    rng = random.Random(328)
    noise = [rng.random() * 2 - 1 for _ in range(70000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.03:
            p = progress / 0.03
            boom = math.exp(-p * 3) * 0.8
            return boom * (math.sin(2 * math.pi * 45 * t) + noise[idx] * 0.7)
        p = (progress - 0.03) / 0.97
        freq = 400 * math.exp(-p * 1.2) + 10 * math.sin(2 * math.pi * 4 * t)
        freq = max(freq, 80)
        amplitude = math.exp(-p * 0.8)
        shift = p * 0.7
        formants = _lerp_formants(_AH_FORMANTS, _OH_FORMANTS, shift)
        scream = _voice(t, freq, formants, breathiness=0.2 + 0.3 * p, noise_val=noise[idx])
        return amplitude * scream
    return _make_sound(22050, 3.0, fn)


# --- Shield hit sounds ---

def shield_crackle_deflect() -> pygame.mixer.Sound:
    """Electric crackle with a deflection tone — energy shield absorb."""
    import random
    rng = random.Random(401)
    noise = [rng.random() * 2 - 1 for _ in range(6000)]
    crackle = [rng.random() for _ in range(6000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.05:
            return noise[idx] * 0.8 * math.exp(-progress / 0.05 * 2)
        p = (progress - 0.05) / 0.95
        freq = 600 + 200 * math.exp(-p * 3)
        amplitude = math.exp(-p * 4)
        tone = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.3
        c = (1.0 if crackle[idx] > 0.88 else 0.0) * amplitude * 0.4
        return amplitude * (tone + octave) * 0.5 + c
    return _make_sound(22050, 0.3, fn)


def shield_buzz_absorb() -> pygame.mixer.Sound:
    """Buzzing energy absorption — shield soaking up damage."""
    import random
    rng = random.Random(402)
    noise = [rng.random() * 2 - 1 for _ in range(6000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.03:
            return noise[idx] * 0.7
        p = (progress - 0.03) / 0.97
        freq = 300 + 100 * math.sin(2 * math.pi * 20 * t)
        amplitude = math.exp(-p * 3)
        tone = math.sin(2 * math.pi * freq * t)
        octave = math.sin(2 * math.pi * freq * 2 * t) * 0.4
        n = noise[idx] * 0.2 * amplitude
        return amplitude * (tone + octave) * 0.5 + n
    return _make_sound(22050, 0.3, fn)


def shield_shimmer_hit() -> pygame.mixer.Sound:
    """High shimmer with descending harmonics — glancing shield hit."""
    def fn(t, progress):
        if progress < 0.02:
            p = progress / 0.02
            return math.sin(2 * math.pi * 2000 * t) * 0.6 * math.exp(-p * 2)
        p = (progress - 0.02) / 0.98
        freq = 1500 - 800 * p
        amplitude = math.exp(-p * 3.5)
        s1 = math.sin(2 * math.pi * freq * t)
        s2 = math.sin(2 * math.pi * freq * 1.5 * t) * 0.3
        s3 = math.sin(2 * math.pi * freq * 2 * t) * 0.2
        return amplitude * (s1 + s2 + s3) * 0.5
    return _make_sound(22050, 0.3, fn)


def shield_thump_ring() -> pygame.mixer.Sound:
    """Low thump into a ringing shield — heavy impact absorbed."""
    import random
    rng = random.Random(404)
    noise = [rng.random() * 2 - 1 for _ in range(6000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        thump = math.exp(-progress * 15) * math.sin(2 * math.pi * 80 * t) * 0.6
        thump += math.exp(-progress * 15) * noise[idx] * 0.3
        if progress > 0.03:
            p = (progress - 0.03) / 0.97
            freq = 800
            ring = math.exp(-p * 4) * math.sin(2 * math.pi * freq * t) * 0.5
            ring += math.exp(-p * 5) * math.sin(2 * math.pi * freq * 2 * t) * 0.15
        else:
            ring = 0
        return thump + ring
    return _make_sound(22050, 0.35, fn)


def shield_electric_zap() -> pygame.mixer.Sound:
    """Sharp electric zap — quick discharge on impact."""
    import random
    rng = random.Random(405)
    noise = [rng.random() * 2 - 1 for _ in range(6000)]
    crackle = [rng.random() for _ in range(6000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        freq = 500 + 1000 * math.exp(-progress * 8)
        amplitude = math.exp(-progress * 5)
        tone = math.sin(2 * math.pi * freq * t)
        c = (1.0 if crackle[idx] > 0.85 else 0.0) * amplitude * 0.5
        n = noise[idx] * 0.25 * amplitude
        return amplitude * tone * 0.5 + c + n
    return _make_sound(22050, 0.25, fn)


def shield_pulse_absorb() -> pygame.mixer.Sound:
    """Pulsing energy absorb — shield rippling from impact."""
    def fn(t, progress):
        freq = 700 - 300 * progress
        amplitude = math.exp(-progress * 3)
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 25 * t)
        s1 = math.sin(2 * math.pi * freq * t)
        s2 = math.sin(2 * math.pi * freq * 2 * t) * 0.25
        return amplitude * pulse * (s1 + s2) * 0.6
    return _make_sound(22050, 0.3, fn)


def shield_harmonic_deflect() -> pygame.mixer.Sound:
    """Rich harmonic deflection ring — musical shield bounce."""
    def fn(t, progress):
        if progress < 0.02:
            return math.sin(2 * math.pi * 1200 * t) * 0.7
        p = (progress - 0.02) / 0.98
        freq = 900 - 300 * p
        amplitude = math.exp(-p * 3)
        s1 = math.sin(2 * math.pi * freq * t)
        s2 = math.sin(2 * math.pi * freq * 1.5 * t) * 0.4
        s3 = math.sin(2 * math.pi * freq * 2 * t) * 0.25
        s4 = math.sin(2 * math.pi * freq * 3 * t) * 0.1
        return amplitude * (s1 + s2 + s3 + s4) * 0.4
    return _make_sound(22050, 0.35, fn)


def shield_impact_sizzle() -> pygame.mixer.Sound:
    """Hard impact then sizzling energy dissipation."""
    import random
    rng = random.Random(408)
    noise = [rng.random() * 2 - 1 for _ in range(6000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        impact = math.exp(-progress * 12) * 0.7
        impact_sound = impact * (math.sin(2 * math.pi * 150 * t) + noise[idx] * 0.5)
        if progress > 0.03:
            p = (progress - 0.03) / 0.97
            sizzle_amp = math.exp(-p * 3)
            mod = math.sin(2 * math.pi * 800 * t)
            sizzle = sizzle_amp * noise[idx] * 0.4 * (0.5 + 0.5 * mod)
        else:
            sizzle = 0
        return impact_sound + sizzle
    return _make_sound(22050, 0.35, fn)


def shield_heavy_thump_sizzle() -> pygame.mixer.Sound:
    """Heavy thump with sizzling tail — big hit absorbed."""
    import random
    rng = random.Random(411)
    noise = [rng.random() * 2 - 1 for _ in range(6000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        thump = math.exp(-progress * 12) * 0.8
        thump_sound = thump * (math.sin(2 * math.pi * 60 * t) + noise[idx] * 0.5)
        if progress > 0.04:
            p = (progress - 0.04) / 0.96
            sizzle_amp = math.exp(-p * 2.5)
            mod = math.sin(2 * math.pi * 600 * t)
            sizzle = sizzle_amp * noise[idx] * 0.35 * (0.5 + 0.5 * mod)
            pulse = 0.6 + 0.4 * math.sin(2 * math.pi * 15 * t)
            sizzle *= pulse
        else:
            sizzle = 0
        return thump_sound + sizzle
    return _make_sound(22050, 0.4, fn)


def shield_double_thump() -> pygame.mixer.Sound:
    """Two quick thumps — impact then shield pushback."""
    import random
    rng = random.Random(412)
    noise = [rng.random() * 2 - 1 for _ in range(6000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        env1 = math.exp(-((progress - 0.03) ** 2) / (2 * 0.015 ** 2))
        env2 = math.exp(-((progress - 0.12) ** 2) / (2 * 0.02 ** 2)) * 0.6
        thump1 = env1 * (math.sin(2 * math.pi * 70 * t) + noise[idx] * 0.4)
        thump2 = env2 * (math.sin(2 * math.pi * 100 * t) + noise[idx] * 0.3)
        # Tail sizzle
        if progress > 0.1:
            p = (progress - 0.1) / 0.9
            sizzle = math.exp(-p * 3) * noise[idx] * 0.2
        else:
            sizzle = 0
        return thump1 + thump2 + sizzle
    return _make_sound(22050, 0.35, fn)


def shield_pulse_thump() -> pygame.mixer.Sound:
    """Thump into pulsing resonance — shield vibrating from hit."""
    import random
    rng = random.Random(413)
    noise = [rng.random() * 2 - 1 for _ in range(6000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        thump = math.exp(-progress * 14) * 0.7
        thump_sound = thump * (math.sin(2 * math.pi * 75 * t) + noise[idx] * 0.45)
        if progress > 0.03:
            p = (progress - 0.03) / 0.97
            amplitude = math.exp(-p * 3)
            pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 18 * t)
            freq = 500 - 200 * p
            ring = math.sin(2 * math.pi * freq * t)
            octave = math.sin(2 * math.pi * freq * 2 * t) * 0.2
            return thump_sound + amplitude * pulse * (ring + octave) * 0.35
        return thump_sound
    return _make_sound(22050, 0.35, fn)


def shield_impact_ripple() -> pygame.mixer.Sound:
    """Hard impact then rippling pulse wave — energy dispersing."""
    import random
    rng = random.Random(414)
    noise = [rng.random() * 2 - 1 for _ in range(6000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        impact = math.exp(-progress * 15) * 0.8
        impact_sound = impact * (math.sin(2 * math.pi * 90 * t) + noise[idx] * 0.5)
        if progress > 0.03:
            p = (progress - 0.03) / 0.97
            amplitude = math.exp(-p * 2.5)
            # Ripple: pulsing that slows down
            ripple_rate = 30 * math.exp(-p * 2)
            pulse = 0.5 + 0.5 * math.sin(2 * math.pi * ripple_rate * t)
            freq = 600 - 250 * p
            tone = math.sin(2 * math.pi * freq * t) * 0.3
            sizzle = noise[idx] * 0.25
            return impact_sound + amplitude * pulse * (tone + sizzle)
        return impact_sound
    return _make_sound(22050, 0.4, fn)


def shield_thump_fade_sizzle() -> pygame.mixer.Sound:
    """Big thump then long sizzling fade — lingering shield discharge."""
    import random
    rng = random.Random(415)
    noise = [rng.random() * 2 - 1 for _ in range(8000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        thump = math.exp(-progress * 10) * 0.8
        thump_sound = thump * (math.sin(2 * math.pi * 55 * t)
                               + math.sin(2 * math.pi * 110 * t) * 0.3
                               + noise[idx] * 0.5)
        if progress > 0.05:
            p = (progress - 0.05) / 0.95
            sizzle_amp = math.exp(-p * 1.8)
            mod = math.sin(2 * math.pi * 500 * t)
            sizzle = sizzle_amp * noise[idx] * 0.3 * (0.5 + 0.5 * mod)
        else:
            sizzle = 0
        return thump_sound + sizzle
    return _make_sound(22050, 0.5, fn)


def shield_punch_pulse_sizzle() -> pygame.mixer.Sound:
    """Punchy hit into pulsing sizzle — forceful absorption."""
    import random
    rng = random.Random(416)
    noise = [rng.random() * 2 - 1 for _ in range(6000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        # Punch
        if progress < 0.03:
            return noise[idx] * 0.75 + math.sin(2 * math.pi * 80 * t) * 0.5
        p = (progress - 0.03) / 0.97
        amplitude = math.exp(-p * 2.5)
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 20 * t)
        mod = math.sin(2 * math.pi * 700 * t)
        sizzle = noise[idx] * 0.35 * (0.5 + 0.5 * mod)
        freq = 400 - 150 * p
        tone = math.sin(2 * math.pi * freq * t) * 0.25
        return amplitude * pulse * (sizzle + tone)
    return _make_sound(22050, 0.4, fn)


# ── Shield recharge sounds ──────────────────────────────────────────────

def shield_recharge_rising_chime() -> pygame.mixer.Sound:
    """Rising three-note chime — classic power-up feel."""
    def fn(t, progress):
        if progress < 0.33:
            freq = 600
            p = progress / 0.33
        elif progress < 0.66:
            freq = 800
            p = (progress - 0.33) / 0.33
        else:
            freq = 1000
            p = (progress - 0.66) / 0.34
        amplitude = math.sin(p * math.pi)
        tone = math.sin(2 * math.pi * freq * t)
        harmonic = math.sin(2 * math.pi * freq * 2 * t) * 0.3
        return amplitude * (tone + harmonic) * 0.6
    return _make_sound(22050, 0.6, fn)


def shield_recharge_hum_swell() -> pygame.mixer.Sound:
    """Low hum that swells up and rings out — shield powering on."""
    def fn(t, progress):
        freq = 150 + 250 * progress
        if progress < 0.6:
            amplitude = progress / 0.6
        else:
            amplitude = 1.0 - (progress - 0.6) / 0.4
        tone = math.sin(2 * math.pi * freq * t)
        h2 = math.sin(2 * math.pi * freq * 2 * t) * 0.4
        h3 = math.sin(2 * math.pi * freq * 3 * t) * 0.2
        return amplitude * (tone + h2 + h3) * 0.5
    return _make_sound(22050, 0.8, fn)


def shield_recharge_shimmer() -> pygame.mixer.Sound:
    """Shimmering tone with beating harmonics — energy field activating."""
    def fn(t, progress):
        freq = 500 + 300 * progress
        amplitude = math.sin(progress * math.pi) * 0.7
        t1 = math.sin(2 * math.pi * freq * t)
        t2 = math.sin(2 * math.pi * (freq + 8) * t)
        t3 = math.sin(2 * math.pi * (freq * 1.5) * t) * 0.3
        return amplitude * (t1 + t2 + t3) / 2.3
    return _make_sound(22050, 0.7, fn)


def shield_recharge_pulse_rise() -> pygame.mixer.Sound:
    """Pulsing tone that rises in pitch — charging up effect."""
    def fn(t, progress):
        freq = 300 + 500 * progress
        pulse_rate = 8 + 12 * progress
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * pulse_rate * t)
        envelope = math.sin(progress * math.pi)
        tone = math.sin(2 * math.pi * freq * t)
        h = math.sin(2 * math.pi * freq * 2.5 * t) * 0.3
        return envelope * pulse * (tone + h) * 0.6
    return _make_sound(22050, 0.7, fn)


def shield_recharge_bright_ping() -> pygame.mixer.Sound:
    """Quick bright ping with a resonant tail — shield online notification."""
    def fn(t, progress):
        freq = 1200
        amplitude = math.exp(-progress * 5)
        tone = math.sin(2 * math.pi * freq * t)
        h = math.sin(2 * math.pi * freq * 1.5 * t) * 0.4
        sub = math.sin(2 * math.pi * 400 * t) * 0.3 * math.exp(-progress * 3)
        return amplitude * (tone + h + sub) * 0.6
    return _make_sound(22050, 0.5, fn)


def shield_recharge_sweep_chime() -> pygame.mixer.Sound:
    """Upward sweep into a chime hit — energy building then locking in."""
    def fn(t, progress):
        if progress < 0.5:
            p = progress / 0.5
            freq = 200 + 800 * p * p
            amplitude = 0.3 + 0.7 * p
            tone = math.sin(2 * math.pi * freq * t)
            h = math.sin(2 * math.pi * freq * 2 * t) * 0.2 * p
            return amplitude * (tone + h) * 0.5
        else:
            p = (progress - 0.5) / 0.5
            freq = 1000
            amplitude = math.exp(-p * 4)
            tone = math.sin(2 * math.pi * freq * t)
            h2 = math.sin(2 * math.pi * freq * 2 * t) * 0.3
            h3 = math.sin(2 * math.pi * freq * 3 * t) * 0.15
            return amplitude * (tone + h2 + h3) * 0.6
    return _make_sound(22050, 0.7, fn)


def shield_recharge_warm_glow() -> pygame.mixer.Sound:
    """Warm rising tone with gentle harmonics — comforting recharge."""
    def fn(t, progress):
        freq = 350 + 350 * progress
        envelope = math.sin(progress * math.pi) ** 0.7
        tone = math.sin(2 * math.pi * freq * t)
        h2 = math.sin(2 * math.pi * freq * 2 * t) * 0.5
        h3 = math.sin(2 * math.pi * freq * 3 * t) * 0.25
        h4 = math.sin(2 * math.pi * freq * 4 * t) * 0.1
        return envelope * (tone + h2 + h3 + h4) / 1.85 * 0.6
    return _make_sound(22050, 0.8, fn)


def shield_recharge_double_ping() -> pygame.mixer.Sound:
    """Two quick ascending pings — confirmation beep."""
    def fn(t, progress):
        if progress < 0.45:
            p = progress / 0.45
            freq = 800
            amplitude = math.exp(-p * 6)
        elif progress < 0.55:
            return 0.0
        else:
            p = (progress - 0.55) / 0.45
            freq = 1100
            amplitude = math.exp(-p * 5)
        tone = math.sin(2 * math.pi * freq * t)
        h = math.sin(2 * math.pi * freq * 1.5 * t) * 0.3
        return amplitude * (tone + h) * 0.6
    return _make_sound(22050, 0.5, fn)


# ── Ship destruction sounds ─────────────────────────────────────────────

def destroy_big_boom() -> pygame.mixer.Sound:
    """Massive low boom with long rumbling tail — ship goes up."""
    import random
    rng = random.Random(500)
    noise = [rng.random() * 2 - 1 for _ in range(88200)]
    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        # Initial blast
        if progress < 0.1:
            p = progress / 0.1
            blast = noise[idx] * (1.0 - p) * 0.8
            freq = 40 + 20 * (1 - p)
            boom = math.sin(2 * math.pi * freq * t) * (1.0 - p * 0.5)
            return blast + boom
        # Rumble decay
        p = (progress - 0.1) / 0.9
        amplitude = math.exp(-p * 1.8)
        freq = 35 - 15 * p
        boom = math.sin(2 * math.pi * freq * t)
        rumble = noise[idx] * 0.3
        throb = 0.7 + 0.3 * math.sin(2 * math.pi * 2 * t)
        return amplitude * throb * (boom * 0.7 + rumble * 0.3)
    return _make_sound(22050, 4.0, fn)


def destroy_cascading_explosion() -> pygame.mixer.Sound:
    """Multiple explosions in sequence — chain reaction destruction."""
    import random
    rng = random.Random(501)
    noise = [rng.random() * 2 - 1 for _ in range(88200)]
    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        result = 0.0
        # Four blasts at 0.0, 0.2, 0.4, 0.6
        for offset in (0.0, 0.2, 0.4, 0.6):
            if progress >= offset:
                p = (progress - offset)
                amp = math.exp(-p * 2.0) * 0.7
                freq = 50 - 20 * min(p, 1.0)
                result += amp * (math.sin(2 * math.pi * freq * t) * 0.6 + noise[idx] * 0.4)
        # Fade-out rumble
        if progress > 0.7:
            tail = (progress - 0.7) / 0.3
            result *= (1.0 - tail * 0.7)
        return max(-1.0, min(1.0, result))
    return _make_sound(22050, 4.0, fn)


def destroy_deep_shockwave() -> pygame.mixer.Sound:
    """Deep sub-bass shockwave with debris crackle."""
    import random
    rng = random.Random(502)
    noise = [rng.random() * 2 - 1 for _ in range(88200)]
    crackle = [1.0 if rng.random() > 0.95 else 0.0 for _ in range(88200)]
    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        # Sub-bass shockwave
        if progress < 0.15:
            p = progress / 0.15
            freq = 30
            amp = math.sin(p * math.pi)
            wave = math.sin(2 * math.pi * freq * t) * amp
        else:
            p = (progress - 0.15) / 0.85
            freq = 30 - 10 * p
            amp = math.exp(-p * 1.5)
            wave = math.sin(2 * math.pi * freq * t) * amp * 0.8
        # Crackle/debris
        crack_amp = 0.0
        if progress > 0.1:
            crack_p = (progress - 0.1) / 0.9
            crack_amp = math.exp(-crack_p * 2) * 0.4
        crack = crackle[idx] * noise[idx] * crack_amp
        return wave + crack
    return _make_sound(22050, 4.0, fn)


def destroy_rumble_crescendo() -> pygame.mixer.Sound:
    """Builds from rumble to massive explosion peak then long fade."""
    import random
    rng = random.Random(503)
    noise = [rng.random() * 2 - 1 for _ in range(88200)]
    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.3:
            # Build-up rumble
            p = progress / 0.3
            amp = p * p * 0.5
            freq = 40 + 30 * p
            tone = math.sin(2 * math.pi * freq * t) * 0.6
            rumble = noise[idx] * 0.4
            return amp * (tone + rumble)
        elif progress < 0.4:
            # Peak blast
            p = (progress - 0.3) / 0.1
            amp = 1.0
            freq = 50
            tone = math.sin(2 * math.pi * freq * t) * 0.5
            blast = noise[idx] * 0.5
            return amp * (tone + blast)
        else:
            # Long decay with rumble and crackle
            p = (progress - 0.4) / 0.6
            amp = math.exp(-p * 2.0)
            freq = 35 - 15 * p
            tone = math.sin(2 * math.pi * freq * t) * 0.5
            rumble = noise[idx] * 0.3
            # Secondary rumble throb
            throb = 0.6 + 0.4 * math.sin(2 * math.pi * 3 * t)
            return amp * throb * (tone + rumble)
    return _make_sound(22050, 4.0, fn)


def destroy_hollow_boom() -> pygame.mixer.Sound:
    """Hollow metallic boom — like a hull breaching."""
    import random
    rng = random.Random(504)
    noise = [rng.random() * 2 - 1 for _ in range(88200)]
    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.08:
            p = progress / 0.08
            amp = p
        else:
            p = (progress - 0.08) / 0.92
            amp = math.exp(-p * 1.5)
        freq = 80 - 30 * min(progress, 1.0)
        tone = math.sin(2 * math.pi * freq * t)
        # Metallic ring
        ring = math.sin(2 * math.pi * 220 * t) * math.exp(-progress * 3) * 0.3
        ring2 = math.sin(2 * math.pi * 340 * t) * math.exp(-progress * 3.5) * 0.2
        # Debris rumble
        rumble = noise[idx] * 0.15 * amp
        return amp * tone * 0.6 + ring + ring2 + rumble
    return _make_sound(22050, 4.0, fn)


def destroy_fire_crackle() -> pygame.mixer.Sound:
    """Explosion with extended fire/crackle aftermath."""
    import random
    rng = random.Random(505)
    noise = [rng.random() * 2 - 1 for _ in range(88200)]
    crackle_timing = [rng.random() for _ in range(88200)]
    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        result = 0.0
        # Initial boom
        if progress < 0.12:
            p = progress / 0.12
            boom_amp = math.sin(p * math.pi) if p < 0.5 else math.exp(-(p - 0.5) * 4)
            freq = 45
            result += boom_amp * (math.sin(2 * math.pi * freq * t) * 0.6 + noise[idx] * 0.4)
        # Fire crackle tail
        if progress > 0.08:
            p = (progress - 0.08) / 0.92
            fire_amp = math.exp(-p * 1.0) * 0.5
            crackle = noise[idx] * (0.3 + 0.7 * (crackle_timing[idx] > 0.7))
            # Filtered rumble
            freq = 100 + 50 * math.sin(2 * math.pi * 3 * t)
            rumble = math.sin(2 * math.pi * freq * t) * 0.3
            result += fire_amp * (crackle * 0.6 + rumble * 0.4)
        return max(-1.0, min(1.0, result))
    return _make_sound(22050, 4.0, fn)


def destroy_double_blast() -> pygame.mixer.Sound:
    """Two heavy blasts — hull breach then reactor explosion, long tail."""
    import random
    rng = random.Random(506)
    noise = [rng.random() * 2 - 1 for _ in range(88200)]
    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        result = 0.0
        # First blast (0.0 - 0.25)
        if progress < 0.25:
            p = progress / 0.25
            amp = math.exp(-p * 3) * 0.8
            freq = 50
            result += amp * (math.sin(2 * math.pi * freq * t) * 0.6 + noise[idx] * 0.4)
        # Second bigger blast (0.3 - 0.7)
        if progress > 0.3:
            p = (progress - 0.3) / 0.7
            amp = math.exp(-p * 1.8)
            freq = 35 - 10 * p
            result += amp * (math.sin(2 * math.pi * freq * t) * 0.5 + noise[idx] * 0.5)
            # Rumble undertone
            throb = 0.6 + 0.4 * math.sin(2 * math.pi * 2.5 * t)
            result *= throb
        return max(-1.0, min(1.0, result))
    return _make_sound(22050, 4.0, fn)


def destroy_massive_rupture() -> pygame.mixer.Sound:
    """Enormous low-end rupture with shaking sub-bass."""
    import random
    rng = random.Random(507)
    noise = [rng.random() * 2 - 1 for _ in range(88200)]
    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        # Sub-bass throb
        throb_rate = 4 - 2 * progress
        throb = 0.5 + 0.5 * math.sin(2 * math.pi * throb_rate * t)
        if progress < 0.1:
            amp = progress / 0.1
        else:
            p = (progress - 0.1) / 0.9
            amp = math.exp(-p * 1.5)
        freq = 30 + 10 * math.sin(2 * math.pi * 0.5 * t)
        bass = math.sin(2 * math.pi * freq * t)
        rumble = noise[idx] * 0.35
        return amp * throb * (bass * 0.65 + rumble) * 0.9
    return _make_sound(22050, 4.0, fn)


# Keep old functions for backwards compat but they're unused in tester now
def destroy_scream_crackle() -> pygame.mixer.Sound:
    """Boom with crackle then distorted scream — comms static."""
    import random
    rng = random.Random(308)
    noise = [rng.random() * 2 - 1 for _ in range(8000)]
    crackle = [rng.random() for _ in range(8000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.1:
            p = progress / 0.1
            boom = math.exp(-p * 3) * 0.75
            c = (1.0 if crackle[idx] > 0.9 else 0.0) * 0.3
            return boom * (math.sin(2 * math.pi * 45 * t) + noise[idx] * 0.6) + c
        p = (progress - 0.1) / 0.9
        freq = 800 - 300 * p
        amplitude = math.exp(-p * 2)
        scream = _scream_formant(t, freq, vibrato_hz=7, vibrato_depth=40)
        # Crackle/static over the scream
        c = (1.0 if crackle[idx] > 0.93 else 0.0) * amplitude * 0.25
        n = noise[idx] * 0.15 * amplitude
        return amplitude * scream + n + c
    return _make_sound(22050, 0.8, fn)


def _voice(t, base_freq, formants, breathiness=0.2, noise_val=0.0):
    """Synthesize voice: glottal pulse shaped by formant resonances.

    formants: list of (freq, amplitude, bandwidth) tuples
    """
    # Rich glottal pulse — sawtooth approximation (30 harmonics)
    phase = base_freq * t
    glottal = 0.0
    for n in range(1, 30):
        harm_freq = base_freq * n
        # Weight each harmonic by proximity to formant peaks (bandpass sim)
        weight = 0.0
        for f_freq, f_amp, f_bw in formants:
            # Gaussian-like resonance around each formant
            dist = (harm_freq - f_freq) / f_bw
            weight += f_amp * math.exp(-0.5 * dist * dist)
        glottal += math.sin(2 * math.pi * n * phase) * weight / (n ** 0.5)

    # Mix in breathiness (noise shaped by formants)
    breath = noise_val * breathiness

    return (glottal * 0.15 + breath) * 0.8


# "ah" formants: (freq, amplitude, bandwidth)
_AH_FORMANTS = [(730, 1.0, 120), (1090, 0.7, 130), (2440, 0.3, 180)]
# "eh" formants — mouth closing
_EH_FORMANTS = [(530, 1.0, 100), (1840, 0.5, 150), (2480, 0.3, 200)]
# "oh" formants — rounder
_OH_FORMANTS = [(570, 1.0, 100), (840, 0.6, 110), (2410, 0.2, 170)]


def _lerp_formants(f1, f2, mix):
    """Interpolate between two formant sets."""
    return [
        (a[0] + (b[0] - a[0]) * mix, a[1] + (b[1] - a[1]) * mix, a[2] + (b[2] - a[2]) * mix)
        for a, b in zip(f1, f2)
    ]


def destroy_long_aah() -> pygame.mixer.Sound:
    """Small boom then long 'aaaah' scream trailing off."""
    import random
    rng = random.Random(311)
    noise = [rng.random() * 2 - 1 for _ in range(10000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.06:
            p = progress / 0.06
            boom = math.exp(-p * 3) * 0.7
            return boom * (math.sin(2 * math.pi * 50 * t) + noise[idx] * 0.6)
        p = (progress - 0.06) / 0.94
        freq = 220 + 30 * math.sin(2 * math.pi * 5 * t)  # slow vibrato
        amplitude = math.exp(-p * 1.2)
        scream = _vowel_ah(t, freq)
        return amplitude * scream
    return _make_sound(22050, 1.2, fn)


def destroy_aah_falling() -> pygame.mixer.Sound:
    """Boom then 'aaaah' that drops in pitch — dying away."""
    import random
    rng = random.Random(312)
    noise = [rng.random() * 2 - 1 for _ in range(10000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.06:
            p = progress / 0.06
            boom = math.exp(-p * 3) * 0.7
            return boom * (math.sin(2 * math.pi * 50 * t) + noise[idx] * 0.6)
        p = (progress - 0.06) / 0.94
        base = 280 - 100 * p  # pitch slowly drops
        freq = base + 25 * math.sin(2 * math.pi * 5 * t)
        amplitude = math.exp(-p * 1.0)
        scream = _vowel_ah(t, freq)
        return amplitude * scream
    return _make_sound(22050, 1.4, fn)


def destroy_aah_rising_cut() -> pygame.mixer.Sound:
    """Boom then rising 'aaaah' that gets cut off — panicked death."""
    import random
    rng = random.Random(313)
    noise = [rng.random() * 2 - 1 for _ in range(10000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.05:
            p = progress / 0.05
            boom = math.exp(-p * 3) * 0.7
            return boom * (math.sin(2 * math.pi * 50 * t) + noise[idx] * 0.6)
        p = (progress - 0.05) / 0.95
        base = 200 + 150 * p  # pitch rises
        freq = base + 20 * math.sin(2 * math.pi * 6 * t)
        # Sustain then sudden cut
        if p < 0.75:
            amplitude = math.exp(-p * 0.5)
        else:
            amplitude = math.exp(-p * 0.5) * (1.0 - p) / 0.25
        scream = _vowel_ah(t, freq)
        return amplitude * scream
    return _make_sound(22050, 1.2, fn)


def destroy_aah_vibrato() -> pygame.mixer.Sound:
    """Boom then 'aaaah' with heavy vibrato — agonized scream."""
    import random
    rng = random.Random(314)
    noise = [rng.random() * 2 - 1 for _ in range(10000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.06:
            p = progress / 0.06
            boom = math.exp(-p * 3) * 0.7
            return boom * (math.sin(2 * math.pi * 50 * t) + noise[idx] * 0.6)
        p = (progress - 0.06) / 0.94
        vib_depth = 40 + 30 * p  # vibrato intensifies
        freq = 250 + vib_depth * math.sin(2 * math.pi * 7 * t)
        amplitude = math.exp(-p * 1.2)
        scream = _vowel_ah(t, freq)
        return amplitude * scream
    return _make_sound(22050, 1.3, fn)


def destroy_aah_breathy() -> pygame.mixer.Sound:
    """Boom then breathy 'aaaah' with noise layer — gasping scream."""
    import random
    rng = random.Random(315)
    noise = [rng.random() * 2 - 1 for _ in range(10000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.06:
            p = progress / 0.06
            boom = math.exp(-p * 3) * 0.7
            return boom * (math.sin(2 * math.pi * 50 * t) + noise[idx] * 0.6)
        p = (progress - 0.06) / 0.94
        freq = 240 - 60 * p + 20 * math.sin(2 * math.pi * 5 * t)
        amplitude = math.exp(-p * 1.1)
        scream = _vowel_ah(t, freq)
        breath = noise[idx] * 0.25 * amplitude  # breathy layer
        return amplitude * scream + breath
    return _make_sound(22050, 1.3, fn)


def destroy_aah_doppler_long() -> pygame.mixer.Sound:
    """Boom then long scream with slow doppler drop — falling away."""
    import random
    rng = random.Random(316)
    noise = [rng.random() * 2 - 1 for _ in range(10000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.05:
            p = progress / 0.05
            boom = math.exp(-p * 3) * 0.7
            return boom * (math.sin(2 * math.pi * 50 * t) + noise[idx] * 0.6)
        p = (progress - 0.05) / 0.95
        # Slow exponential pitch drop
        freq = 300 * math.exp(-p * 0.8) + 15 * math.sin(2 * math.pi * 5 * t)
        amplitude = math.exp(-p * 1.0)
        scream = _vowel_ah(t, freq)
        return amplitude * scream
    return _make_sound(22050, 1.5, fn)


def destroy_aah_stutter_radio() -> pygame.mixer.Sound:
    """Boom then 'aaaah' breaking up like a dying radio transmission."""
    import random
    rng = random.Random(317)
    noise = [rng.random() * 2 - 1 for _ in range(10000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        if progress < 0.06:
            p = progress / 0.06
            boom = math.exp(-p * 3) * 0.7
            return boom * (math.sin(2 * math.pi * 50 * t) + noise[idx] * 0.6)
        p = (progress - 0.06) / 0.94
        freq = 250 - 70 * p + 20 * math.sin(2 * math.pi * 5 * t)
        amplitude = math.exp(-p * 1.2)
        scream = _vowel_ah(t, freq)
        # Increasing dropouts as it goes
        dropout_rate = 5 + 12 * p
        stutter = 1.0 if math.sin(2 * math.pi * dropout_rate * t) > (-0.3 + 0.8 * p) else 0.05
        static = noise[idx] * 0.15 * amplitude * (1 - stutter)
        return amplitude * stutter * scream + static
    return _make_sound(22050, 1.3, fn)


def destroy_aah_boom_blend() -> pygame.mixer.Sound:
    """Extended boom and 'aaaah' blended together throughout."""
    import random
    rng = random.Random(318)
    noise = [rng.random() * 2 - 1 for _ in range(10000)]

    def fn(t, progress):
        idx = int(t * 22050) % len(noise)
        # Boom layer — fast attack, long decay
        boom_env = math.exp(-progress * 2.5)
        boom_freq = 40 * math.exp(-progress * 2)
        boom = boom_env * (math.sin(2 * math.pi * boom_freq * t) * 0.3 + noise[idx] * 0.4)
        # Scream layer — fades in then out
        if progress < 0.08:
            scream_env = progress / 0.08
        else:
            scream_env = math.exp(-(progress - 0.08) * 1.2)
        freq = 260 - 80 * progress + 25 * math.sin(2 * math.pi * 5 * t)
        scream = scream_env * _vowel_ah(t, freq)
        return boom + scream
    return _make_sound(22050, 1.3, fn)


# ---------------------------------------------------------------------------
# Music: Intro (title screen) and Game Loop variations
# ---------------------------------------------------------------------------

def _make_music_sound(sample_rate: int, duration: float, sample_fn, volume=0.35):
    """Build a music Sound — same as _make_sound but with default lower volume."""
    num_samples = int(sample_rate * duration)
    samples = array.array("h")
    for i in range(num_samples):
        t = i / sample_rate
        progress = t / duration
        value = sample_fn(t, progress)
        sample = int(max(-1.0, min(1.0, value)) * 32767 * volume)
        samples.append(sample)
    return pygame.mixer.Sound(buffer=samples)


def _pad_chord(t, freqs, detune=0.5):
    """Sum of sine waves for a pad chord, with slight detune for richness."""
    val = 0.0
    for f in freqs:
        val += math.sin(2 * math.pi * f * t)
        val += 0.3 * math.sin(2 * math.pi * (f + detune) * t)
    return val / (len(freqs) * 1.3)


def _chord_envelope(progress, chord_start, chord_end, attack=0.15, release=0.15):
    """Smooth envelope for a chord within a progression: fade in, sustain, fade out."""
    if progress < chord_start or progress > chord_end:
        return 0.0
    chord_progress = (progress - chord_start) / (chord_end - chord_start)
    if chord_progress < attack:
        return chord_progress / attack
    if chord_progress > 1.0 - release:
        return (1.0 - chord_progress) / release
    return 1.0


# --- Minor key chord sets (frequencies in Hz) ---
# Am:  A2=110, C3=130.81, E3=164.81
# Dm:  D3=146.83, F3=174.61, A3=220
# Em:  E3=164.81, G3=196, B3=246.94
# F:   F3=174.61, A3=220, C4=261.63
# G:   G3=196, B3=246.94, D4=293.66

_CHORD_Am = [110.0, 130.81, 164.81, 220.0]
_CHORD_Dm = [146.83, 174.61, 220.0, 293.66]
_CHORD_Em = [164.81, 196.0, 246.94, 329.63]
_CHORD_F  = [174.61, 220.0, 261.63, 349.23]
_CHORD_G  = [196.0, 246.94, 293.66, 392.0]
_CHORD_Cm = [130.81, 155.56, 196.0, 261.63]
_CHORD_Gm = [196.0, 233.08, 293.66, 392.0]
_CHORD_Bb = [233.08, 293.66, 349.23, 466.16]


def music_intro_dark_pads() -> pygame.mixer.Sound:
    """Slow Am -> Dm -> Em -> Am progression with lush pads. ~16 seconds."""
    duration = 16.0
    chords = [
        (0.0, 0.25, _CHORD_Am),
        (0.25, 0.5, _CHORD_Dm),
        (0.5, 0.75, _CHORD_Em),
        (0.75, 1.0, _CHORD_Am),
    ]

    def fn(t, progress):
        val = 0.0
        for start, end, freqs in chords:
            env = _chord_envelope(progress, start, end, attack=0.2, release=0.2)
            if env > 0:
                val += env * _pad_chord(t, freqs)
        # Sub bass follows root
        sub_freq = 55.0 if progress < 0.5 else 73.42
        val += 0.3 * math.sin(2 * math.pi * sub_freq * t)
        # Slow LFO tremolo
        val *= 0.8 + 0.2 * math.sin(2 * math.pi * 0.25 * t)
        return val * 0.7
    return _make_music_sound(22050, duration, fn)


def music_intro_space_drift() -> pygame.mixer.Sound:
    """Ethereal Am -> F -> Dm -> Em with high shimmer layer. ~18 seconds."""
    duration = 18.0
    chords = [
        (0.0, 0.25, _CHORD_Am),
        (0.25, 0.5, _CHORD_F),
        (0.5, 0.75, _CHORD_Dm),
        (0.75, 1.0, _CHORD_Em),
    ]

    def fn(t, progress):
        val = 0.0
        for start, end, freqs in chords:
            env = _chord_envelope(progress, start, end, attack=0.25, release=0.25)
            if env > 0:
                val += env * _pad_chord(t, freqs, detune=0.8)
        # Shimmer: high octave sine with slow vibrato
        shimmer_freq = 880.0 + 40 * math.sin(2 * math.pi * 0.3 * t)
        val += 0.12 * math.sin(2 * math.pi * shimmer_freq * t) * (0.5 + 0.5 * math.sin(2 * math.pi * 0.15 * t))
        # Sub bass drone
        val += 0.25 * math.sin(2 * math.pi * 55.0 * t)
        # Overall gentle swell
        val *= 0.7 + 0.3 * math.sin(2 * math.pi * (1.0 / duration) * t)
        return val * 0.65
    return _make_music_sound(22050, duration, fn)


def music_intro_deep_space() -> pygame.mixer.Sound:
    """Very low and dark: Am -> Em with deep sub bass and sparse high pings. ~15 seconds."""
    duration = 15.0
    chords = [
        (0.0, 0.5, _CHORD_Am),
        (0.5, 1.0, _CHORD_Em),
    ]

    def fn(t, progress):
        val = 0.0
        for start, end, freqs in chords:
            env = _chord_envelope(progress, start, end, attack=0.3, release=0.3)
            if env > 0:
                # Lower octave pads
                low_freqs = [f * 0.5 for f in freqs]
                val += env * _pad_chord(t, low_freqs, detune=1.0)
        # Deep sub bass with slow pulse
        sub_env = 0.6 + 0.4 * math.sin(2 * math.pi * 0.2 * t)
        val += 0.4 * sub_env * math.sin(2 * math.pi * 36.7 * t)
        # Sparse high ping every ~3.75 seconds
        ping_phase = (t % 3.75) / 3.75
        if ping_phase < 0.05:
            ping_env = math.exp(-ping_phase * 60)
            val += 0.2 * ping_env * math.sin(2 * math.pi * 1318.5 * t)
        return val * 0.7
    return _make_music_sound(22050, duration, fn)


def music_intro_nebula() -> pygame.mixer.Sound:
    """Cm -> Gm -> Bb -> Cm with breathy texture. ~16 seconds."""
    duration = 16.0
    chords = [
        (0.0, 0.25, _CHORD_Cm),
        (0.25, 0.5, _CHORD_Gm),
        (0.5, 0.75, _CHORD_Bb),
        (0.75, 1.0, _CHORD_Cm),
    ]

    def fn(t, progress):
        val = 0.0
        for start, end, freqs in chords:
            env = _chord_envelope(progress, start, end, attack=0.2, release=0.2)
            if env > 0:
                val += env * _pad_chord(t, freqs, detune=0.6)
        # Breathy noise texture (very quiet)
        import random
        noise_rng = random.Random(int(t * 22050) % 100000)
        noise = noise_rng.random() * 2 - 1
        val += 0.04 * noise * (0.5 + 0.5 * math.sin(2 * math.pi * 0.1 * t))
        # Sub drone
        val += 0.3 * math.sin(2 * math.pi * 65.41 * t)
        val *= 0.75 + 0.25 * math.sin(2 * math.pi * 0.2 * t)
        return val * 0.65
    return _make_music_sound(22050, duration, fn)


def music_intro_arpeggio() -> pygame.mixer.Sound:
    """Am pad with slow descending arpeggio motif. ~16 seconds."""
    duration = 16.0
    arp_notes = [440.0, 329.63, 261.63, 220.0]  # A4, E4, C4, A3
    arp_period = 4.0  # one full arp cycle in seconds

    def fn(t, progress):
        # Pad foundation
        val = 0.5 * _pad_chord(t, _CHORD_Am, detune=0.5)
        # Slow arpeggio
        arp_pos = (t % arp_period) / arp_period
        note_idx = int(arp_pos * len(arp_notes))
        note_freq = arp_notes[min(note_idx, len(arp_notes) - 1)]
        note_phase = (arp_pos * len(arp_notes)) % 1.0
        # Each note has its own envelope
        if note_phase < 0.1:
            note_env = note_phase / 0.1
        elif note_phase > 0.7:
            note_env = (1.0 - note_phase) / 0.3
        else:
            note_env = 1.0
        val += 0.3 * note_env * math.sin(2 * math.pi * note_freq * t)
        # Sub
        val += 0.2 * math.sin(2 * math.pi * 55.0 * t)
        # Global swell
        val *= 0.7 + 0.3 * math.sin(2 * math.pi * 0.15 * t)
        return val * 0.7
    return _make_music_sound(22050, duration, fn)


# --- Game loop music ---

def music_loop_combat_pulse() -> pygame.mixer.Sound:
    """Driving Am -> Em -> Dm -> Am with rhythmic pulse. ~32 seconds."""
    duration = 32.0
    chords = [
        (0.0, 0.25, _CHORD_Am),
        (0.25, 0.5, _CHORD_Em),
        (0.5, 0.75, _CHORD_Dm),
        (0.75, 1.0, _CHORD_Am),
    ]
    pulse_rate = 3.0  # Hz — rhythmic throb

    def fn(t, progress):
        val = 0.0
        for start, end, freqs in chords:
            env = _chord_envelope(progress, start, end, attack=0.1, release=0.1)
            if env > 0:
                val += env * _pad_chord(t, freqs, detune=0.3)
        # Rhythmic pulse
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * pulse_rate * t)
        val *= 0.6 + 0.4 * pulse
        # Bass pulse on beat
        bass_freq = 55.0 if progress < 0.25 or progress >= 0.75 else 73.42
        val += 0.35 * pulse * math.sin(2 * math.pi * bass_freq * t)
        # High tension tone
        val += 0.08 * math.sin(2 * math.pi * 660 * t) * pulse
        return val * 0.7
    return _make_music_sound(22050, duration, fn)


def music_loop_tension_drive() -> pygame.mixer.Sound:
    """Em -> Am -> F -> G with steady eighth-note pulse bass. ~30 seconds."""
    duration = 30.0
    chords = [
        (0.0, 0.25, _CHORD_Em),
        (0.25, 0.5, _CHORD_Am),
        (0.5, 0.75, _CHORD_F),
        (0.75, 1.0, _CHORD_G),
    ]
    beat_rate = 2.5  # Hz

    def fn(t, progress):
        val = 0.0
        for start, end, freqs in chords:
            env = _chord_envelope(progress, start, end, attack=0.12, release=0.12)
            if env > 0:
                val += env * _pad_chord(t, freqs, detune=0.4)
        # Eighth note bass pulse
        beat_phase = (t * beat_rate) % 1.0
        beat_env = math.exp(-beat_phase * 8)
        bass_freq = 82.41 if progress < 0.5 else 98.0
        val += 0.4 * beat_env * math.sin(2 * math.pi * bass_freq * t)
        # Tension high string
        val += 0.06 * math.sin(2 * math.pi * 880 * t) * (0.5 + 0.5 * math.sin(2 * math.pi * 0.5 * t))
        return val * 0.7
    return _make_music_sound(22050, duration, fn)


def music_loop_dark_march() -> pygame.mixer.Sound:
    """Am -> Dm -> Em -> Am with militaristic beat emphasis. ~32 seconds."""
    duration = 32.0
    chords = [
        (0.0, 0.25, _CHORD_Am),
        (0.25, 0.5, _CHORD_Dm),
        (0.5, 0.75, _CHORD_Em),
        (0.75, 1.0, _CHORD_Am),
    ]
    march_rate = 2.0  # Hz — march tempo

    def fn(t, progress):
        val = 0.0
        for start, end, freqs in chords:
            env = _chord_envelope(progress, start, end, attack=0.08, release=0.15)
            if env > 0:
                val += env * _pad_chord(t, freqs, detune=0.3)
        # March beat: sharp attack
        beat_phase = (t * march_rate) % 1.0
        if beat_phase < 0.15:
            beat_env = 1.0 - beat_phase / 0.15
        else:
            beat_env = 0.0
        val += 0.35 * beat_env * math.sin(2 * math.pi * 55.0 * t)
        # Off-beat accent (quieter)
        off_phase = ((t * march_rate) + 0.5) % 1.0
        if off_phase < 0.1:
            off_env = 1.0 - off_phase / 0.1
            val += 0.15 * off_env * math.sin(2 * math.pi * 110.0 * t)
        # Ominous high tone
        val += 0.05 * math.sin(2 * math.pi * 739.99 * t) * (0.5 + 0.5 * math.sin(2 * math.pi * 0.3 * t))
        return val * 0.7
    return _make_music_sound(22050, duration, fn)


def music_loop_space_chase() -> pygame.mixer.Sound:
    """Fast-paced Am -> G -> F -> Em with rapid arpeggiated bass. ~28 seconds."""
    duration = 28.0
    chords = [
        (0.0, 0.25, _CHORD_Am),
        (0.25, 0.5, _CHORD_G),
        (0.5, 0.75, _CHORD_F),
        (0.75, 1.0, _CHORD_Em),
    ]
    arp_notes_map = {
        0: [110.0, 164.81, 220.0, 164.81],  # Am bass arp
        1: [98.0, 146.83, 196.0, 146.83],    # G bass arp
        2: [87.31, 130.81, 174.61, 130.81],  # F bass arp
        3: [82.41, 123.47, 164.81, 123.47],  # Em bass arp
    }
    arp_speed = 4.0  # notes per second

    def fn(t, progress):
        val = 0.0
        chord_idx = 0
        for i, (start, end, freqs) in enumerate(chords):
            env = _chord_envelope(progress, start, end, attack=0.1, release=0.1)
            if env > 0:
                val += env * _pad_chord(t, freqs, detune=0.5)
                chord_idx = i
        # Fast arpeggio bass
        arp_notes = arp_notes_map[chord_idx]
        arp_pos = (t * arp_speed) % len(arp_notes)
        note_idx = int(arp_pos)
        note_phase = arp_pos - note_idx
        note_env = math.exp(-note_phase * 4)
        val += 0.3 * note_env * math.sin(2 * math.pi * arp_notes[note_idx] * t)
        # Urgency high tone
        val += 0.07 * math.sin(2 * math.pi * 1046.5 * t) * (0.4 + 0.6 * abs(math.sin(2 * math.pi * 2.0 * t)))
        return val * 0.7
    return _make_music_sound(22050, duration, fn)


def music_loop_void_pulse() -> pygame.mixer.Sound:
    """Minimal and dark: Cm -> Gm with deep throb and sparse texture. ~30 seconds."""
    duration = 30.0
    chords = [
        (0.0, 0.5, _CHORD_Cm),
        (0.5, 1.0, _CHORD_Gm),
    ]
    throb_rate = 1.5  # Hz

    def fn(t, progress):
        val = 0.0
        for start, end, freqs in chords:
            env = _chord_envelope(progress, start, end, attack=0.2, release=0.2)
            if env > 0:
                low_freqs = [f * 0.5 for f in freqs]
                val += env * _pad_chord(t, low_freqs, detune=0.8)
        # Deep throb
        throb = 0.5 + 0.5 * math.sin(2 * math.pi * throb_rate * t)
        val *= 0.5 + 0.5 * throb
        val += 0.4 * throb * math.sin(2 * math.pi * 41.2 * t)
        # Sparse ping
        ping_phase = (t % 5.0) / 5.0
        if ping_phase < 0.03:
            val += 0.15 * math.exp(-ping_phase * 100) * math.sin(2 * math.pi * 1567.98 * t)
        return val * 0.75
    return _make_music_sound(22050, duration, fn)


# Backwards compat alias
generate_laser_fire = laser_sine_sweep
