from pathlib import Path
import pygame

from game.settings import COLORS, HEIGHT, WIDTH
from ui.battle_kub import draw_hearts, draw_power
from ui.button import Button
from ui.text import draw_text


def load_background(size):
    """ฟังก์ชันโหลดภาพพื้นหลังแบบระบุ Path ตรงๆ"""
    bg_path = Path("game/scenes/battle_bg.png")
    image = pygame.image.load(bg_path).convert()
    return pygame.transform.scale(image, size)


class BattleScene:
    def __init__(self, game):
        self.game = game
        self.bg_image = load_background((WIDTH, HEIGHT))

        self.attack = Button((WIDTH // 2 - 120, 500, 240, 54), "Attack", self.game.player_attack)

    def handle_event(self, event):
        self.attack.handle_event(event)

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))

        player, monster = self.game.player, self.game.monster
        tower_name = self.game.tower.tower_name(player.tower)

        # HUD pills (top-left hearts, top-right POWER)
        margin = 24
        draw_hearts(screen, player.lives, 3, (margin, margin),
                    max_hearts=3)
        draw_power(screen, (WIDTH - margin, margin), player.power)

        draw_text(screen, f"{tower_name} - Floor {(player.position[1] + 1)}: {monster.name}",
                  (WIDTH // 2, 125), 32, COLORS["accent"], center=True)
        draw_text(screen, player.name, (220, 170), 26, COLORS["text"], center=True)
        draw_text(screen, monster.name, (740, 170), 26, COLORS["text"], center=True)

        draw_text(screen, f"Item: {player.item or 'None'}", (220, 220), 22, COLORS["text"], center=True)
        draw_text(screen, f"Doable damage: {player.doable_damage:g}", (220, 255), 22, COLORS["text"], center=True)
        draw_text(screen, f"{monster.kind.title()} power: {monster.power}", (740, 220), 22, COLORS["text"], center=True)
        draw_text(screen, f"Item reward: {monster.item or 'None'}", (740, 255), 22, COLORS["text"], center=True)

        draw_text(screen, self.game.message, (WIDTH // 2, 390), 20, COLORS["muted"], center=True)

        self.attack.draw(screen)
