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


# Backwards compat alias
generate_laser_fire = laser_sine_sweep
