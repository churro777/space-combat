import math
import pygame
from settings import (
    GRID_SIZE, TILE_SIZE, COLOR_BG, COLOR_GRID, COLOR_PLAYER, COLOR_ENEMY,
    COLOR_LASER_P, COLOR_LASER_E, COLOR_SCAN_OUT, COLOR_SCAN_RET,
    COLOR_SCAN_MARK, COLOR_WHITE,
)

HALF = TILE_SIZE / 2


class Renderer:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.font = pygame.font.SysFont("monospace", 10)
        self.debug = False

    def draw(self, engine):
        self._draw_grid()
        self._draw_scan_pulses(engine)
        self._draw_lasers(engine)
        self._draw_scan_markers(engine.player, engine.tick_count)
        self._draw_ship(engine.player, COLOR_PLAYER)
        if self.debug:
            self._draw_ship(engine.bot, COLOR_ENEMY)

    def _draw_grid(self):
        grid_area = GRID_SIZE * TILE_SIZE
        self.surface.fill(COLOR_BG, (0, 0, grid_area, grid_area))
        step = max(1, 10 if TILE_SIZE < 10 else 1)
        for i in range(0, GRID_SIZE + 1, step):
            x = i * TILE_SIZE
            pygame.draw.line(self.surface, COLOR_GRID, (x, 0), (x, grid_area))
            pygame.draw.line(self.surface, COLOR_GRID, (0, x), (grid_area, x))

    def _draw_ship(self, ship, color):
        if not ship.alive:
            return
        cx = ship.x * TILE_SIZE + HALF
        cy = ship.y * TILE_SIZE + HALF
        r = max(TILE_SIZE // 2, 4)
        fdx, fdy = ship.facing
        angle = math.atan2(-fdy, fdx)
        points = []
        for a in [0, 2.4, -2.4]:
            px = cx + r * math.cos(angle + a)
            py = cy - r * math.sin(angle + a)
            points.append((px, py))
        pygame.draw.polygon(self.surface, color, points)

    def _draw_lasers(self, engine):
        for laser in engine.lasers:
            color = COLOR_LASER_P if laser.owner == "player" else COLOR_LASER_E
            cx = laser.x * TILE_SIZE + HALF
            cy = laser.y * TILE_SIZE + HALF
            pygame.draw.circle(self.surface, color, (int(cx), int(cy)), max(3, TILE_SIZE // 2))
            tail_x = cx - laser.dx * TILE_SIZE * 2
            tail_y = cy - laser.dy * TILE_SIZE * 2
            pygame.draw.line(self.surface, color, (int(tail_x), int(tail_y)), (int(cx), int(cy)), 2)

    def _draw_scan_pulses(self, engine):
        if not self.debug:
            return
        for pulse in engine.scan_pulses:
            if pulse.radius <= 0:
                continue
            color = COLOR_PLAYER if pulse.owner == "player" else COLOR_ENEMY
            cx = int(pulse.origin_x * TILE_SIZE + HALF)
            cy = int(pulse.origin_y * TILE_SIZE + HALF)
            pixel_radius = int(pulse.radius * TILE_SIZE)
            if pulse.returning:
                # Solid line for return
                pygame.draw.circle(self.surface, color, (cx, cy), pixel_radius, 2)
            else:
                # Dashed circle for outgoing
                self._draw_dashed_circle(cx, cy, pixel_radius, color)

    def _draw_dashed_circle(self, cx, cy, radius, color, dash_len=12, gap_len=8):
        if radius < 1:
            return
        circumference = 2 * math.pi * radius
        total = dash_len + gap_len
        segments = max(1, int(circumference / total))
        for i in range(segments):
            start_angle = (i * total / radius)
            end_angle = start_angle + dash_len / radius
            # Draw arc as short line segments
            steps = max(2, dash_len // 3)
            points = []
            for s in range(steps + 1):
                a = start_angle + (end_angle - start_angle) * s / steps
                px = cx + radius * math.cos(a)
                py = cy + radius * math.sin(a)
                points.append((int(px), int(py)))
            if len(points) >= 2:
                pygame.draw.lines(self.surface, color, False, points, 1)

    def _draw_scan_markers(self, player_ship, engine_tick_count):
        from settings import SCAN_MAX_AGE
        alive = [r for r in player_ship.scan_results if engine_tick_count - r.turn_detected <= SCAN_MAX_AGE]
        recent = alive[-10:]
        total = len(recent)
        for i, result in enumerate(recent):
            ex, ey = result.enemy_position
            cx = ex * TILE_SIZE + HALF
            cy = ey * TILE_SIZE + HALF
            s = max(TILE_SIZE // 2, 4)
            pygame.draw.polygon(self.surface, COLOR_SCAN_MARK, [
                (cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy),
            ], 2)
            rank = total - i  # newest = 1, oldest = N
            label = self.font.render(str(rank), True, COLOR_SCAN_MARK)
            self.surface.blit(label, (int(cx + s + 1), int(cy - 5)))
