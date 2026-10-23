import pygame

from game.settings import COLORS, WIDTH
from ui.button import Button
from ui.text import draw_text


class TowerScene:
    def __init__(self, game):
        self.game = game
        self.menu = Button((WIDTH // 2 - 120, 535, 240, 44), "Main Menu", game.show_menu)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for tower_index, floor_index, rect in self._floor_rects():
                if rect.collidepoint(event.pos):
                    self.game.select_enemy(tower_index, floor_index)
                    break
        self.menu.handle_event(event)

    def draw(self, screen):
        screen.fill(COLORS["background"])
        player = self.game.player
        draw_text(screen, "TOWER MAP", (WIDTH // 2, 45), 34, COLORS["accent"], center=True)
        draw_text(screen, f"{player.name}  |  HP {player.health}/{player.max_health}  |  Gold {player.gold}",
                  (WIDTH // 2, 85), 20, COLORS["text"], center=True)
        draw_text(screen, "Click an enemy to move there and resolve the fight instantly.",
                  (WIDTH // 2, 120), 18,
                  COLORS["muted"], center=True)
        if self.game.message:
            draw_text(screen, self.game.message, (WIDTH // 2, 155), 16, COLORS["text"], center=True)
        self._draw_towers(screen)
        self.menu.draw(screen)

    def _floor_rects(self):
        player = self.game.player
        towers = self.game.tower.towers
        tower_width = 190
        gap = 25
        left = (WIDTH - (len(towers) * tower_width + (len(towers) - 1) * gap)) // 2
        bottom = 440
        floor_height = 48

        rects = []
        for tower_index, tower in enumerate(towers):
            x = left + tower_index * (tower_width + gap)
            floors = tower["floors"]
            for floor_index in range(len(floors)):
                y = bottom - (floor_index + 1) * floor_height
                rects.append((tower_index, floor_index, pygame.Rect(x, y, tower_width, floor_height)))
        return rects

    def _draw_towers(self, screen):
        player = self.game.player
        towers = self.game.tower.towers
        tower_width = 190
        gap = 25
        left = (WIDTH - (len(towers) * tower_width + (len(towers) - 1) * gap)) // 2
        bottom = 440
        floor_height = 48

        for tower_index, tower in enumerate(towers):
            x = left + tower_index * (tower_width + gap)
            floors = tower["floors"]
            draw_text(screen, tower["name"], (x + tower_width // 2, bottom + 28), 20,
                      COLORS["accent"] if tower_index == player.tower else COLORS["muted"], center=True)
            pygame.draw.rect(screen, COLORS["panel"], (x, bottom - len(floors) * floor_height, tower_width,
                                                        len(floors) * floor_height), border_radius=4)
            pygame.draw.rect(screen, COLORS["muted"], (x, bottom - len(floors) * floor_height, tower_width,
                                                        len(floors) * floor_height), 2, border_radius=4)

            for floor_index, floor in enumerate(floors):
                y = bottom - (floor_index + 1) * floor_height
                enemy_id = (tower_index, floor_index)
                conquered = enemy_id in self.game.defeated
                selectable = tower_index == player.tower and not conquered
                current = (tower_index == player.location_tower and
                           floor_index + 1 == player.location_floor)
                color = COLORS["success"] if conquered else COLORS["accent"] if selectable else COLORS["muted"]
                if selectable:
                    pygame.draw.rect(screen, COLORS["accent"], (x + 1, y + 1, tower_width - 2, floor_height - 2), 1)
                pygame.draw.line(screen, COLORS["muted"], (x, y), (x + tower_width, y), 1)
                monster = floor["monster"]
                label = f"{floor_index + 1}. {monster['name']}"
                draw_text(screen, label, (x + 10, y + floor_height // 2 - 8), 16, color)
                if current:
                    draw_text(screen, "YOU", (x + tower_width - 32, y + floor_height // 2 - 8), 13,
                              COLORS["text"], center=True)
