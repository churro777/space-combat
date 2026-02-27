import sys
import math
import pygame
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TICK_RATE, GRID_SIZE, TILE_SIZE,
    COLOR_BG, COLOR_WHITE,
)
from game.engine import GameEngine
from game.bot import Bot
from ui.renderer import Renderer
from ui.hud import HUD
from ui.input_handler import InputHandler
from audio.manager import SoundManager

GRID_PX = GRID_SIZE * TILE_SIZE


def _safe_event_get():
    """Wrapper around pygame.event.get() that handles joystick-poisoned queues."""
    try:
        return pygame.event.get()
    except (SystemError, KeyError):
        pygame.event.clear()
        return []


def _init_joystick():
    """Detect and initialize the first available joystick. Returns joystick or None."""
    # pygame.init() already inited joystick — quit it and flush any poisoned events
    pygame.joystick.quit()
    pygame.event.clear()

    # Re-init and try each joystick until one works
    pygame.joystick.init()
    count = pygame.joystick.get_count()
    for i in range(count):
        try:
            js = pygame.joystick.Joystick(i)
            js.init()
            js.get_name()
            # Flush any bad events from init
            pygame.event.clear()
            return js
        except (pygame.error, SystemError, KeyError):
            continue

    # No working joystick — disable subsystem
    pygame.joystick.quit()
    pygame.event.clear()
    return None


def title_screen(screen, clock, joystick):
    title_font = pygame.font.SysFont("monospace", 52, bold=True)
    prompt_font = pygame.font.SysFont("monospace", 18)
    sub_font = pygame.font.SysFont("monospace", 14)

    frame = 0
    while True:
        for event in _safe_event_get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    return True
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 6:  # Start button
                    return True

        clock.tick(FPS)
        frame += 1

        screen.fill(COLOR_BG)

        # Title
        title = title_font.render("SPACE COMBAT", True, (0, 200, 255))
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        screen.blit(title, title_rect)

        # Subtitle
        sub = sub_font.render("Relativistic Warfare", True, (100, 100, 180))
        sub_rect = sub.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 45))
        screen.blit(sub, sub_rect)

        # Blinking prompt
        if (frame // 40) % 2 == 0:
            prompt = prompt_font.render("Press ENTER to start", True, COLOR_WHITE)
            prompt_rect = prompt.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 2 // 3))
            screen.blit(prompt, prompt_rect)

        # Controller status
        if joystick:
            ctrl_text = f"Controller: {joystick.get_name()}"
            ctrl_color = (0, 200, 100)
        else:
            ctrl_text = "No controller detected"
            ctrl_color = (120, 120, 120)
        ctrl_surf = sub_font.render(ctrl_text, True, ctrl_color)
        ctrl_rect = ctrl_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        screen.blit(ctrl_surf, ctrl_rect)

        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Space Combat v2 — Relativistic Warfare")
    clock = pygame.time.Clock()

    sound_manager = SoundManager()
    joystick = _init_joystick()

    if not title_screen(screen, clock, joystick):
        pygame.quit()
        sys.exit()

    bot = Bot()
    engine = GameEngine(bot)
    renderer = Renderer(screen)
    hud = HUD(screen)
    input_handler = InputHandler(hud, renderer, joystick)

    hud.show_message("WASD:move  Space:fire  F:scan", 180)

    tick_interval = 1.0 / TICK_RATE
    tick_accumulator = 0.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        tick_accumulator += dt

        quit_game, restart = input_handler.process_events()

        if quit_game:
            running = False
            continue

        if restart:
            bot = Bot()
            engine = GameEngine(bot)
            renderer.reset()
            tick_accumulator = 0.0
            hud.show_message("New game!", 120)
            continue

        # Run ticks
        while tick_accumulator >= tick_interval:
            tick_accumulator -= tick_interval
            if not engine.game_over:
                direction, fire, scan, missile = input_handler.get_continuous_state()
                engine.tick(direction, fire, scan, missile)
                for event in engine.events:
                    sound_manager.play(event)

        renderer.draw(engine, dt)
        hud.draw(engine)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
