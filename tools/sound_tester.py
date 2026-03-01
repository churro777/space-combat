#!/usr/bin/env python3
"""CLI tool for auditioning synthesized sound effect variations.

Single-keypress controls inside a category (no Enter needed):
  w/s = prev/next (auto-plays)    + = like    - = dislike
  r = replay    b = back    v = votes    q = quit
"""

import sys
import os
import tty
import termios

# Allow imports from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pygame
from audio import synth

SOUNDS = {
    "laser": {
        "1. Rising chirp":           lambda: synth.laser_rising_chirp(),
        "2. Charge + fire":          lambda: synth.laser_charge_fire(),
        "3. Harmonic wide sweep":    lambda: synth.laser_harmonic_wide_sweep(),
        "4. Bounce chirp":           lambda: synth.laser_bounce_chirp(),
        "5. Triple chirp":           lambda: synth.laser_triple_chirp(),
        "6. Charge burst":           lambda: synth.laser_charge_burst(),
        "7. Harmonic stutter":       lambda: synth.laser_harmonic_stutter(),
        "8. Slow charge beam":       lambda: synth.laser_slow_charge_beam(),
        "9. Harmonic chirp":         lambda: synth.laser_harmonic_chirp(),
        "10. Rising triple burst":   lambda: synth.laser_rising_triple_burst(),
        "11. Charge harmonic beam":  lambda: synth.laser_charge_harmonic_beam(),
        "12. Swell shot":            lambda: synth.laser_swell_shot(),
        "13. Ascending rings":       lambda: synth.laser_ascending_rings(),
        "14. Quick charge chirp":    lambda: synth.laser_quick_charge_chirp(),
    },
    "scan": {
        "1. Harmonic pulse sweep":     lambda: synth.scan_harmonic_pulse_sweep(),
        "2. Dual pulse":               lambda: synth.scan_dual_pulse(),
        "3. Rising dual pulse":        lambda: synth.scan_rising_dual_pulse(),
        "4. Triple tone sweep":        lambda: synth.scan_triple_tone_sweep(),
        "5. Accelerating pulse sweep": lambda: synth.scan_accelerating_pulse_sweep(),
        "6. Wide rising pulse":        lambda: synth.scan_wide_rising_pulse(),
        "7. Converging pulse":         lambda: synth.scan_converging_pulse(),
        "8. Harmonic rising spread":   lambda: synth.scan_harmonic_rising_spread(),
    },
    "contact": {
        "1. Success ding":           lambda: synth.contact_success_ding(),
        "2. Octave ping":            lambda: synth.contact_octave_ping(),
        "3. Ascending chime":        lambda: synth.contact_ascending_chime(),
        "4. Triple rising pulse":    lambda: synth.contact_triple_rising_pulse(),
    },
    "missile": {
        "1. Deep rocket":            lambda: synth.missile_deep_rocket(),
        "2. Ignition roar":          lambda: synth.missile_ignition_roar(),
        "3. Thunder launch":         lambda: synth.missile_thunder_launch(),
        "4. Deep pulse rocket":      lambda: synth.missile_deep_pulse_rocket(),
        "5. Booster separation":     lambda: synth.missile_booster_separation(),
        "6. Sustained burn":         lambda: synth.missile_sustained_burn(),
        "7. Shockwave launch":       lambda: synth.missile_shockwave_launch(),
        "8. Pressure wave":          lambda: synth.missile_pressure_wave(),
    },
    "explosion": {
        "1. Deep boom":              lambda: synth.explosion_deep_boom(),
        "2. Shockwave boom":         lambda: synth.explosion_shockwave_boom(),
        "3. Crackle boom":           lambda: synth.explosion_crackle_boom(),
        "4. Double boom":            lambda: synth.explosion_double_boom(),
        "5. Rumble fade":            lambda: synth.explosion_rumble_fade(),
        "6. Punch boom":             lambda: synth.explosion_punch_boom(),
        "7. Pulse rumble":           lambda: synth.explosion_pulse_rumble(),
        "8. Massive blast":          lambda: synth.explosion_massive_blast(),
    },
    "destroy": {
        "1. Big boom":               lambda: synth.destroy_big_boom(),
        "2. Cascading explosion":    lambda: synth.destroy_cascading_explosion(),
        "3. Deep shockwave":         lambda: synth.destroy_deep_shockwave(),
        "4. Rumble crescendo":       lambda: synth.destroy_rumble_crescendo(),
        "5. Hollow boom":            lambda: synth.destroy_hollow_boom(),
        "6. Fire crackle":           lambda: synth.destroy_fire_crackle(),
        "7. Double blast":           lambda: synth.destroy_double_blast(),
        "8. Massive rupture":        lambda: synth.destroy_massive_rupture(),
    },
    "shield": {
        "1. Thump ring":             lambda: synth.shield_thump_ring(),
        "2. Pulse absorb":           lambda: synth.shield_pulse_absorb(),
        "3. Impact sizzle":          lambda: synth.shield_impact_sizzle(),
        "4. Heavy thump sizzle":     lambda: synth.shield_heavy_thump_sizzle(),
        "5. Double thump":           lambda: synth.shield_double_thump(),
        "6. Pulse thump":            lambda: synth.shield_pulse_thump(),
        "7. Impact ripple":          lambda: synth.shield_impact_ripple(),
        "8. Thump fade sizzle":      lambda: synth.shield_thump_fade_sizzle(),
        "9. Punch pulse sizzle":     lambda: synth.shield_punch_pulse_sizzle(),
    },
    "shield_recharge": {
        "1. Rising chime":           lambda: synth.shield_recharge_rising_chime(),
        "2. Hum swell":              lambda: synth.shield_recharge_hum_swell(),
        "3. Shimmer":                lambda: synth.shield_recharge_shimmer(),
        "4. Pulse rise":             lambda: synth.shield_recharge_pulse_rise(),
        "5. Bright ping":            lambda: synth.shield_recharge_bright_ping(),
        "6. Sweep chime":            lambda: synth.shield_recharge_sweep_chime(),
        "7. Warm glow":              lambda: synth.shield_recharge_warm_glow(),
        "8. Double ping":            lambda: synth.shield_recharge_double_ping(),
    },
    "music_intro": {
        "1. Dark pads":              lambda: synth.music_intro_dark_pads(),
        "2. Space drift":            lambda: synth.music_intro_space_drift(),
        "3. Deep space":             lambda: synth.music_intro_deep_space(),
        "4. Nebula":                 lambda: synth.music_intro_nebula(),
        "5. Arpeggio":               lambda: synth.music_intro_arpeggio(),
    },
    "music_loop": {
        "1. Combat pulse":           lambda: synth.music_loop_combat_pulse(),
        "2. Tension drive":          lambda: synth.music_loop_tension_drive(),
        "3. Dark march":             lambda: synth.music_loop_dark_march(),
        "4. Space chase":            lambda: synth.music_loop_space_chase(),
        "5. Void pulse":             lambda: synth.music_loop_void_pulse(),
    },
}


