from pathlib import Path
import pygame

from game.settings import HEIGHT, WIDTH
from ui.battle import HomeButton, draw_hearts
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
        self.fatal = (not game.won) and (not game.player.alive)   # หัวใจหมดแล้ว -> ไป EndLostScene ต่อ
        self.fatal_delay = 2.0                                    # วินาทีที่ค้างหน้า DEFEATED ก่อนไปต่อ
        size = 96
        y = HEIGHT - 100

        def go_home_with_cutscene():
            if hasattr(game, "play_cutscene"):
                game.play_cutscene(on_done=game.show_menu)
            else:
                game.scene = CutScene(game, on_done=game.show_menu)

        bg_filename = "VICTORY.png" if game.won else "DEFEATED.png"
        image_path = Path("game/scenes/image/") / bg_filename

        if image_path.exists():
            image = pygame.image.load(str(image_path)).convert()
            self.bg = pygame.transform.scale(image, (WIDTH, HEIGHT))
        else:
            self.bg = pygame.Surface((WIDTH, HEIGHT))
            self.bg.fill((14, 18, 40))

        if self.fatal:
            self.buttons = []
        elif game.won:
            self.buttons = [
                HomeButton((WIDTH // 2, y), go_home_with_cutscene, size=size)
            ]
        else:
            offset = size // 2 + 25
            self.buttons = [
                # แพ้แล้วกลับไปสู้ตัวเดิม (หัวใจหมดจะเริ่มเกมใหม่เอง)
                RestartButton((WIDTH // 2 - offset, y), game.retry_battle, size=size),
                HomeButton((WIDTH // 2 + offset, y), game.show_menu, size=size),
            ]

    def handle_event(self, event: pygame.event.Event):
        if self.fatal:
            skip = (event.type == pygame.MOUSEBUTTONUP and event.button == 1) or (
                event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_ESCAPE))
            if skip:
                self.game.retry_battle()      # หัวใจหมด -> EndLostScene
            return
        for button in self.buttons:
            button.handle_event(event)

    def update(self, dt: float):
        if self.fatal:
            self.fatal_delay -= dt
            if self.fatal_delay <= 0:
                self.game.retry_battle()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.bg, (0, 0))
        if not self.game.won:
            draw_hearts(screen, self.game.player.lives, 3, (24, 24), max_hearts=3)
        for button in self.buttons:
            button.draw(screen)