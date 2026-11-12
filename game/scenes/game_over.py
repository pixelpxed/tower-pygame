from pathlib import Path
import pygame

from game.settings import HEIGHT, WIDTH
from ui.battle_kub import HomeButton
from game.scenes.cut_scene import CutScene

BLACK = (15, 15, 20)
class RestartButton:
    def __init__(self, center: tuple, callback, size: int = 96):
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = center
        self.callback = callback

        font = pygame.font.SysFont("segoeuiemoji,dejavusans,arial", int(size * 0.5), bold=True)
        self.icon = font.render("↺", True, BLACK)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def draw(self, surf: pygame.Surface):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        cx, cy = self.rect.center
        rad = self.rect.w // 2
        bg_color = (255, 250, 215) if hover else (255, 255, 255)
        pygame.draw.circle(surf, bg_color, (cx, cy), rad)

        if hover:
            pygame.draw.circle(surf, (0, 200, 60), (cx, cy), rad, 4)
        surf.blit(self.icon, self.icon.get_rect(center=(cx, cy)))

class GameOverScene:
    def __init__(self, game):
        self.game = game
        size = 96
        y = HEIGHT - 100

        def go_home_with_cutscene():
            if hasattr(game, "play_cutscene"):
                game.play_cutscene(on_done=game.show_menu)
            else:
                game.scene = CutScene(game, on_done=game.show_menu)

        bg_filename = "VICTORY.jpg" if game.won else "DEFEATED.jpg"
        image_path = Path("game/scenes/") / bg_filename

        if image_path.exists():
            image = pygame.image.load(str(image_path)).convert()
            self.bg = pygame.transform.scale(image, (WIDTH, HEIGHT))
        else:
            self.bg = pygame.Surface((WIDTH, HEIGHT))
            self.bg.fill((14, 18, 40))

        if game.won:
            self.buttons = [
                HomeButton((WIDTH // 2, y), go_home_with_cutscene, size=size)
            ]
        else:
            offset = size // 2 + 25
            self.buttons = [
                RestartButton((WIDTH // 2 - offset, y), game.new_run, size=size),
                HomeButton((WIDTH // 2 + offset, y), game.show_menu, size=size),
            ]

    def handle_event(self, event: pygame.event.Event):
        for button in self.buttons:
            button.handle_event(event)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.bg, (0, 0))
        for button in self.buttons:
            button.draw(screen)