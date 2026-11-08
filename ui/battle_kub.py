import math

import pygame

WHITE = (255, 255, 255)
BLACK = (15, 15, 20)

# 7x6 pixel heart
HEART = [
    ".XX.XX.",
    "XXXXXXX",
    "XXXXXXX",
    ".XXXXX.",
    "..XXX..",
    "...X...",
]
_CELLS = {(c, r) for r, row in enumerate(HEART) for c, ch in enumerate(row) if ch == "X"}
_BORDER = {
    (c + dc, r + dr)
    for c, r in _CELLS
    for dc in (-1, 0, 1)
    for dr in (-1, 0, 1)
    if (c + dc, r + dr) not in _CELLS
}

_font_cache = {}


def _pixel_text(text, color, size):
    """Render small with no anti-aliasing, then scale up for a blocky pixel look."""
    if "f" not in _font_cache:
        _font_cache["f"] = pygame.font.SysFont(
            "couriernew,consolas,dejavusansmono,monospace", 22, bold=True)
    small = _font_cache["f"].render(text, False, color)
    return pygame.transform.scale(small, size)


def _draw_heart(surf, x, y, cell, full):
    fill = (255, 70, 120) if full else WHITE
    edge = (160, 20, 70) if full else BLACK
    for c, r in _BORDER:
        surf.fill(edge, ((x + (c + 1) * cell), (y + (r + 1) * cell), cell, cell))
    for c, r in _CELLS:
        surf.fill(fill, ((x + (c + 1) * cell), (y + (r + 1) * cell), cell, cell))
    if full:  # small shine
        surf.fill((255, 175, 205), (x + 2 * cell, y + 2 * cell, cell, cell))


def draw_hearts(surf, health, max_health, topleft, max_hearts=3):
    """White pill with hearts; health is converted to 0..max_hearts hearts."""
    k = surf.get_width() / 1280
    cell = max(3, round(5 * k))
    hw, hh = 9 * cell, 8 * cell
    pad, gap = round(20 * k), round(10 * k)
    w = pad * 2 + max_hearts * hw + (max_hearts - 1) * gap
    h = hh + round(28 * k)
    rect = pygame.Rect(topleft, (w, h))
    pygame.draw.rect(surf, WHITE, rect, border_radius=h // 2)

    full = math.ceil(max(0, health) / max(1, max_health) * max_hearts)
    for i in range(max_hearts):
        _draw_heart(surf, rect.x + pad + i * (hw + gap), rect.centery - hh // 2,
                    cell, full=i < full)
    return rect


def draw_power(surf, topright, value=None):
    """White pill with POWER (and optional number in the empty left part)."""
    k = surf.get_width() / 1280
    w, h = round(336 * k), round(72 * k)
    rect = pygame.Rect(0, 0, w, h)
    rect.topright = topright
    pygame.draw.rect(surf, WHITE, rect, border_radius=h // 2)

    label = _pixel_text("POWER", BLACK, (round(210 * k), round(42 * k)))
    surf.blit(label, label.get_rect(midright=(rect.right - round(30 * k), rect.centery)))
    if value is not None:
        num = _pixel_text(str(value), (200, 40, 90), (round(26 * len(str(value)) * k), round(34 * k)))
        surf.blit(num, num.get_rect(midleft=(rect.left + round(34 * k), rect.centery)))
    return rect


# 9x8 pixel house
HOUSE = [
    "....X....",
    "...XXX...",
    "..XXXXX..",
    ".XXXXXXX.",
    "XXXXXXXXX",
    ".XXXXXXX.",
    ".XXX.XXX.",
    ".XXX.XXX.",
]


class HomeButton:
    """Round white button with a pixel house icon (same style as the HUD pills)."""

    def __init__(self, center, callback, size=64):
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = center
        self.callback = callback

    def handle_event(self, event):
        if (event.type == pygame.MOUSEBUTTONUP and event.button == 1
                and self.rect.collidepoint(event.pos)):
            self.callback()

    def draw(self, surf):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.circle(surf, (255, 250, 215) if hover else WHITE,
                           self.rect.center, self.rect.w // 2)
        if hover:
            pygame.draw.circle(surf, (0, 200, 60), self.rect.center, self.rect.w // 2, 4)
        cell = max(3, self.rect.w // 16)
        x0 = self.rect.centerx - len(HOUSE[0]) * cell // 2
        y0 = self.rect.centery - len(HOUSE) * cell // 2
        for r, row in enumerate(HOUSE):
            for c, ch in enumerate(row):
                if ch == "X":
                    surf.fill(BLACK, (x0 + c * cell, y0 + r * cell, cell, cell))


# public alias so other scenes can reuse the blocky pixel text
pixel_text = _pixel_text