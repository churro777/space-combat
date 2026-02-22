import random
from game.ship import Ship
from settings import DIRECTIONS, GRID_SIZE

DIR_LIST = list(DIRECTIONS.values())
DIR_NAMES = list(DIRECTIONS.keys())


class Bot:
    def __init__(self):
        self.last_move_dir = random.choice(DIR_LIST)

    def choose_action(self, ship: Ship, turn: int) -> dict:
        if not ship.alive:
            return {"type": "wait"}

        recent = self._latest_scan(ship, turn)

        # If no scan data or data is very stale, scan
        if recent is None or (turn - recent.turn_received) > 6:
            return {"type": "scan"}

        staleness = turn - recent.turn_detected
        ex, ey = recent.enemy_position

        # Predict enemy moved randomly — aim at last known position
        # With some probability, lead the shot
        if random.random() < 0.6:
            return self._fire_towards(ship, ex, ey)

        # Otherwise move to reposition
        return self._random_move(ship)

    def _latest_scan(self, ship: Ship, turn: int):
        if not ship.scan_results:
            return None
        return max(ship.scan_results, key=lambda s: s.turn_received)

    def _fire_towards(self, ship: Ship, tx: int, ty: int) -> dict:
        dx = tx - ship.x
        dy = ty - ship.y
        # Snap to nearest of 8 directions
        if dx != 0:
            dx = dx // abs(dx)
        if dy != 0:
            dy = dy // abs(dy)
        if (dx, dy) == (0, 0):
            dx, dy = random.choice(DIR_LIST)
        return {"type": "fire", "direction": (dx, dy)}

    def _random_move(self, ship: Ship) -> dict:
        # Prefer continuing in same direction, but sometimes change
        if random.random() < 0.3:
            self.last_move_dir = random.choice(DIR_LIST)
        dx, dy = self.last_move_dir
        nx, ny = ship.x + dx, ship.y + dy
        if not (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE):
            self.last_move_dir = random.choice(DIR_LIST)
        return {"type": "move", "direction": self.last_move_dir}
