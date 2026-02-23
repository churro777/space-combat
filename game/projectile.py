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
