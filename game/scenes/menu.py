import pygame
from pathlib import Path
from game.settings import COLORS, HEIGHT, WIDTH
from ui.button import Button


class MenuScene:
    def __init__(self, game):
        self.game = game
        self.bg_image = pygame.image.load("game/scenes/image/Menu_bg.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))
        self.play_music()

        button_width = 400
        button_height = 100
        button_x = (WIDTH // 2) - (button_width // 2) + 295
        button_y = HEIGHT // 2

        self.start = Button((button_x, button_y, button_width, button_height), "S T A R T", self.start)
        self.quit = Button((button_x, button_y + button_height + 30, button_width, button_height), "Q U I T",
                           self.game.quit)

    def play_music(self):
        music_path = Path("game/scenes/soundeffect/soundback_home.mp3")
        pygame.mixer.music.load(str(music_path))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def start(self):
        pygame.mixer.music.stop()
        self.game.new_run()

    def handle_event(self, event):
        self.start.handle_event(event)
        self.quit.handle_event(event)

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
        self.start.draw(screen)
        self.quit.draw(screen)