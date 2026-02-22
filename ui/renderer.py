import pygame
from settings import (
    GRID_SIZE, TILE_SIZE, COLOR_BG, COLOR_GRID, COLOR_PLAYER, COLOR_ENEMY,
    COLOR_LASER_P, COLOR_LASER_E, COLOR_SCAN_OUT, COLOR_SCAN_RET,
    COLOR_SCAN_MARK, COLOR_WHITE,
)


class Renderer:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.font = pygame.font.SysFont("monospace", 14)

    def draw(self, engine):
        self._draw_grid()
        self._draw_scan_pulses(engine)
        self._draw_lasers(engine)
        self._draw_scan_markers(engine.player)
        self._draw_ship(engine.player, COLOR_PLAYER)
        # Bot is invisible — only scan markers show where it might be

    def _draw_grid(self):
        grid_area = GRID_SIZE * TILE_SIZE
        self.surface.fill(COLOR_BG, (0, 0, grid_area, grid_area))
        for i in range(GRID_SIZE + 1):
            x = i * TILE_SIZE
            pygame.draw.line(self.surface, COLOR_GRID, (x, 0), (x, grid_area))
            pygame.draw.line(self.surface, COLOR_GRID, (0, x), (grid_area, x))

    def _draw_ship(self, ship, color):
        if not ship.alive:
            return
        cx = ship.x * TILE_SIZE + TILE_SIZE // 2
        cy = ship.y * TILE_SIZE + TILE_SIZE // 2
        r = TILE_SIZE // 3
        pygame.draw.polygon(self.surface, color, [
            (cx, cy - r),
            (cx - r, cy + r),
            (cx + r, cy + r),
        ])

    def _draw_lasers(self, engine):
        for laser in engine.lasers:
            color = COLOR_LASER_P if laser.owner == "player" else COLOR_LASER_E
            cx = laser.x * TILE_SIZE + TILE_SIZE // 2
            cy = laser.y * TILE_SIZE + TILE_SIZE // 2
            # Draw a bright dot for the laser head
            pygame.draw.circle(self.surface, color, (cx, cy), 5)
            # Draw a tail trailing back
            tail_x = cx - laser.dx * TILE_SIZE
            tail_y = cy - laser.dy * TILE_SIZE
            pygame.draw.line(self.surface, color, (tail_x, tail_y), (cx, cy), 2)

    def _draw_scan_pulses(self, engine):
        for pulse in engine.scan_pulses:
            if pulse.radius <= 0:
                continue
            color = COLOR_SCAN_RET if pulse.returning else COLOR_SCAN_OUT
            # Draw Chebyshev ring as a rectangle outline
            left = (pulse.origin_x - pulse.radius) * TILE_SIZE
            top = (pulse.origin_y - pulse.radius) * TILE_SIZE
            size = pulse.radius * 2 * TILE_SIZE
            rect = pygame.Rect(left, top, size, size)
            pygame.draw.rect(self.surface, color, rect, 1)

    def _draw_scan_markers(self, player_ship):
        for result in player_ship.scan_results:
            ex, ey = result.enemy_position
            cx = ex * TILE_SIZE + TILE_SIZE // 2
            cy = ey * TILE_SIZE + TILE_SIZE // 2
            # Ghost diamond marker
            s = TILE_SIZE // 4
            pygame.draw.polygon(self.surface, COLOR_SCAN_MARK, [
                (cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy),
            ], 2)
            # Staleness label
            label = self.font.render(f"t-{result.turn_received - result.turn_detected}", True, COLOR_SCAN_MARK)
            self.surface.blit(label, (cx + s + 2, cy - 8))
