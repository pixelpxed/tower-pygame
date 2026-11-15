import json
from pathlib import Path

import pygame

from game.scenes.battle import load_background
from game.settings import COLORS, HEIGHT, WIDTH
from ui.battle_kub import HomeButton, draw_hearts, draw_power
from ui.text import draw_text

TOWER_WIDTH = 130
GAP = 22
BOTTOM = 650
FLOOR_HEIGHT = 54
PLAYER_IMAGE_SIZE = (42, 42)
ENEMY_IMAGE_SIZE = (42, 42)
BONK_DELAY_MS = 320


class TowerScene:
    def __init__(self, game):
        self.game = game
        self.bg_image = load_background((WIDTH, HEIGHT))
        self.menu = HomeButton((WIDTH // 2, 24 + 32), game.show_menu)  # top-center
        root = Path(__file__).resolve().parents[2]
        self.player_frames, self.player_durations = self._load_animation(
            root / "assets" / "player",
            PLAYER_IMAGE_SIZE,
        )
        self.enemy_frames, self.enemy_durations = self._load_animation(
            root / "assets" / "enemy",
            ENEMY_IMAGE_SIZE,
        )
        self.player_frame_index = 0
        self.player_frame_timer = 0
        self.attacking = False
        self.player_won = True
        self.bonk_delay = None
        self.player_image = self.player_frames[0]
        self.enemy_image = self.enemy_frames[0]
        self.enemy_attack_image = self.enemy_image
        items_dir = root / "assets" / "items"
        self.enemy_item_images = {
            "stick": self._load_item(items_dir / "stick.png", ENEMY_IMAGE_SIZE),
            "lightsaber": self._load_item(
                items_dir / "lightsaber-enemy.png",
                ENEMY_IMAGE_SIZE,
            ),
        }
        self.player_item_images = {
            "stick": self._load_item(items_dir / "stick.png", PLAYER_IMAGE_SIZE),
            "lightsaber": self._load_item(
                items_dir / "lightsaber-player.png",
                PLAYER_IMAGE_SIZE,
            ),
        }

    @staticmethod
    def _load_animation(asset_dir, image_size):
        with (asset_dir / "attack.json").open(encoding="utf-8") as file:
            animation_data = json.load(file)

        sheet = pygame.image.load(asset_dir / animation_data["sheet"]).convert_alpha()
        frame_width = animation_data["frame_width"]
        frame_height = animation_data["frame_height"]
        frames = [
            pygame.transform.scale(
                sheet.subsurface(
                    (frame["index"] * frame_width, 0, frame_width, frame_height)
                ).copy(),
                image_size,
            )
            for frame in animation_data["frames"]
        ]
        durations = [frame["duration_ms"] for frame in animation_data["frames"]]
        return frames, durations

    @staticmethod
    def _load_item(path, image_size):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, image_size)

    def handle_event(self, event):
        if not self.attacking and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for tower_index, floor_index, rect in self._floor_rects():
                if rect.collidepoint(event.pos):
                    self.game.select_enemy(tower_index, floor_index)
                    break
        self.menu.handle_event(event)

    def start_attack(self, player_won):
        if self.attacking:
            return
        self.attacking = True
        self.player_won = player_won
        self.bonk_delay = BONK_DELAY_MS if player_won else None
        self.player_frame_index = 0
        self.player_frame_timer = 0
        self.player_image = self.player_frames[0]
        self.enemy_attack_image = self.enemy_frames[0]

    def update(self, dt_ms):
        if not self.attacking:
            return

        if self.bonk_delay is not None:
            self.bonk_delay -= dt_ms
            if self.bonk_delay <= 0:
                self.game.play_sound("bonk.mp3")
                self.bonk_delay = None

        frames = self.player_frames if self.player_won else self.enemy_frames
        durations = self.player_durations if self.player_won else self.enemy_durations
        self.player_frame_timer += dt_ms
        while self.player_frame_timer >= durations[self.player_frame_index]:
            self.player_frame_timer -= durations[self.player_frame_index]
            if self.player_frame_index + 1 == len(frames):
                self.attacking = False
                self.player_image = self.player_frames[0]
                self.enemy_attack_image = self.enemy_frames[0]
                self.game.player_attack()
                return
            self.player_frame_index += 1
            if self.player_won:
                self.player_image = frames[self.player_frame_index]
            else:
                self.enemy_attack_image = frames[self.player_frame_index]

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

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
        player = self.game.player

        self._draw_hud(screen, player)
        self._draw_towers(screen)
        if self.game.message:
            status_rect = pygame.Rect(120, HEIGHT - 72, WIDTH - 240, 48)
            navy = (20, 35, 80)
            pygame.draw.rect(screen, (255, 255, 255), status_rect, border_radius=8)
            pygame.draw.rect(screen, navy, status_rect, 3, border_radius=8)
            draw_text(
                screen,
                self.game.message,
                status_rect.center,
                16,
                navy,
                center=True,
            )
        self.menu.draw(screen)

    @staticmethod
    def _draw_hud(screen, player):
        margin = 24
        draw_hearts(screen, player.lives, 3, (margin, margin),
                    max_hearts=3)

        draw_power(screen, (WIDTH - margin, margin), player.power)
        draw_text(screen, f"Item: {player.item or 'None'}  |  Damage: {player.doable_damage:g}",
                  (WIDTH - 180, 105), 20, COLORS["text"], center=True)

    def _draw_towers(self, screen):
        player = self.game.player
        towers = self.game.tower.towers
        left = self._left()

        pygame.draw.line(
            screen,
            COLORS["muted"],
            (left - 70, BOTTOM + 2),
            (left + len(towers) * (TOWER_WIDTH + GAP) - GAP + 70, BOTTOM + 2),
            3,
        )

        for tower_index, tower in enumerate(towers):
            x = left + tower_index * (TOWER_WIDTH + GAP)
            floors = tower["floors"]
            height = len(floors) * FLOOR_HEIGHT
            top = BOTTOM - height
            active = tower_index == player.tower

            tower_color = COLORS["accent"] if active else COLORS["muted"]
            pygame.draw.rect(screen, (20, 14, 50), (x, top, TOWER_WIDTH, height))
            pygame.draw.rect(screen, tower_color, (x, top, TOWER_WIDTH, height), 3)
            self._draw_tower_top(screen, x, top, tower_color)

            for floor_index, floor in enumerate(floors):
                y = BOTTOM - (floor_index + 1) * FLOOR_HEIGHT
                enemy_id = (tower_index, floor_index)
                conquered = enemy_id in self.game.defeated
                selectable = active and not conquered
                current = (tower_index, floor_index) == player.position
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
                draw_text(
                    screen,
                    str(floor["monster"]["power"]),
                    (x + 10, y + 8),
                    14,
                    COLORS["text"],
                )

                enemy_image = (
                    self.enemy_attack_image
                    if current and self.attacking and not self.player_won
                    else self.enemy_image
                )
                screen.blit(
                    enemy_image,
                    enemy_image.get_rect(
                        midright=(x + TOWER_WIDTH - 8, y + FLOOR_HEIGHT // 2)
                    ),
                )
                enemy_item = self.enemy_item_images.get(floor["monster"]["item"])
                if enemy_item is not None:
                    screen.blit(
                        enemy_item,
                        enemy_item.get_rect(
                            midright=(x + TOWER_WIDTH - 8, y + FLOOR_HEIGHT // 2)
                        ),
                    )
                if current:
                    screen.blit(
                        self.player_image,
                        self.player_image.get_rect(
                            midleft=(x + 8, y + FLOOR_HEIGHT // 2)
                        ),
                    )
                    player_item = self.player_item_images.get(player.item)
                    if player_item is not None:
                        screen.blit(
                            player_item,
                            player_item.get_rect(
                                midleft=(x + 8, y + FLOOR_HEIGHT // 2)
                            ),
                        )

    @staticmethod
    def _draw_tower_top(screen, x, top, color):
        crenel_width = 16
        crenel_height = 9
        for offset in (8, 8 + crenel_width * 2, 8 + crenel_width * 4):
            pygame.draw.rect(
                screen,
                (20, 14, 50),
                (x + offset, top - crenel_height, crenel_width, crenel_height),
            )
            pygame.draw.rect(
                screen,
                color,
                (x + offset, top - crenel_height, crenel_width, crenel_height),
                3,
            )
