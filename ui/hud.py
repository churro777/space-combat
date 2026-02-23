import pygame
from settings import (
    GRID_SIZE, TILE_SIZE, SIDEBAR_WIDTH, WINDOW_HEIGHT,
    COLOR_HUD_BG, COLOR_HUD_TEXT, COLOR_WHITE, COLOR_PLAYER,
)

GRID_PX = GRID_SIZE * TILE_SIZE
BTN_X = GRID_PX + 20

DIR_NAMES = {
    (0, -1): "N", (1, -1): "NE", (1, 0): "E", (1, 1): "SE",
    (0, 1): "S", (-1, 1): "SW", (-1, 0): "W", (-1, -1): "NW",
}


class HUD:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.font = pygame.font.SysFont("monospace", 15)
        self.small_font = pygame.font.SysFont("monospace", 12)
        self.message: str | None = None
        self.message_timer = 0

    def draw(self, engine):
        # Sidebar background
        self.surface.fill(COLOR_HUD_BG, (GRID_PX, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT))

        y = 10

        # Turn counter
        self.surface.blit(self.font.render(f"Turn: {engine.turn}", True, COLOR_WHITE), (BTN_X, y))
        y += 28

        # Facing direction
        facing_name = DIR_NAMES.get(engine.player.facing, "?")
        self.surface.blit(self.font.render(f"Facing: {facing_name}", True, COLOR_PLAYER), (BTN_X, y))
        y += 28

        # Position
        self.surface.blit(self.font.render(f"Pos: {engine.player.position}", True, COLOR_HUD_TEXT), (BTN_X, y))
        y += 36

        # Controls
        controls = [
            "Controls:",
            "WASD/Arrows  Move",
            "Space        Fire",
            "F            Scan",
            "",
            "R  Restart",
            "Q  Quit",
            "`  Debug",
        ]
        for line in controls:
            self.surface.blit(self.small_font.render(line, True, COLOR_HUD_TEXT), (BTN_X, y))
            y += 16

        # Scan history
        y += 12
        self._draw_scan_history(engine, y)

        # Flash message
        if self.message and self.message_timer > 0:
            msg = self.font.render(self.message, True, COLOR_WHITE)
            self.surface.blit(msg, (BTN_X, WINDOW_HEIGHT - 30))
            self.message_timer -= 1

        # Game over overlay
        if engine.game_over:
            self._draw_game_over(engine)

    def _draw_scan_history(self, engine, y):
        header = self.font.render("Scan History:", True, COLOR_HUD_TEXT)
        self.surface.blit(header, (BTN_X, y))
        y += 20
        results = engine.player.scan_results[-8:]
        for r in reversed(results):
            staleness = r.turn_received - r.turn_detected
            text = self.small_font.render(
                f"T{r.turn_received}: @{r.enemy_position} d:{staleness}",
                True, COLOR_HUD_TEXT,
            )
            self.surface.blit(text, (BTN_X, y))
            y += 16

    def _draw_game_over(self, engine):
        overlay = pygame.Surface((GRID_PX, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.surface.blit(overlay, (0, 0))
        if engine.winner == "player":
            text = "YOU WIN!"
            color = (0, 255, 100)
        elif engine.winner == "bot":
            text = "YOU LOSE"
            color = (255, 60, 60)
        else:
            text = "DRAW"
            color = (200, 200, 0)
        big_font = pygame.font.SysFont("monospace", 48, bold=True)
        label = big_font.render(text, True, color)
        rect = label.get_rect(center=(GRID_PX // 2, WINDOW_HEIGHT // 2))
        self.surface.blit(label, rect)
        sub = self.font.render("Press R to restart or Q to quit", True, COLOR_WHITE)
        sub_rect = sub.get_rect(center=(GRID_PX // 2, WINDOW_HEIGHT // 2 + 50))
        self.surface.blit(sub, sub_rect)

    def show_message(self, msg: str, duration: int = 90):
        self.message = msg
        self.message_timer = duration
