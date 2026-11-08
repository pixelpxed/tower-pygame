import pygame

from game.scenes.battle import load_background
from game.settings import COLORS, HEIGHT, WIDTH
from ui.battle_kub import HomeButton, draw_hearts, draw_power
from ui.text import draw_text

TOWER_WIDTH = 190
GAP = 25
BOTTOM = 440
FLOOR_HEIGHT = 48


class TowerScene:
    def __init__(self, game):
        self.game = game
        self.bg_image = load_background((WIDTH, HEIGHT))
        self.menu = HomeButton((WIDTH // 2, 24 + 32), game.show_menu)  # top-center

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for tower_index, floor_index, rect in self._floor_rects():
                if rect.collidepoint(event.pos):
                    self.game.select_enemy(tower_index, floor_index)
                    break
        self.menu.handle_event(event)

    # ------------------------------------------------------------ layout
    def _left(self):
        count = len(self.game.tower.towers)
        return (WIDTH - (count * TOWER_WIDTH + (count - 1) * GAP)) // 2

    def _floor_rects(self):
        rects = []
        for tower_index, tower in enumerate(self.game.tower.towers):
            x = self._left() + tower_index * (TOWER_WIDTH + GAP)
            for floor_index in range(len(tower["floors"])):
                y = BOTTOM - (floor_index + 1) * FLOOR_HEIGHT
                rects.append((tower_index, floor_index,
                              pygame.Rect(x, y, TOWER_WIDTH, FLOOR_HEIGHT)))
        return rects

    # ------------------------------------------------------------- draw
    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
        player = self.game.player

        self._draw_hud(screen, player)
        if self.game.message:
            draw_text(screen, self.game.message, (WIDTH // 2, 230), 16, COLORS["text"], center=True)

        self._draw_towers(screen)
        self.menu.draw(screen)

    @staticmethod
    def _draw_hud(screen, player):
        margin = 24
        draw_hearts(screen, player.lives, player.max_lives, (margin, margin),
                    max_hearts=player.max_lives)

        draw_power(screen, (WIDTH - margin, margin), getattr(player, "attack", None))

    def _draw_towers(self, screen):
        player = self.game.player
        towers = self.game.tower.towers
        left = self._left()

        for tower_index, tower in enumerate(towers):
            x = left + tower_index * (TOWER_WIDTH + GAP)
            floors = tower["floors"]
            height = len(floors) * FLOOR_HEIGHT
            top = BOTTOM - height
            active = tower_index == player.tower

            draw_text(screen, tower["name"], (x + TOWER_WIDTH // 2, BOTTOM + 28), 20,
                      COLORS["accent"] if active else COLORS["muted"], center=True)

            # translucent panel so the background shows through
            panel = pygame.Surface((TOWER_WIDTH, height), pygame.SRCALPHA)
            pygame.draw.rect(panel, (20, 14, 50, 205), panel.get_rect(), border_radius=8)
            screen.blit(panel, (x, top))
            pygame.draw.rect(screen, COLORS["accent"] if active else COLORS["muted"],
                             (x, top, TOWER_WIDTH, height), 2, border_radius=8)

            for floor_index, floor in enumerate(floors):
                y = BOTTOM - (floor_index + 1) * FLOOR_HEIGHT
                enemy_id = (tower_index, floor_index)
                conquered = enemy_id in self.game.defeated
                selectable = active and not conquered
                current = (tower_index == player.location_tower and
                           floor_index + 1 == player.location_floor)
                color = (COLORS["success"] if conquered
                         else COLORS["accent"] if selectable else COLORS["muted"])

                if conquered:
                    tint = pygame.Surface((TOWER_WIDTH - 4, FLOOR_HEIGHT - 2), pygame.SRCALPHA)
                    tint.fill((60, 200, 110, 45))
                    screen.blit(tint, (x + 2, y + 1))
                if selectable:
                    pygame.draw.rect(screen, COLORS["accent"],
                                     (x + 3, y + 3, TOWER_WIDTH - 6, FLOOR_HEIGHT - 6), 1,
                                     border_radius=4)
                if floor_index > 0:
                    pygame.draw.line(screen, COLORS["muted"], (x + 6, y + FLOOR_HEIGHT),
                                     (x + TOWER_WIDTH - 6, y + FLOOR_HEIGHT), 1)

                label = f"{floor_index + 1}. {floor['monster']['name']}"
                draw_text(screen, label, (x + 10, y + FLOOR_HEIGHT // 2 - 8), 16, color)
                if current:
                    draw_text(screen, "YOU", (x + TOWER_WIDTH - 32, y + FLOOR_HEIGHT // 2 - 8), 13,
                              COLORS["text"], center=True)