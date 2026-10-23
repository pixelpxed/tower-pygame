import pygame


def draw_bar(screen, rect, value, maximum, color):
    area = pygame.Rect(rect)
    pygame.draw.rect(screen, (62, 67, 86), area, border_radius=6)
    ratio = max(0.0, min(1.0, value / maximum if maximum else 0.0))
    fill = area.copy()
    fill.width = round(area.width * ratio)
    pygame.draw.rect(screen, color, fill, border_radius=6)
