import pygame

from game.settings import COLORS
from ui.text import draw_text


class Button:
    def __init__(self, rect, label, callback):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.callback = callback

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.rect.collidepoint(event.pos):
            self.callback()

    def draw(self, screen):
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        color = (255, 198, 76) if hovered else COLORS["accent"]
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        draw_text(screen, self.label, self.rect.center, 22, COLORS["background"], center=True)
