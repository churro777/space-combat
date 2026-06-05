import math
import pygame
from settings import MOBILE_HUD_HEIGHT

# Sector index → (dx, dy) for 8 directions, starting from East, going CCW
# atan2(-dy, dx) gives angle where 0=E, pi/2=N (screen y flipped)
_SECTORS = [
    (1, 0),   # 0: E
    (1, -1),  # 1: NE
    (0, -1),  # 2: N
    (-1, -1), # 3: NW
    (-1, 0),  # 4: W
    (-1, 1),  # 5: SW
    (0, 1),   # 6: S
    (1, 1),   # 7: SE
]


class TouchInput:
    def __init__(self, screen_w: int, screen_h: int):
        self._sw = screen_w
        self._sh = screen_h

        self._joy_radius = screen_h * 0.09
        self._dead_zone = screen_h * 0.015

        # Joystick state
        self._joy_finger = None
        self._joy_ox = 0.0
        self._joy_oy = 0.0
        self._joy_cx = 0.0   # current finger x (pixel)
        self._joy_cy = 0.0   # current finger y (pixel)
        self._joy_dir = None  # (dx, dy) or None

        # Button definitions: (cx, cy, radius)
        self._btn_fire = (
            screen_w - screen_h * 0.1,
            screen_h * 0.75,
            screen_h * 0.07,
        )
        self._btn_scan = (
            screen_w - screen_h * 0.18,
            screen_h * 0.58,
            screen_h * 0.055,
        )
        self._btn_missile = (
            screen_w - screen_h * 0.05,
            screen_h * 0.58,
            screen_h * 0.055,
        )

        # Edge-triggered flags, cleared after get_state()
        self._fire = False
        self._scan = False
        self._missile = False

    # ------------------------------------------------------------------
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.FINGERDOWN:
            px = event.x * self._sw
            py = event.y * self._sh

            # Left zone → joystick (only claim first finger in that zone)
            if self._joy_finger is None and px < self._sw * 0.4 and py > MOBILE_HUD_HEIGHT:
                self._joy_finger = event.finger_id
                self._joy_ox = px
                self._joy_oy = py
                self._joy_cx = px
                self._joy_cy = py
                self._joy_dir = None
                return

            # Right zone → buttons (edge-triggered)
            self._check_buttons(px, py)

        elif event.type == pygame.FINGERMOTION:
            if event.finger_id == self._joy_finger:
                px = event.x * self._sw
                py = event.y * self._sh
                self._joy_cx = px
                self._joy_cy = py
                self._joy_dir = self._compute_direction(px, py)

        elif event.type == pygame.FINGERUP:
            if event.finger_id == self._joy_finger:
                self._joy_finger = None
                self._joy_dir = None

    def _compute_direction(self, px: float, py: float) -> tuple[int, int] | None:
        dx = px - self._joy_ox
        dy = py - self._joy_oy
        dist = math.hypot(dx, dy)
        if dist < self._dead_zone:
            return None
        angle = math.atan2(-dy, dx)  # negate dy: screen y grows downward
        sector_idx = round(angle / (math.pi / 4)) % 8
        return _SECTORS[sector_idx]

    def _check_buttons(self, px: float, py: float) -> None:
        cx, cy, r = self._btn_fire
        if math.hypot(px - cx, py - cy) <= r:
            self._fire = True
            return
        cx, cy, r = self._btn_scan
        if math.hypot(px - cx, py - cy) <= r:
            self._scan = True
            return
        cx, cy, r = self._btn_missile
        if math.hypot(px - cx, py - cy) <= r:
            self._missile = True

    # ------------------------------------------------------------------
    def get_state(self) -> tuple[tuple[int, int] | None, bool, bool, bool]:
        result = (self._joy_dir, self._fire, self._scan, self._missile)
        self._fire = False
        self._scan = False
        self._missile = False
        return result

    # ------------------------------------------------------------------
    def draw(self, surface: pygame.Surface) -> None:
        self._draw_buttons(surface)
        if self._joy_finger is not None:
            self._draw_joystick(surface)

    def _draw_joystick(self, surface: pygame.Surface) -> None:
        r = int(self._joy_radius)
        ox, oy = int(self._joy_ox), int(self._joy_oy)

        # Base circle
        base_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(base_surf, (0, 220, 220, 50), (r, r), r)
        pygame.draw.circle(base_surf, (0, 220, 220, 120), (r, r), r, 2)
        surface.blit(base_surf, (ox - r, oy - r))

        # Thumb dot clamped to joy_radius
        dx = self._joy_cx - self._joy_ox
        dy = self._joy_cy - self._joy_oy
        dist = math.hypot(dx, dy)
        if dist > self._joy_radius:
            scale = self._joy_radius / dist
            dx *= scale
            dy *= scale
        tx = int(self._joy_ox + dx)
        ty = int(self._joy_oy + dy)
        dot_r = max(8, int(self._joy_radius * 0.35))
        dot_surf = pygame.Surface((dot_r * 2, dot_r * 2), pygame.SRCALPHA)
        pygame.draw.circle(dot_surf, (0, 220, 220, 180), (dot_r, dot_r), dot_r)
        surface.blit(dot_surf, (tx - dot_r, ty - dot_r))

    def _draw_buttons(self, surface: pygame.Surface) -> None:
        font = pygame.font.SysFont(None, max(12, int(self._sh * 0.028)))
        buttons = [
            (self._btn_fire,    (255, 60,  60,  80), "FIRE"),
            (self._btn_scan,    (255, 200, 0,   80), "SCAN"),
            (self._btn_missile, (0,   255, 200, 80), "MSL"),
        ]
        for (cx, cy, r), color, label in buttons:
            ir = int(r)
            btn_surf = pygame.Surface((ir * 2, ir * 2), pygame.SRCALPHA)
            pygame.draw.circle(btn_surf, color, (ir, ir), ir)
            pygame.draw.circle(btn_surf, (color[0], color[1], color[2], 180), (ir, ir), ir, 2)
            surface.blit(btn_surf, (int(cx) - ir, int(cy) - ir))

            text_surf = font.render(label, True, (255, 255, 255))
            text_surf.set_alpha(200)
            tr = text_surf.get_rect(center=(int(cx), int(cy)))
            surface.blit(text_surf, tr)
