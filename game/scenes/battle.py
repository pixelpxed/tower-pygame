from pathlib import Path

import pygame

from game.settings import COLORS, HEIGHT, WIDTH
from ui.battle_kub import draw_hearts, draw_power
from ui.button import Button
from ui.hud import draw_bar
from ui.text import draw_text

HERE = Path(__file__).resolve().parent
BG_CANDIDATES = [
    HERE / "battle_bg.png",                                       # game/scenes/
    HERE.parents[1] / "assets" / "images" / "battle_bg.png",      # assets/images/
    HERE.parents[1] / "battle_bg.png",                            # project root
    Path("game/scenes/battle_bg.png"),                            # relative to cwd
]


def load_background(size):
    """Try several locations; fall back to a purple gradient so the game still runs."""
    for path in BG_CANDIDATES:
        if path.exists():
            try:
                return pygame.transform.scale(pygame.image.load(str(path)).convert(), size)
            except pygame.error as err:
                print(f"[battle] found {path} but could not load it: {err}")
    print("[battle] battle_bg.png not found. Tried:")
    for path in BG_CANDIDATES:
        print("   ", path)
    fallback = pygame.Surface(size)
    for y in range(size[1]):
        k = y / size[1]
        fallback.fill((int(20 + 60 * k), int(15 + 30 * k), int(60 + 80 * k)), (0, y, size[0], 1))
    return fallback


class BattleScene:
    def __init__(self, game):
        self.game = game
        self.bg_image = load_background((WIDTH, HEIGHT))

        self.attack = Button((WIDTH // 2 - 120, 500, 240, 54), "Attack", self.game.player_attack)
        self.potion = Button((WIDTH // 2 - 120, 565, 240, 48), "Use Potion", self.game.player_potion)

    def handle_event(self, event):
        self.attack.handle_event(event)
        self.potion.handle_event(event)

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))

        player, monster = self.game.player, self.game.monster
        tower_name = self.game.tower.tower_name(player.tower)

        # HUD pills (top-left hearts, top-right POWER)
        margin = 24
        draw_hearts(screen, player.lives, player.max_lives, (margin, margin),
                    max_hearts=player.max_lives)
        draw_power(screen, (WIDTH - margin, margin), getattr(player, "attack", None))

        draw_text(screen, f"{tower_name} - Floor {player.floor}: {monster.name}",
                  (WIDTH // 2, 125), 32, COLORS["accent"], center=True)
        draw_text(screen, player.name, (220, 170), 26, COLORS["text"], center=True)
        draw_text(screen, monster.name, (740, 170), 26, COLORS["text"], center=True)

        draw_bar(screen, (100, 220, 240, 22), player.health, player.max_health, COLORS["success"])
        draw_bar(screen, (620, 220, 240, 22), monster.health, monster.max_health, COLORS["danger"])

        draw_text(screen, self.game.message, (WIDTH // 2, 390), 20, COLORS["muted"], center=True)

        self.attack.draw(screen)
        self.potion.draw(screen)