import pygame
from settings import (
    GRID_SIZE, TILE_SIZE, SIDEBAR_WIDTH, WINDOW_HEIGHT,
    COLOR_HUD_BG, COLOR_HUD_TEXT, COLOR_BTN, COLOR_BTN_HOVER,
    COLOR_BTN_SEL, COLOR_WHITE, DIRECTIONS,
)

GRID_PX = GRID_SIZE * TILE_SIZE
BTN_W = 220
BTN_H = 36
BTN_X = GRID_PX + 20
DIR_BTN_SIZE = 40


class HUD:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.font = pygame.font.SysFont("monospace", 15)
        self.small_font = pygame.font.SysFont("monospace", 12)
        self.selected_action: str | None = None  # "fire", "move", "scan"
        self.action_buttons = self._make_action_buttons()
        self.dir_buttons = self._make_dir_buttons()
        self.confirm_rect = pygame.Rect(BTN_X, 260, BTN_W, BTN_H)
        self.pending_action: dict | None = None
        self.message: str | None = None
        self.message_timer = 0

    def _make_action_buttons(self) -> list[tuple[pygame.Rect, str]]:
        buttons = []
        labels = ["Scan (S)", "Move (M)", "Fire (F)"]
        keys = ["scan", "move", "fire"]
        for i, (label, key) in enumerate(zip(labels, keys)):
            rect = pygame.Rect(BTN_X, 40 + i * (BTN_H + 6), BTN_W, BTN_H)
            buttons.append((rect, key, label))
        return buttons

    def _make_dir_buttons(self) -> list[tuple[pygame.Rect, str, tuple[int, int]]]:
        # 3x3 grid for 8 directions + center blank
        buttons = []
        positions = {
            "NW": (0, 0), "N": (1, 0), "NE": (2, 0),
            "W":  (0, 1),              "E":  (2, 1),
            "SW": (0, 2), "S": (1, 2), "SE": (2, 2),
        }
        base_x = BTN_X + 50
        base_y = 180
        for name, (dx, dy) in DIRECTIONS.items():
            col, row = positions[name]
            rect = pygame.Rect(
                base_x + col * (DIR_BTN_SIZE + 4),
                base_y + row * (DIR_BTN_SIZE + 4),
                DIR_BTN_SIZE, DIR_BTN_SIZE,
            )
            buttons.append((rect, name, (dx, dy)))
        return buttons

    def draw(self, engine):
        # Sidebar background
        self.surface.fill(COLOR_HUD_BG, (GRID_PX, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT))

        # Turn counter
        turn_text = self.font.render(f"Turn: {engine.turn}", True, COLOR_WHITE)
        self.surface.blit(turn_text, (BTN_X, 10))

        mx, my = pygame.mouse.get_pos()

        # Action buttons
        for rect, key, label in self.action_buttons:
            if self.selected_action == key:
                color = COLOR_BTN_SEL
            elif rect.collidepoint(mx, my):
                color = COLOR_BTN_HOVER
            else:
                color = COLOR_BTN
            pygame.draw.rect(self.surface, color, rect, border_radius=4)
            text = self.font.render(label, True, COLOR_WHITE)
            self.surface.blit(text, (rect.x + 10, rect.y + 9))

        # Direction buttons (when fire or move selected)
        if self.selected_action in ("fire", "move"):
            label = self.font.render(
                "Pick direction:" if self.selected_action == "fire" else "Move direction:",
                True, COLOR_HUD_TEXT,
            )
            self.surface.blit(label, (BTN_X, 164))
            for rect, name, _dir in self.dir_buttons:
                hover = rect.collidepoint(mx, my)
                color = COLOR_BTN_HOVER if hover else COLOR_BTN
                pygame.draw.rect(self.surface, color, rect, border_radius=3)
                text = self.small_font.render(name, True, COLOR_WHITE)
                self.surface.blit(text, (rect.x + 6, rect.y + 12))

        # Scan confirm
        if self.selected_action == "scan":
            label = self.font.render("Press Enter or click:", True, COLOR_HUD_TEXT)
            self.surface.blit(label, (BTN_X, 164))
            hover = self.confirm_rect.collidepoint(mx, my)
            color = COLOR_BTN_HOVER if hover else COLOR_BTN
            pygame.draw.rect(self.surface, color, self.confirm_rect, border_radius=4)
            text = self.font.render("Confirm Scan", True, COLOR_WHITE)
            self.surface.blit(text, (self.confirm_rect.x + 10, self.confirm_rect.y + 9))

        # Scan history
        self._draw_scan_history(engine)

        # Flash message
        if self.message and self.message_timer > 0:
            msg = self.font.render(self.message, True, COLOR_WHITE)
            self.surface.blit(msg, (BTN_X, WINDOW_HEIGHT - 30))
            self.message_timer -= 1

        # Game over overlay
        if engine.game_over:
            self._draw_game_over(engine)

    def _draw_scan_history(self, engine):
        y = 320
        header = self.font.render("Scan History:", True, COLOR_HUD_TEXT)
        self.surface.blit(header, (BTN_X, y))
        y += 20
        results = engine.player.scan_results[-8:]  # show last 8
        for r in reversed(results):
            staleness = r.turn_received - r.turn_detected
            text = self.small_font.render(
                f"T{r.turn_received}: enemy@{r.enemy_position} (delay:{staleness})",
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

    def handle_click(self, pos: tuple[int, int]) -> dict | None:
        """Handle mouse click, return an action dict if one is fully specified."""
        # Check action buttons
        for rect, key, _label in self.action_buttons:
            if rect.collidepoint(pos):
                self.selected_action = key
                if key == "scan":
                    return None  # need confirm
                return None

        # Check direction buttons
        if self.selected_action in ("fire", "move"):
            for rect, _name, direction in self.dir_buttons:
                if rect.collidepoint(pos):
                    action = {"type": self.selected_action, "direction": direction}
                    self.selected_action = None
                    return action

        # Check scan confirm
        if self.selected_action == "scan" and self.confirm_rect.collidepoint(pos):
            self.selected_action = None
            return {"type": "scan"}

        return None

    def handle_key(self, key: int) -> dict | None:
        """Handle keyboard input, return an action dict if one is fully specified."""
        # Action selection shortcuts
        if key == pygame.K_s:
            self.selected_action = "scan"
            return None
        if key == pygame.K_m:
            self.selected_action = "move"
            return None
        if key == pygame.K_f:
            self.selected_action = "fire"
            return None

        # Confirm scan
        if self.selected_action == "scan" and key == pygame.K_RETURN:
            self.selected_action = None
            return {"type": "scan"}

        # Direction keys
        if self.selected_action in ("fire", "move"):
            dir_map = {
                pygame.K_UP: "N", pygame.K_DOWN: "S",
                pygame.K_LEFT: "W", pygame.K_RIGHT: "E",
                pygame.K_KP8: "N", pygame.K_KP2: "S",
                pygame.K_KP4: "W", pygame.K_KP6: "E",
                pygame.K_KP7: "NW", pygame.K_KP9: "NE",
                pygame.K_KP1: "SW", pygame.K_KP3: "SE",
            }
            if key in dir_map:
                from settings import DIRECTIONS
                name = dir_map[key]
                action = {"type": self.selected_action, "direction": DIRECTIONS[name]}
                self.selected_action = None
                return action

        return None
