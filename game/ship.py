from dataclasses import dataclass, field


@dataclass
class ScanResult:
    enemy_position: tuple[int, int]
    turn_detected: int
    turn_received: int


@dataclass
class Ship:
    x: int
    y: int
    alive: bool = True
    scan_results: list[ScanResult] = field(default_factory=list)

    @property
    def position(self) -> tuple[int, int]:
        return (self.x, self.y)

    @position.setter
    def position(self, value: tuple[int, int]):
        self.x, self.y = value
