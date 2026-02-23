import pygame
from settings import DIRECTIONS

_STICK_DEADZONE = 0.4


def _safe_event_get():
    """Wrapper around pygame.event.get() that handles joystick-poisoned queues."""
    try:
        return pygame.event.get()
    except (SystemError, KeyError):
        pygame.event.clear()
        return []

# Map held keys to direction components
_MOVE_KEYS = {
    pygame.K_w: (0, -1), pygame.K_UP: (0, -1),
    pygame.K_s: (0, 1),  pygame.K_DOWN: (0, 1),
    pygame.K_a: (-1, 0), pygame.K_LEFT: (-1, 0),
    pygame.K_d: (1, 0),  pygame.K_RIGHT: (1, 0),
}


def _get_move_direction(keys) -> tuple[int, int] | None:
    """Check held keys and return a combined direction, or None if no move keys held."""
    dx, dy = 0, 0
    for key, (kdx, kdy) in _MOVE_KEYS.items():
        if keys[key]:
            dx += kdx
            dy += kdy
    if dx == 0 and dy == 0:
        return None
    # Clamp to unit vector for diagonals
    if dx != 0:
        dx = dx // abs(dx)
    if dy != 0:
        dy = dy // abs(dy)
    return (dx, dy)


def _get_joystick_direction(joystick) -> tuple[int, int] | None:
    """Read left stick + d-pad hat and return a direction, or None."""
    dx, dy = 0.0, 0.0

    # Left stick (axes 0, 1)
    ax = joystick.get_axis(0)
    ay = joystick.get_axis(1)
    if abs(ax) > _STICK_DEADZONE:
        dx += ax
    if abs(ay) > _STICK_DEADZONE:
        dy += ay

    # D-pad hat (first hat)
    if joystick.get_numhats() > 0:
        hx, hy = joystick.get_hat(0)
        dx += hx
        dy -= hy  # hat y is inverted (up = +1)

    if dx == 0 and dy == 0:
        return None

    # Snap to unit vector
    sdx = 1 if dx > 0 else (-1 if dx < 0 else 0)
    sdy = 1 if dy > 0 else (-1 if dy < 0 else 0)
    return (sdx, sdy)


class InputHandler:
    def __init__(self, hud, renderer, joystick=None):
        self.hud = hud
        self.renderer = renderer
        self.joystick = joystick
        self._fire_pressed = False
        self._scan_pressed = False

    def process_events(self) -> tuple[bool, bool]:
        """Process pygame events. Returns (quit, restart)."""
        restart = False
        quit_game = False

        for event in _safe_event_get():
            if event.type == pygame.QUIT:
                quit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit_game = True
                elif event.key == pygame.K_r:
                    restart = True
                elif event.key == pygame.K_BACKQUOTE:
                    self.renderer.debug = not self.renderer.debug
                elif event.key == pygame.K_SPACE:
                    self._fire_pressed = True
                elif event.key == pygame.K_f:
                    self._scan_pressed = True
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:      # A → fire
                    self._fire_pressed = True
                elif event.button == 1:    # B → scan
                    self._scan_pressed = True
                elif event.button == 6:    # Start → restart
                    restart = True

        return quit_game, restart

    def get_continuous_state(self) -> tuple[tuple[int, int] | None, bool, bool]:
        """Returns (direction, fire, scan) for the current tick.
        Fire and scan are edge-triggered (one-shot per keypress)."""
        keys = pygame.key.get_pressed()
        direction = _get_move_direction(keys)

        # Merge joystick direction (either source can provide direction)
        if direction is None and self.joystick is not None:
            direction = _get_joystick_direction(self.joystick)

        fire = self._fire_pressed
        scan = self._scan_pressed
        self._fire_pressed = False
        self._scan_pressed = False

        return direction, fire, scan
