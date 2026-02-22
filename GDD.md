# Space Combat v2 — Game Design Document

## Overview

**Genre:** Turn-based relativistic space combat
**Engine:** Python + Pygame
**Platform:** Desktop (Windows, macOS, Linux)

A two-player (player vs bot for now) space combat game where all information and weapons travel at the speed of light. Ships move slower than light, creating an inherent information delay — you never know where the enemy *currently* is, only where they *were* when your scan reached them. The core gameplay is using stale scan data to predict enemy movement and land shots.

## Core Concept: Lightspeed Delay

Everything in this game revolves around one physical constraint: **information cannot travel faster than light.**

- **Scans** travel at the speed of light (c). They go out, bounce off an enemy, and return at c. The player learns where the enemy was *at the moment the scan hit them* — not where they are now.
- **Lasers** travel at c (one-way). The player fires at a target position and the laser takes time to arrive. If the enemy has moved, it misses.
- **Ships** move at 0.5c. Between the time a scan hits an enemy and the data returns, the enemy could have moved a significant distance.

This means:

- Scan data is always outdated by the time you receive it.
- Shooting requires predicting where the enemy will be when the laser arrives.
- The farther away the enemy is, the more stale your information and the harder it is to hit them.

## Turn Structure

Each turn, both players (player and bot) choose **one** action:

| Action           | Speed              | Description                                                                                                                                    |
| ---------------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **Fire Laser**   | c (2 tiles/turn)   | Fires a laser in a straight line toward a target position. Travels at lightspeed. Destroys on hit.                                             |
| **Move**         | 0.5c (1 tile/turn) | Move the ship one step in a chosen direction.                                                                                                  |
| **Scan**         | c (2 tiles/turn)   | Emits an omnidirectional pulse (like radar) that expands outward in all directions at lightspeed. On contact with enemy, bounces back at lightspeed. Returns the enemy's position *at the time of contact*. |

Both players choose actions simultaneously each turn, then all actions resolve.

> **Speed units (v1 — grid):** For the grid-based prototype, the speed of light = 2 tiles per turn. Ship speed = 0.5c = 1 tile per turn. This keeps ship movement aligned to the grid — one move action = one tile.

## Game Rules

### Information & Fog of War

- Neither player can see the other's ship directly.
- The only way to learn the enemy's position is via scan results.
- A scan result tells you: **"The enemy was at position (x, y) on turn N"** — where N is the turn the scan reached them, not the current turn.
- Scan hits are displayed on the grid as markers at the position the enemy was detected. Each marker shows how many turns ago the scan hit (e.g., "2 turns ago"). The age updates every turn so the player can see their intel getting staler over time.
- Multiple scan markers can exist on the grid at once, forming a breadcrumb trail of past enemy positions that helps the player extrapolate movement direction and speed.

### Combat

- A laser is fired at a **target coordinate**, not at the enemy ship directly.
- The laser travels toward that coordinate at c (2 tiles/turn) and keeps going past the target if it doesn't hit anything.
- Each turn, the laser checks every tile it passes through for a collision with the enemy ship. A hit can happen before reaching the target, at the target, or beyond it.
- The laser continues until it hits a ship or leaves the grid.
- **One hit = destroyed** (for now).

### Future Combat (not in v1)

- Shields absorb damage before hull takes damage.
- Hull has HP — destroyed at 0.
- Missiles: slower than lasers, more damage, possibly area effect.
- Mines: stationary hazards left on the grid.

### Win/Lose

- Destroy the enemy ship to win.
- Your ship is destroyed, you lose.

## Grid Setup (v1)

- 2D grid, size TBD (e.g., 16x16 or 20x20 — large enough that lightspeed delay matters).
- Both ships start on opposite ends, hidden from each other.
- Dark space background with subtle grid lines.

## Bot AI (v1)

The bot plays by the same rules as the player — no cheating, no seeing the player's position without scanning. Basic strategy:

1. Scan periodically to locate the player.
2. Move unpredictably to avoid being predictable.
3. When it has scan data, estimate the player's current position and fire.

## Player UI

- Grid view showing your ship and any known information (scan results, laser paths).
- Scan history panel showing past scan results with timestamps (turn numbers).
- Action selection: Fire / Move / Scan.
- If Fire: select target coordinate on grid.
- If Move: select direction (up/down/left/right).
- If Scan: no input needed — pulse goes out in all directions automatically.

## Future Plans (not in v1)

- **Two-player multiplayer** — replace bot with a second human player.
- **Free 2D space** — replace grid with continuous coordinates and vector movement.
- **Ship loadouts** — shields, hull HP, weapon types.
- **Weapon variety** — missiles (slower, more damage), mines (stationary).
- **Advanced movement** — velocity/momentum instead of tile-by-tile.

## Technical Architecture

```text
space_combat_v2/
├── GDD.md                # This document
├── requirements.txt      # Python dependencies
├── main.py               # Entry point
├── settings.py           # Constants (grid size, speeds, colors)
├── game/
│   ├── __init__.py
│   ├── engine.py         # Game loop, turn management, state
│   ├── grid.py           # Grid logic, coordinate system
│   ├── ship.py           # Ship class (position, actions)
│   ├── projectile.py     # Lasers, scans — things that travel at c
│   ├── combat.py         # Hit detection, damage resolution
│   └── bot.py            # Enemy AI (plays by same rules as player)
├── ui/
│   ├── __init__.py
│   ├── renderer.py       # Pygame drawing (grid, ships, effects)
│   ├── hud.py            # Scan history, action buttons, status
│   └── input_handler.py  # Mouse/keyboard input
└── assets/
    ├── fonts/
    └── sprites/
```

## Milestones

### M1 — Foundations

- [ ] Pygame window + game loop
- [ ] Grid rendering
- [ ] Player ship on grid, movement working

### M2 — Core Mechanics

- [ ] Turn system (simultaneous action selection + resolution)
- [ ] Scan: travels out, hits enemy, returns with position data
- [ ] Laser: travels to target coordinate, hit detection
- [ ] Fog of war (enemy hidden until scanned)

### M3 — Bot Opponent

- [ ] Bot that scans, moves, and shoots by the same rules
- [ ] Basic prediction logic for bot targeting

### M4 — Playable Game

- [ ] Win/lose detection
- [ ] Scan history display
- [ ] Visual feedback (laser paths, scan pulses, hit/miss)
- [ ] Start screen, game over screen
