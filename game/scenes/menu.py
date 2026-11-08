import pygame

from game.scenes.cut_scene import CutScene
from game.settings import COLORS, HEIGHT, WIDTH
from ui.button import Button
from ui.text import draw_text


class MenuScene:
    def __init__(self, game):
        self.game = game
        self.bg_image = pygame.image.load("game/scenes/Menu_bg.jpg").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))

        button_width = 400
        button_height = 100
        button_x = (WIDTH // 2) - (button_width // 2) + 60
        button_y = HEIGHT // 2 - 120

        self.start = Button((button_x, button_y, button_width, button_height), "S T A R T", self._start)
        self.quit = Button((button_x, button_y + button_height + 50, button_width, button_height), "G I V E    U P", self.game.quit)

    def _start(self):
        # Start -> cut scene (GIF, 3 s, SKIP button) -> game.new_run()
        self.game.scene = CutScene(self.game)

    def handle_event(self, event):
        self.start.handle_event(event)
        self.quit.handle_event(event)

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
        self.start.draw(screen)
        self.quit.draw(screen)