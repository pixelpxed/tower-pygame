import pygame

from game.settings import COLORS, HEIGHT, WIDTH
from ui.button import Button
from ui.hud import draw_bar
from ui.text import draw_text


class BattleScene:
    def __init__(self, game):
        self.game = game
        self.attack = Button((WIDTH // 2 - 120, 500, 240, 54), "Attack", game.player_attack)
        self.potion = Button((WIDTH // 2 - 120, 565, 240, 40), "Use Potion", game.use_potion)

    def handle_event(self, event):
        self.attack.handle_event(event)
        self.potion.handle_event(event)

    def draw(self, screen):
        screen.fill(COLORS["background"])
        player, monster = self.game.player, self.game.monster
        draw_text(screen, f"Floor {player.floor}: {monster.name}", (WIDTH // 2, 75), 36, COLORS["accent"], center=True)
        draw_text(screen, player.name, (220, 170), 26, COLORS["text"], center=True)
        draw_text(screen, monster.name, (740, 170), 26, COLORS["text"], center=True)
        draw_bar(screen, (100, 220, 240, 22), player.health, player.max_health, COLORS["success"])
        draw_bar(screen, (620, 220, 240, 22), monster.health, monster.max_health, COLORS["danger"])
        draw_text(screen, self.game.message, (WIDTH // 2, 390), 20, COLORS["muted"], center=True)
        self.attack.draw(screen)
        self.potion.draw(screen)
