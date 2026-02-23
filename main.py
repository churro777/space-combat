import sys
import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TICK_RATE
from game.engine import GameEngine
from game.bot import Bot
from ui.renderer import Renderer
from ui.hud import HUD
from ui.input_handler import InputHandler


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Space Combat v2 — Relativistic Warfare")
    clock = pygame.time.Clock()

    bot = Bot()
    engine = GameEngine(bot)
    renderer = Renderer(screen)
    hud = HUD(screen)
    input_handler = InputHandler(hud, renderer)

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
            tick_accumulator = 0.0
            hud.show_message("New game!", 120)
            continue

        # Run ticks
        while tick_accumulator >= tick_interval:
            tick_accumulator -= tick_interval
            if not engine.game_over:
                direction, fire, scan = input_handler.get_continuous_state()
                engine.tick(direction, fire, scan)

        renderer.draw(engine)
        hud.draw(engine)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
