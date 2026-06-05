# Mobile Support — Design Spec

Adds touch controls and responsive layout so the game is playable on mobile browsers (landscape orientation) via the existing Pygbag/GitHub Pages deployment.

**Constraints**: No changes to game logic (`engine.py`, `bot.py`, `ship.py`, `projectile.py`). Mobile support is purely input + rendering + layout.

---

## 1. Mobile Detection

At startup in `main.py`, detect whether the game is running on a touch device:

- Use Pygbag's JS interop to check `navigator.maxTouchPoints > 0`
- Fall back to screen dimension heuristics if needed (viewport width < 1100)
- Set `settings.MOBILE = True` at runtime so other modules can read it

When `MOBILE` is true:
- Skip sidebar — `pygame.display.set_mode((viewport_w, viewport_h))` with no sidebar width
- Enable touch controls
- Use mobile HUD (top bar) instead of sidebar HUD
- Modify title and game-over screens for touch

When `MOBILE` is false: everything works exactly as today.

## 2. Screen Scaling & Viewport Math

On mobile startup:
- Query browser viewport dimensions via JS interop
- Grid area = full width × (full height − 28px top bar)
- `VIEWPORT_TILE_PX = min(grid_width, grid_height) / VIEWPORT_TILES`
- `VIEWPORT_TILES` stays at 40 (same tactical view, scaled to fit)
- Grid is centered if aspect ratio doesn't fill both axes

Touch control sizing (joystick radius, button sizes, positions) is defined as percentages of screen height, not hard-coded pixels. This ensures proportional feel across phone (667px wide) and tablet (1024px wide) screens.

## 3. Touch Input System

**New file: `ui/touch_input.py`**

### Virtual Joystick (left thumb)

- Activates on `FINGERDOWN` in the left 40% of the screen
- Tracks finger via `FINGERMOTION` — calculates angle/distance from initial touch point
- Snaps to one of 8 directions (N/NE/E/SE/S/SW/W/NW) based on angle
- Dead zone: small radius around touch origin where no direction is registered
- Deactivates on `FINGERUP` — movement stops immediately
- Visual: renders joystick base circle + thumb dot at current finger position

### Action Buttons (right thumb)

Three circular touch zones in the bottom-right:
- **FIRE** (large, ~60px equivalent) — bottom center-right, primary action
- **SCAN** (smaller, ~45px equivalent) — above-left of fire
- **MISSILE** (smaller, ~45px equivalent) — above-right of fire

Edge-triggered: one press per `FINGERDOWN`, no auto-repeat (matches keyboard behavior).

Visual: semi-transparent circles with labels, drawn over the game grid.

### Multi-touch

Pygame's `FINGERDOWN`/`FINGERUP`/`FINGERMOTION` events include `finger_id`. The joystick tracks one finger, action buttons track independently. Left-thumb movement and right-thumb firing work simultaneously.

### Integration with InputHandler

- `InputHandler.__init__` gets a `touch_controls` parameter (`TouchInput` instance or `None`)
- `process_events()` passes `FINGERDOWN`/`UP`/`MOTION` events to `TouchInput`
- `get_continuous_state()` merges touch direction/actions with keyboard/gamepad — any source can provide input (same pattern as existing joystick merge)

## 4. Mobile HUD (Top Bar)

**New file: `ui/mobile_hud.py`**

A 28px full-width bar at the top of the screen. Same interface as `HUD`: `draw(engine)`.

### Contents (left to right)

- **Left group**: Shield status (text: "SHIELD" when up, countdown when recharging), time elapsed
- **Center group**: Three cooldown mini-bars (Fire, Scan, Missile) with labels, plus missile count (e.g. "3/5")
- **Right group**: Facing direction + coordinates (e.g. "N · (45,32)")

### What it drops vs desktop HUD

- Controls legend (touch buttons are self-explanatory)
- Scan history text (on-grid diamond markers already show this)

### Flash messages

Same bottom-of-grid text position, but relative to grid area not sidebar.

## 5. Title Screen (Mobile)

- "Tap to start" replaces "Press ENTER to start" (blinking text, same cadence)
- Controller detection text hidden
- Any `FINGERDOWN` event triggers game start
- Title and subtitle rendering unchanged

## 6. Game Over Screen (Mobile)

- Same dark overlay and win/lose/draw text
- "Press R to restart or Q to quit" replaced with "TAP TO PLAY AGAIN"
- Any `FINGERDOWN` on the overlay triggers restart
- No quit button (mobile users close the tab)

## 7. Files Changed

| File | Change |
|------|--------|
| `settings.py` | Add `MOBILE` flag, mobile viewport constants |
| `main.py` | Mobile detection at startup, conditional layout, touch event routing to title/game-over screens |
| `ui/touch_input.py` | **New** — virtual joystick + action button touch handling + rendering |
| `ui/mobile_hud.py` | **New** — 28px top bar HUD for mobile |
| `ui/input_handler.py` | Accept optional `TouchInput`, merge touch state in `get_continuous_state()` |
| `ui/renderer.py` | Minor: adjust grid fill area when mobile (no sidebar) |
| `ui/hud.py` | No changes (desktop HUD stays as-is) |
| `game/*` | No changes |

## 8. Out of Scope

- Portrait orientation support
- On-screen scan history list
- Pinch-to-zoom or camera gestures
- Sound/music changes for mobile
- Responsive desktop sidebar
