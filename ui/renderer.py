import math
import random
import pygame
from settings import (
    GRID_SIZE, TILE_SIZE, COLOR_BG, COLOR_GRID, COLOR_PLAYER, COLOR_ENEMY,
    COLOR_LASER_P, COLOR_LASER_E, COLOR_SCAN_OUT, COLOR_SCAN_RET,
    COLOR_SCAN_MARK, COLOR_WHITE, MISSILE_BLAST_RADIUS, LASER_VISIBLE_RANGE,
)

HALF = TILE_SIZE / 2

SHIP_FLAME_COLORS = [
    (255, 255, 200),
    (255, 220, 80),
    (255, 160, 30),
    (255, 80, 20),
    (255, 40, 10),
]

MISSILE_FLAME_COLORS = [
    (200, 255, 200),
    (100, 255, 100),
    (60, 200, 60),
    (30, 160, 30),
    (20, 120, 20),
]


class _Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "max_life", "color", "size")

    def __init__(self, x: float, y: float, palette=None, speed_range=(20, 100), size_range=(2, 5), life_range=(0.6, 1.5)):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(*speed_range)
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.uniform(*life_range)
        self.max_life = self.life
        self.color = random.choice(palette or SHIP_FLAME_COLORS)
        self.size = random.uniform(*size_range)


class Renderer:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.font = pygame.font.SysFont("monospace", 10)
        self.debug = False
        self._particles: list[_Particle] = []
        self._known_explosion_count = 0

    def draw(self, engine, dt: float = 0.016):
        # Spawn particles for any new explosions
        while self._known_explosion_count < len(engine.explosions):
            ex, ey, _, etype = engine.explosions[self._known_explosion_count]
            cx = ex * TILE_SIZE + HALF
            cy = ey * TILE_SIZE + HALF
            if etype == "missile":
                blast_px = MISSILE_BLAST_RADIUS * TILE_SIZE
                for _ in range(80):
                    self._particles.append(_Particle(
                        cx, cy,
                        palette=MISSILE_FLAME_COLORS,
                        speed_range=(40, blast_px / 1.0),
                        size_range=(3, 7),
                        life_range=(0.8, 2.0),
                    ))
            else:
                for _ in range(30):
                    self._particles.append(_Particle(cx, cy, palette=SHIP_FLAME_COLORS))
            self._known_explosion_count += 1

        # Update particles
        alive = []
        for p in self._particles:
            p.life -= dt
            if p.life > 0:
                p.x += p.vx * dt
                p.y += p.vy * dt
                p.vx *= 0.97  # drag
                p.vy *= 0.97
                alive.append(p)
        self._particles = alive

        self._draw_grid()
        self._draw_scan_pulses(engine)
        self._draw_lasers(engine)
        self._draw_missiles(engine)
        self._draw_scan_markers(engine.player, engine.tick_count)
        self._draw_ship(engine.player, COLOR_PLAYER)
        if engine.player.shield and engine.player.alive:
            self._draw_shield(engine.player)
        if self.debug:
            self._draw_ship(engine.bot, COLOR_ENEMY)
            if engine.bot.shield and engine.bot.alive:
                self._draw_shield(engine.bot)
        self._draw_particles()

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

    def _draw_shield(self, ship):
        cx = int(ship.x * TILE_SIZE + HALF)
        cy = int(ship.y * TILE_SIZE + HALF)
        radius = max(TILE_SIZE // 2, 4) + 3
        pygame.draw.circle(self.surface, (80, 150, 255), (cx, cy), radius, 1)

    def _draw_particles(self):
        for p in self._particles:
            t = p.life / p.max_life  # 1.0 → 0.0
            alpha = max(0, min(255, int(255 * t)))
            r, g, b = p.color
            size = max(1, int(p.size * t))
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (r, g, b, alpha), (size, size), size)
            self.surface.blit(surf, (int(p.x) - size, int(p.y) - size))

    def reset(self):
        self._particles.clear()
        self._known_explosion_count = 0

    def _draw_lasers(self, engine):
        for laser in engine.lasers:
            if laser.owner != "player" and not self.debug:
                dx = laser.x - engine.player.x
                dy = laser.y - engine.player.y
                if dx * dx + dy * dy > LASER_VISIBLE_RANGE * LASER_VISIBLE_RANGE:
                    continue
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

    def _draw_missiles(self, engine):
        """Draw player missiles always, enemy missiles only in debug mode."""
        for missile in engine.missiles:
            if missile.owner != "player" and not self.debug:
                continue
            cx = missile.x * TILE_SIZE + HALF
            cy = missile.y * TILE_SIZE + HALF
            pygame.draw.circle(self.surface, COLOR_PLAYER, (int(cx), int(cy)), max(3, TILE_SIZE // 2))
            # Small cross to distinguish from lasers
            s = 2
            pygame.draw.line(self.surface, COLOR_WHITE, (int(cx - s), int(cy)), (int(cx + s), int(cy)), 1)
            pygame.draw.line(self.surface, COLOR_WHITE, (int(cx), int(cy - s)), (int(cx), int(cy + s)), 1)

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
