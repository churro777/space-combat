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

    def ring_tiles(self) -> list[tuple[int, int]]:
        """Return all tiles on the Chebyshev ring at current radius."""
        if self.radius == 0:
            return [(self.origin_x, self.origin_y)]
        tiles = []
        r = self.radius
        cx, cy = self.origin_x, self.origin_y
        for d in range(-r, r + 1):
            tiles.append((cx + d, cy - r))  # top edge
            tiles.append((cx + d, cy + r))  # bottom edge
        for d in range(-r + 1, r):
            tiles.append((cx - r, cy + d))  # left edge
            tiles.append((cx + r, cy + d))  # right edge
        return [(x, y) for x, y in tiles if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE]

    def expand(self):
        """Expand radius by 2 (speed of light)."""
        self.radius += 2

    def is_expired(self) -> bool:
        """Pulse expired if outgoing ring is entirely off-grid."""
        if self.returning:
            return self.radius <= 0
        return self.radius > GRID_SIZE * 2
