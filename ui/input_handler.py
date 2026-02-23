import pygame
from settings import DIRECTIONS


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


class InputHandler:
    def __init__(self, hud, renderer):
        self.hud = hud
        self.renderer = renderer
        self._fire_pressed = False
        self._scan_pressed = False

    def process_events(self) -> tuple[bool, bool]:
        """Process pygame events. Returns (quit, restart)."""
        restart = False
        quit_game = False

        for event in pygame.event.get():
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

        return quit_game, restart

    def get_continuous_state(self) -> tuple[tuple[int, int] | None, bool, bool]:
        """Returns (direction, fire, scan) for the current tick.
        Fire and scan are edge-triggered (one-shot per keypress)."""
        keys = pygame.key.get_pressed()
        direction = _get_move_direction(keys)

        fire = self._fire_pressed
        scan = self._scan_pressed
        self._fire_pressed = False
        self._scan_pressed = False

        return direction, fire, scan
