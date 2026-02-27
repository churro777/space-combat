import random
from game.ship import Ship
from settings import DIRECTIONS, GRID_SIZE

DIR_LIST = list(DIRECTIONS.values())
DIR_NAMES = list(DIRECTIONS.keys())


class Bot:
    def __init__(self):
        self.last_move_dir = random.choice(DIR_LIST)

    def choose_action(self, ship: Ship, tick: int) -> tuple[tuple[int, int] | None, bool, bool, bool]:
        """Returns (direction, fire, scan, missile) for this tick."""
        if not ship.alive:
            return None, False, False, False

        recent = self._latest_scan(ship, tick)

        # If no scan data or data is very stale, scan
        if recent is None or (tick - recent.turn_received) > 60:
            return self._random_move(ship), False, True, False

        # Predict enemy moved randomly — aim at last known position
        ex, ey = recent.enemy_position

        # Occasionally fire a missile at last known position
        fire_missile = (
            ship.missile_cooldown == 0
            and ship.missiles_remaining > 0
            and random.random() < 0.2
        )

        # With some probability, fire towards target
        if random.random() < 0.6:
            self._face_towards(ship, ex, ey)
            return None, True, False, fire_missile

        # Otherwise move to reposition
        return self._random_move(ship), False, False, fire_missile

    def _latest_scan(self, ship: Ship, tick: int):
        if not ship.scan_results:
            return None
        return max(ship.scan_results, key=lambda s: s.turn_received)

    def _face_towards(self, ship: Ship, tx: int, ty: int):
        dx = tx - ship.x
        dy = ty - ship.y
        if dx != 0:
            dx = dx // abs(dx)
        if dy != 0:
            dy = dy // abs(dy)
        if (dx, dy) == (0, 0):
            dx, dy = random.choice(DIR_LIST)
        ship.facing = (dx, dy)

    def _random_move(self, ship: Ship) -> tuple[int, int]:
        if random.random() < 0.3:
            self.last_move_dir = random.choice(DIR_LIST)
        dx, dy = self.last_move_dir
        nx, ny = ship.x + dx, ship.y + dy
        if not (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE):
            self.last_move_dir = random.choice(DIR_LIST)
        return self.last_move_dir
