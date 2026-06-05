import pygame
from settings import (
    COLOR_HUD_BG, COLOR_HUD_TEXT, COLOR_WHITE, COLOR_PLAYER,
    FIRE_COOLDOWN, SCAN_COOLDOWN, MISSILE_COOLDOWN, MISSILE_AMMO,
    MOBILE_HUD_HEIGHT,
)

DIR_NAMES = {
    (0, -1): "N", (1, -1): "NE", (1, 0): "E", (1, 1): "SE",
    (0, 1): "S", (-1, 1): "SW", (-1, 0): "W", (-1, -1): "NW",
}


class MobileHUD:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.font = pygame.font.SysFont("monospace", 13)
        self.small_font = pygame.font.SysFont("monospace", 11)
        self.message: str | None = None
        self.message_timer = 0

    def draw(self, engine) -> None:
        """Draw the top bar HUD."""
        screen_w = self.surface.get_width()
        p = engine.player
        tick = engine.tick_count

        pygame.draw.rect(self.surface, COLOR_HUD_BG, (0, 0, screen_w, MOBILE_HUD_HEIGHT))

        bar_cy = MOBILE_HUD_HEIGHT // 2

        # --- Left group ---
        x = 10
        if p.shield:
            shield_surf = self.font.render("SHIELD", True, (80, 150, 255))
        elif p.alive and (tick % 10 < 5):
            secs = p.shield_recharge / 10.0
            shield_surf = self.font.render(f"SHLD {secs:.1f}s", True, (255, 60, 60))
        else:
            shield_surf = None

        if shield_surf:
            self.surface.blit(shield_surf, shield_surf.get_rect(midleft=(x, bar_cy)))
            x += shield_surf.get_width()

        sep = self.small_font.render(" | ", True, (100, 100, 100))
        self.surface.blit(sep, sep.get_rect(midleft=(x, bar_cy)))
        x += sep.get_width()

        time_surf = self.font.render(f"{tick / 10.0:.1f}s", True, COLOR_WHITE)
        self.surface.blit(time_surf, time_surf.get_rect(midleft=(x, bar_cy)))

        # --- Right group ---
        facing_name = DIR_NAMES.get(tuple(p.facing), "?")
        pos = p.position
        right_text = f"{facing_name} · ({pos[0]},{pos[1]})"
        right_surf = self.font.render(right_text, True, COLOR_HUD_TEXT)
        self.surface.blit(right_surf, right_surf.get_rect(midright=(screen_w - 10, bar_cy)))

        # --- Center group ---
        # Each mini-bar block: label + 35px bar. Three blocks + ammo count.
        # Measure total width to center it.
        label_h = self.small_font.get_height()
        bar_w = 35
        bar_h = 5
        block_w = bar_w  # label can overhang but bar anchors width
        gap = 8
        ammo_text = f"{p.missiles_remaining}/{MISSILE_AMMO}"
        ammo_surf = self.small_font.render(ammo_text, True, COLOR_HUD_TEXT)

        cooldowns = [
            ("FIR", p.fire_cooldown, FIRE_COOLDOWN),
            ("SCN", p.scan_cooldown, SCAN_COOLDOWN),
            ("MSL", p.missile_cooldown, MISSILE_COOLDOWN),
        ]

        label_surfs = [self.small_font.render(lbl, True, COLOR_HUD_TEXT) for lbl, _, _ in cooldowns]
        # Total width: 3 bars + 2 gaps + small gap + ammo
        total_w = 3 * bar_w + 2 * gap + 4 + ammo_surf.get_width()
        cx_start = (screen_w - total_w) // 2

        x = cx_start
        for i, (lbl, current, maximum) in enumerate(cooldowns):
            lbl_surf = label_surfs[i]
            # Center label over bar
            lbl_x = x + (bar_w - lbl_surf.get_width()) // 2
            lbl_y = bar_cy - label_h // 2 - 1
            self.surface.blit(lbl_surf, (lbl_x, lbl_y))

            bar_y = bar_cy + 2
            pygame.draw.rect(self.surface, (40, 40, 60), (x, bar_y, bar_w, bar_h))
            ready = current == 0
            fill = bar_w if ready else int(bar_w * (1 - current / maximum))
            bar_color = (0, 200, 100) if ready else (200, 100, 0)
            if fill > 0:
                pygame.draw.rect(self.surface, bar_color, (x, bar_y, fill, bar_h))

            x += bar_w + gap

        # Ammo count after the 3 bars (remove one gap already added by loop end)
        x -= gap
        x += 4
        self.surface.blit(ammo_surf, ammo_surf.get_rect(midleft=(x, bar_cy)))

        # --- Flash message ---
        if self.message and self.message_timer > 0:
            grid_h = self.surface.get_height() - MOBILE_HUD_HEIGHT
            msg_surf = self.font.render(self.message, True, COLOR_WHITE)
            msg_rect = msg_surf.get_rect(center=(screen_w // 2, MOBILE_HUD_HEIGHT + grid_h - 30))
            self.surface.blit(msg_surf, msg_rect)
            self.message_timer -= 1

    def draw_game_over(self, engine, grid_w: int, grid_h: int) -> None:
        """Game over overlay on the grid area."""
        overlay = pygame.Surface((grid_w, grid_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.surface.blit(overlay, (0, MOBILE_HUD_HEIGHT))

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
        center_x = grid_w // 2
        center_y = MOBILE_HUD_HEIGHT + grid_h // 2
        label_rect = label.get_rect(center=(center_x, center_y))
        self.surface.blit(label, label_rect)

        sub = self.font.render("TAP TO PLAY AGAIN", True, COLOR_WHITE)
        sub_rect = sub.get_rect(center=(center_x, center_y + 50))
        self.surface.blit(sub, sub_rect)

    def show_message(self, msg: str, duration: int = 90) -> None:
        self.message = msg
        self.message_timer = duration
