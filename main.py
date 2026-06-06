import asyncio
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
import settings as settings_module
from ui.touch_input import TouchInput
from ui.mobile_hud import MobileHUD

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
    pygame.joystick.quit()
    pygame.event.clear()

    pygame.joystick.init()
    count = pygame.joystick.get_count()
    for i in range(count):
        try:
            js = pygame.joystick.Joystick(i)
            js.init()
            js.get_name()
            pygame.event.clear()
            return js
        except (pygame.error, SystemError, KeyError):
            continue

    pygame.joystick.quit()
    pygame.event.clear()
    return None


def _detect_mobile() -> bool:
    try:
        from platform import window
        return window.navigator.maxTouchPoints > 0
    except (ImportError, AttributeError):
        pass
    info = pygame.display.Info()
    return info.current_w < 1100


def _get_viewport_size():
    """Get actual browser viewport size via JS. Falls back to pygame display info."""
    try:
        from platform import window
        return int(window.innerWidth), int(window.innerHeight)
    except (ImportError, AttributeError):
        info = pygame.display.Info()
        return info.current_w, info.current_h


def _resize_canvas(w, h):
    """Resize the Pygbag HTML canvas to match viewport."""
    try:
        from platform import window
        canvas = window.document.getElementById("canvas")
        if canvas:
            canvas.width = w
            canvas.height = h
            canvas.style.width = f"{w}px"
            canvas.style.height = f"{h}px"
    except (ImportError, AttributeError):
        pass


