import pygame


def draw_text(screen, text, position, size, color, center=False):
    font = pygame.font.Font(None, size)
    surface = font.render(str(text), True, color)
    rect = surface.get_rect()
    rect.center = position if center else rect.center
    if not center:
        rect.topleft = position
    screen.blit(surface, rect)
