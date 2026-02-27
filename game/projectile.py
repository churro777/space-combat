import math
from dataclasses import dataclass
from settings import GRID_SIZE


@dataclass
class Laser:
    x: int
    y: int
    dx: int
    dy: int
    owner: str  # "player" or "bot"

    def advance(self):
        """Move laser 2 tiles (speed of light). Returns list of tiles traversed this step."""
        tiles = []
        for _ in range(2):
            self.x += self.dx
            self.y += self.dy
            tiles.append((self.x, self.y))
        return tiles

    def is_on_grid(self) -> bool:
        return 0 <= self.x < GRID_SIZE and 0 <= self.y < GRID_SIZE


@dataclass
class ScanPulse:
    origin_x: int
    origin_y: int
    radius: int
    owner: str  # "player" or "bot"
    returning: bool = False
    contact_position: tuple[int, int] | None = None
    contact_turn: int | None = None

    def expand(self):
        """Expand radius by 2 (speed of light)."""
        self.radius += 2

    def is_expired(self) -> bool:
        """Pulse expired if ring is entirely off-grid."""
        return self.radius > GRID_SIZE * 2


@dataclass
class Missile:
    x: float
    y: float
    target_x: int
    target_y: int
    owner: str  # "player" or "bot"
    alive: bool = True

    def advance(self) -> bool:
        """Move 1 tile toward target per tick. Returns True if reached target."""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist <= 1.0:
            self.x = float(self.target_x)
            self.y = float(self.target_y)
            return True
        self.x += dx / dist
        self.y += dy / dist
        return False

    def is_on_grid(self) -> bool:
        return 0 <= self.x < GRID_SIZE and 0 <= self.y < GRID_SIZE