async def title_screen(screen, clock, joystick, mobile=False):
    title_font = pygame.font.SysFont("monospace", 52, bold=True)
    prompt_font = pygame.font.SysFont("monospace", 18)
    sub_font = pygame.font.SysFont("monospace", 14)

    sw, sh = screen.get_size()
    rotate_font = pygame.font.SysFont("monospace", 28, bold=True)
    rotate_sub_font = pygame.font.SysFont("monospace", 16)

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
                if event.button == 6:
                    return True
            elif event.type == pygame.FINGERDOWN:
                if mobile and sw >= sh:
                    return True

        clock.tick(FPS)
        frame += 1

        # Poll viewport size each frame on mobile (handles rotation)
        if mobile:
            vw, vh = _get_viewport_size()
            if (vw, vh) != (sw, sh):
                sw, sh = vw, vh
                _resize_canvas(sw, sh)
                screen = pygame.display.set_mode((sw, sh))

        screen.fill(COLOR_BG)

        if mobile and sw < sh:
            msg = rotate_font.render("Rotate Device", True, COLOR_WHITE)
            sub = rotate_sub_font.render("Landscape mode required", True, (150, 150, 180))
            screen.blit(msg, msg.get_rect(center=(sw // 2, sh // 2 - 20)))
            screen.blit(sub, sub.get_rect(center=(sw // 2, sh // 2 + 20)))
            pygame.display.flip()
            await asyncio.sleep(0)
            continue

        title = title_font.render("SPACE COMBAT", True, (0, 200, 255))
        title_rect = title.get_rect(center=(sw // 2, sh // 3))
        screen.blit(title, title_rect)

        sub = sub_font.render("Relativistic Warfare", True, (100, 100, 180))
        sub_rect = sub.get_rect(center=(sw // 2, sh // 3 + 45))
        screen.blit(sub, sub_rect)

        if (frame // 40) % 2 == 0:
            if mobile:
                prompt = prompt_font.render("Tap to start", True, COLOR_WHITE)
            else:
                prompt = prompt_font.render("Press ENTER to start", True, COLOR_WHITE)
            prompt_rect = prompt.get_rect(center=(sw // 2, sh * 2 // 3))
            screen.blit(prompt, prompt_rect)

        if not mobile:
            if joystick:
                ctrl_text = f"Controller: {joystick.get_name()}"
                ctrl_color = (0, 200, 100)
            else:
                ctrl_text = "No controller detected"
                ctrl_color = (120, 120, 120)
            ctrl_surf = sub_font.render(ctrl_text, True, ctrl_color)
            ctrl_rect = ctrl_surf.get_rect(center=(sw // 2, sh - 40))
            screen.blit(ctrl_surf, ctrl_rect)

        pygame.display.flip()
        await asyncio.sleep(0)


async def main():
    pygame.init()
    mobile = _detect_mobile()
    settings_module.MOBILE = mobile

    if mobile:
        screen_w, screen_h = _get_viewport_size()
        _resize_canvas(screen_w, screen_h)
        screen = pygame.display.set_mode((screen_w, screen_h))
    else:
        screen_w, screen_h = WINDOW_WIDTH, WINDOW_HEIGHT
        screen = pygame.display.set_mode((screen_w, screen_h))

    pygame.display.set_caption("Space Combat v2 — Relativistic Warfare")
    clock = pygame.time.Clock()

    sound_manager = SoundManager()
    joystick = _init_joystick()

    sound_manager.play_music_intro()

    if not await title_screen(screen, clock, joystick, mobile):
        pygame.quit()
        return

    sound_manager.transition_to_game()

    # Re-query viewport after title screen (may have rotated)
    if mobile:
        screen_w, screen_h = _get_viewport_size()
        _resize_canvas(screen_w, screen_h)
        screen = pygame.display.set_mode((screen_w, screen_h))

    bot = Bot()
    engine = GameEngine(bot)
    renderer = Renderer(screen)
    if mobile:
        touch_controls = TouchInput(screen_w, screen_h)
        hud = MobileHUD(screen)
    else:
        touch_controls = None
        hud = HUD(screen)

    input_handler = InputHandler(hud, renderer, joystick, touch_controls=touch_controls)

    if mobile:
        hud.show_message("Joystick:move  Buttons:fire/scan/missile", 180)
    else:
        hud.show_message("WASD:move  Space:fire  F:scan", 180)

    tick_interval = 1.0 / TICK_RATE
    tick_accumulator = 0.0

    rotate_font = pygame.font.SysFont("monospace", 28, bold=True)
    rotate_sub = pygame.font.SysFont("monospace", 16)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        tick_accumulator += dt

        # Poll viewport size on mobile (handles rotation)
        if mobile:
            vw, vh = _get_viewport_size()
            if (vw, vh) != (screen_w, screen_h):
                screen_w, screen_h = vw, vh
                _resize_canvas(screen_w, screen_h)
                screen = pygame.display.set_mode((screen_w, screen_h))
                renderer = Renderer(screen)
                touch_controls = TouchInput(screen_w, screen_h)
                hud = MobileHUD(screen)
                input_handler = InputHandler(hud, renderer, joystick, touch_controls=touch_controls)

        quit_game, restart = input_handler.process_events()

        if mobile and screen_w < screen_h:
            screen.fill(COLOR_BG)
            msg = rotate_font.render("Rotate Device", True, COLOR_WHITE)
            sub = rotate_sub.render("Landscape mode required", True, (150, 150, 180))
            screen.blit(msg, msg.get_rect(center=(screen_w // 2, screen_h // 2 - 20)))
            screen.blit(sub, sub.get_rect(center=(screen_w // 2, screen_h // 2 + 20)))
            pygame.display.flip()
            await asyncio.sleep(0)
            continue

        if mobile and engine.game_over and input_handler._touch_tapped:
            restart = True
            input_handler._touch_tapped = False

        if quit_game:
            running = False
            continue

        if restart:
            bot = Bot()
            engine = GameEngine(bot)
            renderer.reset()
            tick_accumulator = 0.0
            sound_manager.transition_to_game()
            hud.show_message("New game!", 120)
            if hasattr(input_handler, '_touch_tapped'):
                input_handler._touch_tapped = False
            continue

        while tick_accumulator >= tick_interval:
            tick_accumulator -= tick_interval
            if not engine.game_over:
                direction, fire, scan, missile = input_handler.get_continuous_state()
                engine.tick(direction, fire, scan, missile)
                for event in engine.events:
                    sound_manager.play(event)

        renderer.draw(engine, dt)
        if mobile and touch_controls:
            touch_controls.draw(screen)
        hud.draw(engine)
        if mobile and engine.game_over:
            grid_w = screen_w
            grid_h = screen_h - settings_module.MOBILE_HUD_HEIGHT
            hud.draw_game_over(engine, grid_w, grid_h)
        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())
