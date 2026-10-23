import pygame

from game.settings import COLORS, HEIGHT, WIDTH
from ui.button import Button
from ui.text import draw_text


class TowerScene:
    def __init__(self, game):
        self.game = game
        self.enter = Button((WIDTH // 2 - 120, 470, 240, 54), "Enter Floor", game.start_battle)
        self.menu = Button((WIDTH // 2 - 120, 540, 240, 44), "Main Menu", game.show_menu)

    def handle_event(self, event):
        self.enter.handle_event(event)
        self.menu.handle_event(event)

    def draw(self, screen):
        screen.fill(COLORS["background"])
        player = self.game.player
        draw_text(screen, f"Floor {player.floor}", (WIDTH // 2, 100), 42, COLORS["accent"], center=True)
        draw_text(screen, f"{player.name}  |  HP {player.health}/{player.max_health}  |  Gold {player.gold}",
                  (WIDTH // 2, 170), 22, COLORS["text"], center=True)
        draw_text(screen, "Rest between battles, then continue your climb.", (WIDTH // 2, 250), 22,
                  COLORS["muted"], center=True)
        self.enter.draw(screen)
        self.menu.draw(screen)
