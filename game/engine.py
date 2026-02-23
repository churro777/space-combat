import math
from game.ship import Ship, ScanResult
from game.projectile import Laser, ScanPulse
from settings import GRID_SIZE, DIRECTIONS


class GameEngine:
    def __init__(self):
        self.player = Ship(x=10, y=GRID_SIZE // 2)
        self.bot = Ship(x=GRID_SIZE - 11, y=GRID_SIZE // 2)
        self.lasers: list[Laser] = []
        self.scan_pulses: list[ScanPulse] = []
        self.turn = 0
        self.game_over = False
        self.winner: str | None = None

    def resolve_turn(self, player_action: dict, bot_action: dict):
        if self.game_over:
            return

        self.turn += 1

        # 1. Apply new actions (simultaneous)
        self._apply_action(self.player, player_action, "player")
        self._apply_action(self.bot, bot_action, "bot")

        # Clamp positions to grid
        self._clamp_ship(self.player)
        self._clamp_ship(self.bot)

        # 2. Advance existing lasers
        laser_trails: list[tuple[Laser, list[tuple[int, int]]]] = []
        for laser in self.lasers:
            tiles = laser.advance()
            laser_trails.append((laser, tiles))

        # 3. Expand all scan pulses (outgoing and returning both expand)
        for pulse in self.scan_pulses:
            pulse.expand()

        # 4. Laser-ship collisions
        for laser, tiles in laser_trails:
            target = self.bot if laser.owner == "player" else self.player
            if target.alive and target.position in tiles:
                target.alive = False

        # 5. Outgoing scan contacts
        # The pulse swept from (old_radius) to (new_radius) this turn.
        # Check if enemy is within that band using Euclidean distance.
        # On contact, remove the outgoing pulse and spawn a new return pulse
        # expanding from the enemy's detected position.
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
                # Spawn return pulse from enemy's position
                new_return_pulses.append(ScanPulse(
                    origin_x=target.x,
                    origin_y=target.y,
                    radius=0,
                    owner=pulse.owner,
                    returning=True,
                    contact_position=target.position,
                    contact_turn=self.turn,
                ))
                self.scan_pulses.remove(pulse)
        self.scan_pulses.extend(new_return_pulses)

        # 6. Returning scan arrivals
        # The return ping is an expanding circle from the enemy's detected position.
        # It delivers when the ring passes over the owner ship's CURRENT position.
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
                    turn_received=self.turn,
                ))
                self.scan_pulses.remove(pulse)

        # 7. Cleanup off-grid objects
        self.lasers = [l for l in self.lasers if l.is_on_grid()]
        self.scan_pulses = [p for p in self.scan_pulses if not p.is_expired()]

        # 8. Win/lose
        if not self.bot.alive and not self.player.alive:
            self.game_over = True
            self.winner = "draw"
        elif not self.bot.alive:
            self.game_over = True
            self.winner = "player"
        elif not self.player.alive:
            self.game_over = True
            self.winner = "bot"

    def _apply_action(self, ship: Ship, action: dict, owner: str):
        if not ship.alive:
            return
        kind = action.get("type")
        if kind == "move":
            dx, dy = action["direction"]
            if (dx, dy) != (0, 0):
                ship.facing = (dx, dy)
            ship.x += dx
            ship.y += dy
        elif kind == "fire":
            dx, dy = ship.facing
            self.lasers.append(Laser(x=ship.x, y=ship.y, dx=dx, dy=dy, owner=owner))
        elif kind == "scan":
            self.scan_pulses.append(ScanPulse(
                origin_x=ship.x, origin_y=ship.y, radius=0, owner=owner
            ))

    def _clamp_ship(self, ship: Ship):
        ship.x = max(0, min(GRID_SIZE - 1, ship.x))
        ship.y = max(0, min(GRID_SIZE - 1, ship.y))
