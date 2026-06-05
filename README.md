# Space Combat v2 — Relativistic Warfare

A real-time space combat game where information travels at lightspeed. Two ships battle on a grid, but you can't see the enemy until your scan pulse reaches them and bounces back. Lightspeed is only 2x ship speed, so positioning and timing matter as much as aim.

## Setup

Requires Python 3.10+ and Pygame.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running

```bash
source .venv/bin/activate
python3 main.py
```

## How to Play

You control the green ship against an AI opponent on a 100x100 grid. You can't see the enemy by default — you have to **scan** to find them, then **fire** before your intel goes stale.

**Keyboard:**

| Action | Key |
|--------|-----|
| Move | WASD or Arrow keys |
| Fire laser | Space |
| Scan | F |
| Debug overlay | Backtick (`) |
| Restart | R |
| Quit | Q |

**Controller:**

| Action | Button |
|--------|--------|
| Move | Left stick or D-pad |
| Fire | A |
| Scan | B |
| Start/Restart | Start |

## Core Mechanics

- **Scan** sends an expanding pulse at lightspeed. When it hits the enemy, a return signal carries their position back to you. Scan results fade after ~10 seconds.
- **Lasers** also travel at lightspeed (2 tiles/tick). The enemy may have moved by the time your shot arrives.
- **Cooldowns** create tactical rhythm: Move (2 ticks), Fire (5 ticks), Scan (10 ticks).
- **Debug mode** (backtick) shows scan pulse rings and extra info.
