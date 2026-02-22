import pygame


class InputHandler:
    def __init__(self, hud):
        self.hud = hud

    def process_events(self) -> tuple[bool, dict | None, bool]:
        """Process pygame events. Returns (quit, action_or_none, restart)."""
        action = None
        restart = False
        quit_game = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit_game = True
                elif event.key == pygame.K_r:
                    restart = True
                else:
                    result = self.hud.handle_key(event.key)
                    if result and action is None:
                        action = result
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                result = self.hud.handle_click(event.pos)
                if result and action is None:
                    action = result

        return quit_game, action, restart
