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

    def process_events(self) -> tuple[bool, dict | None, bool]:
        """Process pygame events. Returns (quit, action_or_none, restart)."""
        action = None
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
                elif event.key == pygame.K_SPACE and action is None:
                    action = {"type": "fire"}
                elif event.key == pygame.K_f and action is None:
                    action = {"type": "scan"}
                elif event.key in _MOVE_KEYS and action is None:
                    direction = _get_move_direction(pygame.key.get_pressed())
                    if direction:
                        action = {"type": "move", "direction": direction}

        return quit_game, action, restart
