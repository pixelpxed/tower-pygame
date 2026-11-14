from pathlib import Path
import pygame

from game.settings import COLORS, HEIGHT, WIDTH
from ui.battle_kub import BackButton, draw_hearts, draw_power
from ui.button import Button
from ui.hud import draw_bar
from ui.text import draw_text


def load_background(size):
    bg_path = Path("game/scenes/image/battle_bg.png")
    image = pygame.image.load(bg_path).convert()
    return pygame.transform.scale(image, size)


class BattleScene:
    def __init__(self, game):
        self.game = game
        bg_path = Path("game/scenes/image/battle_bg.png")
        image = pygame.image.load(bg_path).convert()
        self.bg_image = pygame.transform.scale(image, (WIDTH, HEIGHT))

        cx = WIDTH // 2
        self.attack = Button((cx - 120, 500, 240, 54), "Attack", game.player_attack)
        self.potion = Button((cx - 120, 565, 240, 48), "Use Potion", game.player_potion)

        # ปุ่มย้อนกลับ กึ่งกลางด้านบน (แถวเดียวกับแถบหัวใจและ POWER)
        k = WIDTH / 1280
        size = round(64 * k)
        self.back = BackButton(
            (WIDTH // 2, round(24 + 34 * k)),
            game.back_to_tower, size=size)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.back_to_tower()
            return
        self.back.handle_event(event)
        self.attack.handle_event(event)
        self.potion.handle_event(event)

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))

        p, m = self.game.player, self.game.monster

        # เลือด และพลัง
        draw_hearts(screen, p.lives, p.max_lives, (24, 24), max_hearts=p.max_lives)
        draw_power(screen, (WIDTH - 24, 24), getattr(p, "attack", None))

        # ชื่อ ชั้น และเลือด
        draw_text(screen, f"{self.game.tower.tower_name(p.tower)} Floor {p.floor}: {m.name}", (WIDTH // 2, 125), 32,
                  COLORS["accent"], center=True)
        draw_text(screen, p.name, (220, 170), 26, COLORS["text"], center=True)
        draw_text(screen, m.name, (740, 170), 26, COLORS["danger"], center=True)

        draw_bar(screen, (100, 220, 240, 22), p.health, p.max_health, COLORS["success"])
        draw_bar(screen, (620, 220, 240, 22), m.health, m.max_health, COLORS["danger"])

        draw_text(screen, self.game.message, (WIDTH // 2, 390), 20, COLORS["muted"], center=True)

        self.back.draw(screen)
        self.attack.draw(screen)
        self.potion.draw(screen)