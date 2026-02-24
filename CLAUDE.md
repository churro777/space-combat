# Space Combat v2 — Relativistic Warfare

A real-time space combat game built with Python and Pygame. Two ships battle on a grid where information travels at lightspeed, creating tactical fog-of-war.

## Core Concepts

- **Relativistic physics**: Lightspeed (C_SPEED=2 tiles/tick) is only 2x ship speed. Lasers and scan pulses travel at C; you can't see the enemy until a scan pulse reaches them and returns.
- **Real-time with tick accumulator**: Renders at 60 FPS, game logic ticks at 10/s. The tick accumulator pattern decouples rendering from physics.
- **100x100 grid**, 7px per tile. 8-direction movement. Ships clamp to boundaries.
- **Cooldowns**: Move (2 ticks), Fire (5 ticks), Scan (10 ticks). Creates tactical timing decisions.
- **Scan system**: Outgoing pulse expands at lightspeed → detects enemy on contact → return pulse carries detection data back to sender. Scan breadcrumbs expire after ~10s.

## Project Structure

```
main.py              Entry point, title screen, game loop, tick accumulator, controller init
settings.py          All constants (grid size, speeds, cooldowns, colors, directions)
game/
  engine.py          Core engine: tick(), movement, laser/scan propagation, collision, win conditions
  ship.py            Ship dataclass (position, facing, cooldowns, scan_results)
  projectile.py      Laser (2 tiles/tick, trail) and ScanPulse (expanding ring, return signal)
  bot.py             AI opponent: periodic scanning, fires at last known position, random movement
ui/
  renderer.py        Draws grid, ships (directional triangles), lasers, scan pulses, breadcrumbs
  hud.py             Sidebar HUD: time, position, cooldown bars, scan history, game over overlay
  input_handler.py   Keyboard (WASD/arrows, Space, F) + gamepad (stick/dpad, A/B/Start)
```

## Running

```
source .venv/bin/activate
python3 main.py
```

## Controls

| Action  | Keyboard        | Controller       |
|---------|-----------------|------------------|
| Move    | WASD / Arrows   | Left stick / D-pad |
| Fire    | Space           | A button         |
| Scan    | F               | B button         |
| Start   | Enter           | Start            |
| Restart | R               | Start            |
| Quit    | Q               | —                |
| Debug   | Backtick (`)    | —                |

## Dev Notes

- Gamepad init has workarounds for macOS SDL joystick calibration errors — see `_init_joystick()` and `_safe_event_get()` in main.py
- Bot difficulty is tunable via scan interval, fire probability, and direction change rate in bot.py
- Debug mode (backtick) shows scan pulse circles and extra rendering info
