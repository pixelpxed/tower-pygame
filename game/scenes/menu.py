import pygame

from game.settings import COLORS, HEIGHT, WIDTH
from ui.button import Button
from ui.text import draw_text


class MenuScene:
    def __init__(self, game):
        self.game = game
        self.start = Button((WIDTH // 2 - 110, HEIGHT // 2, 220, 54), "Start Tower", self._start)
        self.quit = Button((WIDTH // 2 - 110, HEIGHT // 2 + 72, 220, 54), "Quit", self.game.quit)

    def _start(self):
        self.game.new_run()

    def handle_event(self, event):
        self.start.handle_event(event)
        self.quit.handle_event(event)

    def draw(self, screen):
        screen.fill(COLORS["background"])
        draw_text(screen, "TOWER GAME", (WIDTH // 2, 150), 52, COLORS["accent"], center=True)
        draw_text(screen, "Climb the tower. Defeat every monster.", (WIDTH // 2, 220), 22, COLORS["muted"], center=True)
        self.start.draw(screen)
        self.quit.draw(screen)
