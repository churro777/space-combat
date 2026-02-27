#!/usr/bin/env python3
"""CLI tool for auditioning synthesized sound effect variations."""

import sys
import os

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
}


def main():
    pygame.mixer.init()

    last_sound = None
    last_name = None
    votes = {}  # "category/name" -> "up" or "down"
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

        while True:
            print(f"\n--- {choice} ---")
            for key in var_keys:
                vote_key = f"{choice}/{key}"
                marker = ""
                if vote_key in votes:
                    marker = "  [+]" if votes[vote_key] == "up" else "  [-]"
                print(f"  {key}{marker}")
            if last_name:
                print(f"\n  Selected: {last_name}")
            print()
            print("  # = select    Enter = play    + = like    - = dislike")
            print("  b = back      v = votes       q = quit")

            pick = input("> ").strip().lower()
            if pick == "q":
                print_votes(votes)
                pygame.mixer.quit()
                return
            if pick == "b":
                break
            if pick == "v":
                print_votes(votes)
                continue
            if pick == "" and last_sound:
                print(f"Playing: {last_name}")
                last_sound.play()
                continue
            if pick == "+" and last_name:
                vote_key = f"{choice}/{last_name}"
                votes[vote_key] = "up"
                print(f"  Liked: {last_name}")
                continue
            if pick == "-" and last_name:
                vote_key = f"{choice}/{last_name}"
                votes[vote_key] = "down"
                print(f"  Disliked: {last_name}")
                continue

            # Match by leading number
            matched = None
            for key in var_keys:
                if key.startswith(pick + "."):
                    matched = key
                    break

            if matched is None:
                print(f"Unknown choice: {pick}")
                continue

            print(f"Playing: {matched}")
            sound = variations[matched]()
            sound.play()
            last_sound = sound
            last_name = matched

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