def getch():
    """Read a single keypress without waiting for Enter."""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch


def display_list(choice, var_keys, idx, votes):
    """Print the sound list with cursor and vote markers."""
    print(f"\n--- {choice} ---")
    for i, key in enumerate(var_keys):
        vote_key = f"{choice}/{key}"
        marker = ""
        if vote_key in votes:
            marker = "  [+]" if votes[vote_key] == "up" else "  [-]"
        cursor = " >> " if i == idx else "    "
        print(f"{cursor}{key}{marker}")
    print()
    print("  w/s = prev/next    r = replay    + = like    - = dislike")
    print("  b = back           v = votes     q = quit")


def play_sound(variations, var_keys, idx):
    """Generate and play the sound at the given index. Returns the Sound."""
    print(f"  Playing: {var_keys[idx]}")
    sound = variations[var_keys[idx]]()
    sound.play()
    return sound


def main():
    pygame.mixer.init()

    votes = {}
    categories = list(SOUNDS.keys())

    while True:
        print("\n=== Sound Tester ===")
        print("Categories:")
        for cat in categories:
            count = len(SOUNDS[cat])
            print(f"  {cat}  ({count} variations)")
        print("\nType a category name, 'v' for vote summary, or 'q' to quit:")

        choice = input("> ").strip().lower()
        if choice == "q":
            break
        if choice == "v":
            print_votes(votes)
            continue
        if choice not in SOUNDS:
            print(f"Unknown category: {choice}")
            continue

        variations = SOUNDS[choice]
        var_keys = list(variations.keys())
        idx = 0

        display_list(choice, var_keys, idx, votes)
        last_sound = play_sound(variations, var_keys, idx)

        while True:
            key = getch()

            # Ctrl-C / Ctrl-D
            if key in ("\x03", "\x04"):
                print_votes(votes)
                pygame.mixer.quit()
                return

            if key == "q":
                print_votes(votes)
                pygame.mixer.quit()
                return
            if key == "b":
                break
            if key == "w":
                idx = (idx - 1) % len(var_keys)
                display_list(choice, var_keys, idx, votes)
                last_sound = play_sound(variations, var_keys, idx)
                continue
            if key == "s":
                idx = (idx + 1) % len(var_keys)
                display_list(choice, var_keys, idx, votes)
                last_sound = play_sound(variations, var_keys, idx)
                continue
            if key in ("\r", "\n"):
                last_sound = play_sound(variations, var_keys, idx)
                continue
            if key == "r":
                if last_sound:
                    print(f"  Replaying: {var_keys[idx]}")
                    last_sound.play()
                continue
            if key == "+":
                vote_key = f"{choice}/{var_keys[idx]}"
                votes[vote_key] = "up"
                print(f"  Liked: {var_keys[idx]}")
                idx = (idx + 1) % len(var_keys)
                display_list(choice, var_keys, idx, votes)
                last_sound = play_sound(variations, var_keys, idx)
                continue
            if key == "-":
                vote_key = f"{choice}/{var_keys[idx]}"
                votes[vote_key] = "down"
                print(f"  Disliked: {var_keys[idx]}")
                idx = (idx + 1) % len(var_keys)
                display_list(choice, var_keys, idx, votes)
                last_sound = play_sound(variations, var_keys, idx)
                continue
            if key == "v":
                print_votes(votes)
                continue

    print_votes(votes)
    pygame.mixer.quit()


def print_votes(votes):
    if not votes:
        print("\nNo votes yet.")
        return

    liked = [k for k, v in votes.items() if v == "up"]
    disliked = [k for k, v in votes.items() if v == "down"]

    print("\n========== VOTE SUMMARY ==========")
    if liked:
        print("\n  LIKED:")
        for name in liked:
            print(f"    [+] {name.split('/', 1)[1]}")
    if disliked:
        print("\n  DISLIKED:")
        for name in disliked:
            print(f"    [-] {name.split('/', 1)[1]}")
    print("\n==================================")


if __name__ == "__main__":
    main()
