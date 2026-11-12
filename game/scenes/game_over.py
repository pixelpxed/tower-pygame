import math
from pathlib import Path
import pygame

from game.settings import COLORS, HEIGHT, WIDTH
from ui.battle_kub import HomeButton
from ui.text import draw_text
from game.scenes.cut_scene import CutScene

HERE = Path(__file__).resolve().parent
BLACK = (15, 15, 20)


def _load_bg(*names):
    for name in names:
        for path in (HERE / name,
                     HERE.parents[1] / "assets" / "images" / name,
                     HERE.parents[1] / name,
                     Path("game/scenes") / name):
            if path.exists():
                return pygame.transform.scale(pygame.image.load(str(path)).convert(), (WIDTH, HEIGHT))
    print(f"[game_over] {names[0]} not found. Using a plain background.")
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.fill((14, 18, 40))
    return surf


class RestartButton:
    def __init__(self, center, callback, size=96):
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = center
        self.callback = callback

    def handle_event(self, event):
        if (event.type == pygame.MOUSEBUTTONUP and event.button == 1
                and self.rect.collidepoint(event.pos)):
            self.callback()

    def draw(self, surf):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        cx, cy = self.rect.center
        rad = self.rect.w // 2
        pygame.draw.circle(surf, (255, 250, 215) if hover else (255, 255, 255), (cx, cy), rad)
        if hover:
            pygame.draw.circle(surf, (0, 200, 60), (cx, cy), rad, 4)

        r = self.rect.w * 0.2
        dot = max(2, self.rect.w // 28)
        for deg in range(30, 301, 4):
            a = math.radians(deg)
            pygame.draw.circle(surf, BLACK, (round(cx + r * math.cos(a)), round(cy + r * math.sin(a))), dot)

        a = math.radians(300)
        px, py = cx + r * math.cos(a), cy + r * math.sin(a)
        nx, ny = math.cos(a), math.sin(a)
        tx, ty = -math.sin(a), math.cos(a)
        h = self.rect.w * 0.13
        pygame.draw.polygon(surf, BLACK, [
            (px + tx * h * 1.3, py + ty * h * 1.3),
            (px + nx * h - tx * h * 0.2, py + ny * h - ty * h * 0.2),
            (px - nx * h - tx * h * 0.2, py - ny * h - ty * h * 0.2),
        ])


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

        if game.won:
            self.bg = _load_bg("VICTORY.jpg")
            self.buttons = [HomeButton((WIDTH // 2, y), go_home_with_cutscene, size=size)]
        else:
            self.bg = _load_bg("DEFEATED.jpg")
            offset = size // 2 + 25
            self.buttons = [
                RestartButton((WIDTH // 2 - offset, y), game.new_run, size=size),
                HomeButton((WIDTH // 2 + offset, y), game.show_menu, size=size),
            ]

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        draw_text(screen, "Victory!" if self.game.won else "Game Over",
                  (WIDTH // 2, 160), 48, COLORS["text"], center=True)
        draw_text(screen, self.game.message, (WIDTH // 2, 220), 20, COLORS["text"], center=True)
        for button in self.buttons:
            button.draw(screen)