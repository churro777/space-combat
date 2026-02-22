import sys
import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
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

    engine = GameEngine()
    bot = Bot()
    renderer = Renderer(screen)
    hud = HUD(screen)
    input_handler = InputHandler(hud)

    hud.show_message("Select an action: Scan(S) Move(M) Fire(F)", 180)

    running = True
    while running:
        clock.tick(FPS)

        quit_game, player_action, restart = input_handler.process_events()

        if quit_game:
            running = False
            continue

        if restart:
            engine = GameEngine()
            bot = Bot()
            hud.selected_action = None
            hud.show_message("New game! Select an action.", 120)
            continue

        if player_action and not engine.game_over:
            bot_action = bot.choose_action(engine.bot, engine.turn)
            engine.resolve_turn(player_action, bot_action)
            hud.show_message(f"Turn {engine.turn} resolved.", 60)

        renderer.draw(engine)
        hud.draw(engine)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
