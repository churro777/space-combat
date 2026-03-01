import math
import random
import pygame
from settings import (
    GRID_SIZE, TILE_SIZE, COLOR_BG, COLOR_GRID, COLOR_PLAYER, COLOR_ENEMY,
    COLOR_LASER_P, COLOR_LASER_E, COLOR_SCAN_OUT, COLOR_SCAN_RET,
    COLOR_SCAN_MARK, COLOR_WHITE, MISSILE_BLAST_RADIUS, LASER_VISIBLE_RANGE,
    VIEWPORT_TILES, VIEWPORT_TILE_PX,
)

GRID_PX = GRID_SIZE * TILE_SIZE  # 700px total grid area
VP_HALF = VIEWPORT_TILE_PX / 2   # half a viewport tile in pixels

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
    __slots__ = ("tx", "ty", "vx", "vy", "life", "max_life", "color", "size")

    def __init__(self, tx: float, ty: float, palette=None, speed_range=(20, 100), size_range=(2, 5), life_range=(0.6, 1.5)):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(*speed_range)
        self.tx = tx   # tile coordinates
        self.ty = ty
        # velocity in tiles/sec (convert from old pixel speed using TILE_SIZE)
        self.vx = math.cos(angle) * speed / TILE_SIZE
        self.vy = math.sin(angle) * speed / TILE_SIZE
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
        # Camera state (top-left tile coordinate of viewport)
        self._cam_tx = 0.0
        self._cam_ty = 0.0

    def _update_camera(self, player):
        """Center camera on player, clamped to grid bounds."""
        half_vp = VIEWPORT_TILES / 2
        self._cam_tx = max(0, min(GRID_SIZE - VIEWPORT_TILES, player.x - half_vp))
        self._cam_ty = max(0, min(GRID_SIZE - VIEWPORT_TILES, player.y - half_vp))

    def _tile_to_screen(self, tx, ty):
        """Convert tile coords to screen pixel coords."""
        sx = (tx - self._cam_tx) * VIEWPORT_TILE_PX
        sy = (ty - self._cam_ty) * VIEWPORT_TILE_PX
        return sx, sy

    def _in_viewport(self, tx, ty, margin=1):
        """Check if a tile coord is within the visible viewport (with margin in tiles)."""
        return (self._cam_tx - margin <= tx <= self._cam_tx + VIEWPORT_TILES + margin and
                self._cam_ty - margin <= ty <= self._cam_ty + VIEWPORT_TILES + margin)

    def draw(self, engine, dt: float = 0.016):
        self._update_camera(engine.player)

        # Spawn particles for any new explosions
        while self._known_explosion_count < len(engine.explosions):
            ex, ey, _, etype = engine.explosions[self._known_explosion_count]
            if etype == "missile":
                blast_tiles = MISSILE_BLAST_RADIUS
                for _ in range(80):
                    self._particles.append(_Particle(
                        ex + 0.5, ey + 0.5,
                        palette=MISSILE_FLAME_COLORS,
                        speed_range=(40, blast_tiles * TILE_SIZE / 1.0),
                        size_range=(3, 7),
                        life_range=(0.8, 2.0),
                    ))
            else:
                for _ in range(30):
                    self._particles.append(_Particle(ex + 0.5, ey + 0.5, palette=SHIP_FLAME_COLORS))
            self._known_explosion_count += 1

        # Update particles (in tile space)
        alive = []
        for p in self._particles:
            p.life -= dt
            if p.life > 0:
                p.tx += p.vx * dt
                p.ty += p.vy * dt
                p.vx *= 0.97
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
        self.surface.fill(COLOR_BG, (0, 0, GRID_PX, GRID_PX))
        # Draw grid lines for the visible area
        # Determine which tile lines are visible
        start_tx = int(self._cam_tx)
        end_tx = int(self._cam_tx + VIEWPORT_TILES) + 1
        start_ty = int(self._cam_ty)
        end_ty = int(self._cam_ty + VIEWPORT_TILES) + 1
        step = 5  # draw every 5th grid line for cleaner look at this scale
        for i in range(start_tx, min(end_tx + 1, GRID_SIZE + 1)):
            if i % step != 0:
                continue
            sx, _ = self._tile_to_screen(i, 0)
            sx = int(sx)
            if 0 <= sx <= GRID_PX:
                pygame.draw.line(self.surface, COLOR_GRID, (sx, 0), (sx, GRID_PX))
        for j in range(start_ty, min(end_ty + 1, GRID_SIZE + 1)):
            if j % step != 0:
                continue
            _, sy = self._tile_to_screen(0, j)
            sy = int(sy)
            if 0 <= sy <= GRID_PX:
                pygame.draw.line(self.surface, COLOR_GRID, (0, sy), (GRID_PX, sy))

    def _draw_ship(self, ship, color):
        if not ship.alive:
            return
        if not self._in_viewport(ship.x, ship.y, margin=2):
            return
        sx, sy = self._tile_to_screen(ship.x + 0.5, ship.y + 0.5)
        r = VIEWPORT_TILE_PX * 0.45
        fdx, fdy = ship.facing
        angle = math.atan2(-fdy, fdx)
        points = []
        for a in [0, 2.4, -2.4]:
            px = sx + r * math.cos(angle + a)
            py = sy - r * math.sin(angle + a)
            points.append((px, py))
        pygame.draw.polygon(self.surface, color, points)

    def _draw_shield(self, ship):
        if not self._in_viewport(ship.x, ship.y, margin=2):
            return
        sx, sy = self._tile_to_screen(ship.x + 0.5, ship.y + 0.5)
        radius = int(VIEWPORT_TILE_PX * 0.55)
        pygame.draw.circle(self.surface, (80, 150, 255), (int(sx), int(sy)), radius, 1)

    def _draw_particles(self):
        scale = VIEWPORT_TILE_PX / TILE_SIZE  # scale factor for particle sizes
        for p in self._particles:
            if not self._in_viewport(p.tx, p.ty, margin=3):
                continue
            t = p.life / p.max_life
            alpha = max(0, min(255, int(255 * t)))
            r, g, b = p.color
            size = max(1, int(p.size * scale * t))
            sx, sy = self._tile_to_screen(p.tx, p.ty)
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (r, g, b, alpha), (size, size), size)
            self.surface.blit(surf, (int(sx) - size, int(sy) - size))

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
            if not self._in_viewport(laser.x, laser.y, margin=3):
                continue
            color = COLOR_LASER_P if laser.owner == "player" else COLOR_LASER_E
            sx, sy = self._tile_to_screen(laser.x + 0.5, laser.y + 0.5)
            dot_r = max(3, int(VIEWPORT_TILE_PX * 0.3))
            pygame.draw.circle(self.surface, color, (int(sx), int(sy)), dot_r)
            # Trail: 2 tiles behind
            tail_sx = sx - laser.dx * VIEWPORT_TILE_PX * 2
            tail_sy = sy - laser.dy * VIEWPORT_TILE_PX * 2
            pygame.draw.line(self.surface, color, (int(tail_sx), int(tail_sy)), (int(sx), int(sy)), 2)

    def _draw_scan_pulses(self, engine):
        if not self.debug:
            return
        for pulse in engine.scan_pulses:
            if pulse.radius <= 0:
                continue
            color = COLOR_PLAYER if pulse.owner == "player" else COLOR_ENEMY
            sx, sy = self._tile_to_screen(pulse.origin_x + 0.5, pulse.origin_y + 0.5)
            pixel_radius = int(pulse.radius * VIEWPORT_TILE_PX)
            if pulse.returning:
                pygame.draw.circle(self.surface, color, (int(sx), int(sy)), pixel_radius, 2)
            else:
                self._draw_dashed_circle(int(sx), int(sy), pixel_radius, color)

    def _draw_dashed_circle(self, cx, cy, radius, color, dash_len=12, gap_len=8):
        if radius < 1:
            return
        circumference = 2 * math.pi * radius
        total = dash_len + gap_len
        segments = max(1, int(circumference / total))
        for i in range(segments):
            start_angle = (i * total / radius)
            end_angle = start_angle + dash_len / radius
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
        for missile in engine.missiles:
            if missile.owner != "player" and not self.debug:
                continue
            if not self._in_viewport(missile.x, missile.y, margin=2):
                continue
            sx, sy = self._tile_to_screen(missile.x + 0.5, missile.y + 0.5)
            dot_r = max(3, int(VIEWPORT_TILE_PX * 0.3))
            pygame.draw.circle(self.surface, COLOR_PLAYER, (int(sx), int(sy)), dot_r)
            s = int(VIEWPORT_TILE_PX * 0.15)
            pygame.draw.line(self.surface, COLOR_WHITE, (int(sx - s), int(sy)), (int(sx + s), int(sy)), 1)
            pygame.draw.line(self.surface, COLOR_WHITE, (int(sx), int(sy - s)), (int(sx), int(sy + s)), 1)

    def _draw_scan_markers(self, player_ship, engine_tick_count):
        from settings import SCAN_MAX_AGE
        alive = [r for r in player_ship.scan_results if engine_tick_count - r.turn_detected <= SCAN_MAX_AGE]
        recent = alive[-10:]
        total = len(recent)
        edge_margin = VIEWPORT_TILE_PX * 0.8  # padding from screen edge for pinned markers
        for i, result in enumerate(recent):
            ex, ey = result.enemy_position
            sx, sy = self._tile_to_screen(ex + 0.5, ey + 0.5)
            on_screen = self._in_viewport(ex, ey, margin=0)

            if on_screen:
                # Normal diamond marker
                s = VIEWPORT_TILE_PX * 0.45
                pygame.draw.polygon(self.surface, COLOR_SCAN_MARK, [
                    (sx, sy - s), (sx + s, sy), (sx, sy + s), (sx - s, sy),
                ], 2)
                rank = total - i
                label = self.font.render(str(rank), True, COLOR_SCAN_MARK)
                self.surface.blit(label, (int(sx + s + 1), int(sy - 5)))
            else:
                # Off-screen: pin to viewport edge in the direction of the marker
                # Clamp to grid area with margin
                cx = max(edge_margin, min(GRID_PX - edge_margin, sx))
                cy = max(edge_margin, min(GRID_PX - edge_margin, sy))
                # Draw a smaller arrow/chevron pointing outward
                s = VIEWPORT_TILE_PX * 0.35
                # Fade based on age
                age_frac = (engine_tick_count - result.turn_detected) / SCAN_MAX_AGE
                alpha = max(80, int(255 * (1.0 - age_frac)))
                color = (COLOR_SCAN_MARK[0], COLOR_SCAN_MARK[1], COLOR_SCAN_MARK[2], alpha)
                # Draw filled diamond at edge
                diamond_surf = pygame.Surface((int(s * 2 + 2), int(s * 2 + 2)), pygame.SRCALPHA)
                ds = s
                dc = ds + 1  # center of the small surface
                pygame.draw.polygon(diamond_surf, color, [
                    (dc, dc - ds), (dc + ds, dc), (dc, dc + ds), (dc - ds, dc),
                ])
                self.surface.blit(diamond_surf, (int(cx - dc), int(cy - dc)))
                rank = total - i
                label_surf = self.font.render(str(rank), True, COLOR_SCAN_MARK)
                self.surface.blit(label_surf, (int(cx + s + 1), int(cy - 5)))
