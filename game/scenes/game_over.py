from game.settings import COLORS, HEIGHT, WIDTH
from ui.button import Button
from ui.text import draw_text


class GameOverScene:
    def __init__(self, game):
        self.game = game
        self.restart = Button((WIDTH // 2 - 120, 420, 240, 54), "Try Again", game.new_run)
        self.menu = Button((WIDTH // 2 - 120, 490, 240, 44), "Main Menu", game.show_menu)

    def handle_event(self, event):
        self.restart.handle_event(event)
        self.menu.handle_event(event)

    def draw(self, screen):
        screen.fill(COLORS["background"])
        won = self.game.won
        draw_text(screen, "TOWER CLEARED!" if won else "GAME OVER", (WIDTH // 2, 180), 48,
                  COLORS["success"] if won else COLORS["danger"], center=True)
        draw_text(screen, self.game.message, (WIDTH // 2, 280), 22, COLORS["text"], center=True)
        self.restart.draw(screen)
        self.menu.draw(screen)
