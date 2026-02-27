import math
from game.ship import Ship, ScanResult
from game.projectile import Laser, ScanPulse, Missile
from game.bot import Bot
from settings import (
    GRID_SIZE, MOVE_COOLDOWN, FIRE_COOLDOWN, SCAN_COOLDOWN, EXPLOSION_DURATION,
    SHIELD_RECHARGE, MISSILE_COOLDOWN, MISSILE_BLAST_RADIUS,
)


class GameEngine:
    def __init__(self, bot_ai: Bot):
        self.player = Ship(x=10, y=GRID_SIZE // 2)
        self.bot = Ship(x=GRID_SIZE - 11, y=GRID_SIZE // 2)
        self.lasers: list[Laser] = []
        self.missiles: list[Missile] = []
        self.scan_pulses: list[ScanPulse] = []
        self.tick_count = 0
        self.explosions: list[tuple[int, int, int, str]] = []  # (x, y, start_tick, type)
        self.events: list[str] = []
        self.game_over = False
        self.winner: str | None = None
        self.bot_ai = bot_ai

    def tick(self, player_direction: tuple[int, int] | None, player_fire: bool, player_scan: bool, player_missile: bool = False):
        if self.game_over:
            return

        self.events.clear()
        self.tick_count += 1

        # Decrement cooldowns
        if self.player.move_cooldown > 0:
            self.player.move_cooldown -= 1
        if self.player.fire_cooldown > 0:
            self.player.fire_cooldown -= 1
        if self.player.scan_cooldown > 0:
            self.player.scan_cooldown -= 1
        if self.bot.move_cooldown > 0:
            self.bot.move_cooldown -= 1
        if self.bot.fire_cooldown > 0:
            self.bot.fire_cooldown -= 1
        if self.bot.scan_cooldown > 0:
            self.bot.scan_cooldown -= 1
        if self.player.missile_cooldown > 0:
            self.player.missile_cooldown -= 1
        if self.bot.missile_cooldown > 0:
            self.bot.missile_cooldown -= 1

        # 1. Apply player actions
        if self.player.alive:
            if player_direction:
                dx, dy = player_direction
                if (dx, dy) != (0, 0):
                    self.player.facing = (dx, dy)
                if self.player.move_cooldown == 0:
                    self.player.x += dx
                    self.player.y += dy
                    self.player.move_cooldown = MOVE_COOLDOWN
            if player_fire and self.player.fire_cooldown == 0:
                dx, dy = self.player.facing
                self.lasers.append(Laser(x=self.player.x, y=self.player.y, dx=dx, dy=dy, owner="player"))
                self.player.fire_cooldown = FIRE_COOLDOWN
                self.events.append("laser_fire")
            if player_scan and self.player.scan_cooldown == 0:
                self.scan_pulses.append(ScanPulse(
                    origin_x=self.player.x, origin_y=self.player.y, radius=0, owner="player"
                ))
                self.player.scan_cooldown = SCAN_COOLDOWN
                self.events.append("scan_pulse")
            if player_missile and self.player.missile_cooldown == 0 and self.player.missiles_remaining > 0 and self.player.scan_results:
                latest = max(self.player.scan_results, key=lambda s: s.turn_received)
                tx, ty = latest.enemy_position
                self.missiles.append(Missile(x=float(self.player.x), y=float(self.player.y), target_x=tx, target_y=ty, owner="player"))
                self.player.missile_cooldown = MISSILE_COOLDOWN
                self.player.missiles_remaining -= 1

        # 2. Apply bot actions
        if self.bot.alive:
            bot_dir, bot_fire, bot_scan, bot_missile = self.bot_ai.choose_action(self.bot, self.tick_count)
            if bot_dir:
                dx, dy = bot_dir
                if (dx, dy) != (0, 0):
                    self.bot.facing = (dx, dy)
                if self.bot.move_cooldown == 0:
                    self.bot.x += dx
                    self.bot.y += dy
                    self.bot.move_cooldown = MOVE_COOLDOWN
            if bot_fire and self.bot.fire_cooldown == 0:
                dx, dy = self.bot.facing
                self.lasers.append(Laser(x=self.bot.x, y=self.bot.y, dx=dx, dy=dy, owner="bot"))
                self.bot.fire_cooldown = FIRE_COOLDOWN
            if bot_scan and self.bot.scan_cooldown == 0:
                self.scan_pulses.append(ScanPulse(
                    origin_x=self.bot.x, origin_y=self.bot.y, radius=0, owner="bot"
                ))
                self.bot.scan_cooldown = SCAN_COOLDOWN
            if bot_missile and self.bot.missile_cooldown == 0 and self.bot.missiles_remaining > 0 and self.bot.scan_results:
                latest = max(self.bot.scan_results, key=lambda s: s.turn_received)
                tx, ty = latest.enemy_position
                self.missiles.append(Missile(x=float(self.bot.x), y=float(self.bot.y), target_x=tx, target_y=ty, owner="bot"))
                self.bot.missile_cooldown = MISSILE_COOLDOWN
                self.bot.missiles_remaining -= 1

        # Clamp positions to grid
        self._clamp_ship(self.player)
        self._clamp_ship(self.bot)

        # 2b. Ship-to-ship collision (both die)
        if self.player.alive and self.bot.alive and self.player.position == self.bot.position:
            for ship in (self.player, self.bot):
                ship.alive = False
                self.explosions.append((ship.x, ship.y, self.tick_count, "ship"))

        # 2c. Advance missiles
        for missile in list(self.missiles):
            if missile.advance():
                self.missiles.remove(missile)
                self.explosions.append((missile.target_x, missile.target_y, self.tick_count, "missile"))
                target = self.bot if missile.owner == "player" else self.player
                if target.alive:
                    dx = target.x - missile.target_x
                    dy = target.y - missile.target_y
                    dist = math.sqrt(dx * dx + dy * dy)
                    if dist <= MISSILE_BLAST_RADIUS:
                        if target.shield:
                            target.shield = False
                            target.shield_recharge = SHIELD_RECHARGE
                        else:
                            target.alive = False
                            self.explosions.append((target.x, target.y, self.tick_count, "ship"))
            elif not missile.is_on_grid():
                self.missiles.remove(missile)

        # 3. Advance existing lasers
        laser_trails: list[tuple[Laser, list[tuple[int, int]]]] = []
        for laser in self.lasers:
            tiles = laser.advance()
            laser_trails.append((laser, tiles))

        # 4. Expand all scan pulses
        for pulse in self.scan_pulses:
            pulse.expand()

        # 5. Shield recharge
        for ship in (self.player, self.bot):
            if ship.alive and not ship.shield and ship.shield_recharge > 0:
                ship.shield_recharge -= 1
                if ship.shield_recharge == 0:
                    ship.shield = True

        # 6. Laser-ship collisions
        for laser, tiles in laser_trails:
            target = self.bot if laser.owner == "player" else self.player
            if target.alive and target.position in tiles:
                if target.shield:
                    target.shield = False
                    target.shield_recharge = SHIELD_RECHARGE
                else:
                    target.alive = False
                    self.explosions.append((target.x, target.y, self.tick_count, "ship"))

        # 6. Outgoing scan contacts
        new_return_pulses = []
        for pulse in list(self.scan_pulses):
            if pulse.returning:
                continue
            target = self.bot if pulse.owner == "player" else self.player
            if not target.alive:
                continue
            dx = target.x - pulse.origin_x
            dy = target.y - pulse.origin_y
            dist = math.sqrt(dx * dx + dy * dy)
            old_radius = pulse.radius - 2
            if old_radius <= dist <= pulse.radius:
                new_return_pulses.append(ScanPulse(
                    origin_x=target.x,
                    origin_y=target.y,
                    radius=0,
                    owner=pulse.owner,
                    returning=True,
                    contact_position=target.position,
                    contact_turn=self.tick_count,
                ))
                self.scan_pulses.remove(pulse)
        self.scan_pulses.extend(new_return_pulses)

        # 7. Returning scan arrivals
        for pulse in list(self.scan_pulses):
            if not pulse.returning or not pulse.contact_position:
                continue
            owner_ship = self.player if pulse.owner == "player" else self.bot
            dx = owner_ship.x - pulse.origin_x
            dy = owner_ship.y - pulse.origin_y
            dist = math.sqrt(dx * dx + dy * dy)
            old_radius = pulse.radius - 2
            if old_radius <= dist <= pulse.radius:
                owner_ship.scan_results.append(ScanResult(
                    enemy_position=pulse.contact_position,
                    turn_detected=pulse.contact_turn,
                    turn_received=self.tick_count,
                ))
                if pulse.owner == "player":
                    self.events.append("scan_contact")
                self.scan_pulses.remove(pulse)

        # 8. Cleanup off-grid objects
        self.lasers = [l for l in self.lasers if l.is_on_grid()]
        self.scan_pulses = [p for p in self.scan_pulses if not p.is_expired()]

        # 9. Win/lose (delayed until explosions finish)
        has_active_explosion = any(
            self.tick_count - t < EXPLOSION_DURATION for _, _, t, _ in self.explosions
        )
        if not has_active_explosion:
            if not self.bot.alive and not self.player.alive:
                self.game_over = True
                self.winner = "draw"
            elif not self.bot.alive:
                self.game_over = True
                self.winner = "player"
            elif not self.player.alive:
                self.game_over = True
                self.winner = "bot"

    def _clamp_ship(self, ship: Ship):
        ship.x = max(0, min(GRID_SIZE - 1, ship.x))
        ship.y = max(0, min(GRID_SIZE - 1, ship.y))
