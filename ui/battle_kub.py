import math
import pygame

WHITE = (255, 255, 255)
BLACK = (15, 15, 20)
HEART_FILL_COLOR = (255, 70, 120)
HEART_EDGE_COLOR = (160, 20, 70)
HEART_SHINE_COLOR = (255, 175, 205)
POWER_NUM_COLOR = (200, 40, 90)
HOVER_CIRCLE_COLOR = (255, 250, 215)
HOVER_BORDER_COLOR = (0, 200, 60)

HEART = [
    ".XX.XX.",
    "XXXXXXX",
    "XXXXXXX",
    ".XXXXX.",
    "..XXX..",
    "...X...",
]

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

BACK_ARROW = [
    "...X....",
    "..XX....",
    ".XXXXXXX",
    "XXXXXXXX",
    ".XXXXXXX",
    "..XX....",
    "...X....",
]


def pixel_text(text: str, color: tuple, size: tuple) -> pygame.Surface:
    font = pygame.font.SysFont("couriernew,consolas,dejavusansmono,monospace", 22, bold=True)
    small = font.render(text, False, color)
    return pygame.transform.scale(small, size)

_CELLS = {(c, r) for r, row in enumerate(HEART) for c, ch in enumerate(row) if ch == "X"}
_BORDER = {
    (c + dc, r + dr)
    for c, r in _CELLS
    for dc in (-1, 0, 1)
    for dr in (-1, 0, 1)
    if (c + dc, r + dr) not in _CELLS
}

_font_cache = {}

def _draw_heart(surf: pygame.Surface, x: int, y: int, cell: int, full: bool):
    #หัวใจ
    fill = HEART_FILL_COLOR if full else WHITE
    edge = HEART_EDGE_COLOR if full else BLACK

    #ขอบ
    for c, r in _BORDER:
        surf.fill(edge, ((x + (c + 1) * cell), (y + (r + 1) * cell), cell, cell))

    #หวใจ
    for c, r in _CELLS:
        surf.fill(fill, ((x + (c + 1) * cell), (y + (r + 1) * cell), cell, cell))

    if full:
        surf.fill(HEART_SHINE_COLOR, (x + 2 * cell, y + 2 * cell, cell, cell))


def draw_hearts(surf: pygame.Surface, health: float, max_health: float, topleft: tuple,
                max_hearts: int = 3) -> pygame.Rect:
    k = surf.get_width() / 1280
    cell = max(3, round(5 * k))

    hw = 9 * cell
    hh = 8 * cell
    pad = round(20 * k)
    gap = round(10 * k)

    w = pad * 2 + max_hearts * hw + (max_hearts - 1) * gap
    h = hh + round(28 * k)

    rect = pygame.Rect(topleft, (w, h))
    pygame.draw.rect(surf, WHITE, rect, border_radius=h // 2)

    #จน.หัวใจ
    full = math.ceil(max(0, health) / max(1, max_health) * max_hearts)
    for i in range(max_hearts):
        hx = rect.x + pad + i * (hw + gap)
        hy = rect.centery - hh // 2
        _draw_heart(surf, hx, hy, cell, full=(i < full))
    return rect


def draw_power(surf: pygame.Surface, topright: tuple, value: int = None) -> pygame.Rect:
    #Powarrrrr
    k = surf.get_width() / 1280
    w = round(336 * k)
    h = round(72 * k)

    rect = pygame.Rect(0, 0, w, h)
    rect.topright = topright
    pygame.draw.rect(surf, WHITE, rect, border_radius=h // 2)

    # วาดข้อความคำว่า "POWER"
    label_w = round(210 * k)
    label_h = round(42 * k)
    label = pixel_text("POWER", BLACK, (label_w, label_h))
    surf.blit(label, label.get_rect(midright=(rect.right - round(30 * k), rect.centery)))

    # ค่าพลัง
    if value is not None:
        num_str = str(value)
        num_w = round(26 * len(num_str) * k)
        num_h = round(34 * k)
        num = pixel_text(num_str, POWER_NUM_COLOR, (num_w, num_h))
        surf.blit(num, num.get_rect(midleft=(rect.left + round(34 * k), rect.centery)))

    return rect


class HomeButton:
    def __init__(self, center: tuple, callback, size: int = 64):
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = center
        self.callback = callback

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def draw(self, surf: pygame.Surface):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        bg_color = HOVER_CIRCLE_COLOR if hover else WHITE
        pygame.draw.circle(surf, bg_color, self.rect.center, self.rect.w // 2)

        if hover:
            pygame.draw.circle(surf, HOVER_BORDER_COLOR, self.rect.center, self.rect.w // 2, 4)

        cell = max(3, self.rect.w // 16)
        x0 = self.rect.centerx - len(HOUSE[0]) * cell // 2
        y0 = self.rect.centery - len(HOUSE) * cell // 2

        for r, row in enumerate(HOUSE):
            for c, ch in enumerate(row):
                if ch == "X":
                    surf.fill(BLACK, (x0 + c * cell, y0 + r * cell, cell, cell))


class BackButton:
    """ปุ่มวงกลมลูกศรย้อนกลับ สไตล์เดียวกับ HomeButton"""

    def __init__(self, center: tuple, callback, size: int = 64):
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = center
        self.callback = callback

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def draw(self, surf: pygame.Surface):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        bg_color = HOVER_CIRCLE_COLOR if hover else WHITE
        pygame.draw.circle(surf, bg_color, self.rect.center, self.rect.w // 2)

        if hover:
            pygame.draw.circle(surf, HOVER_BORDER_COLOR, self.rect.center, self.rect.w // 2, 4)

        cell = max(3, self.rect.w // 14)
        x0 = self.rect.centerx - len(BACK_ARROW[0]) * cell // 2
        y0 = self.rect.centery - len(BACK_ARROW) * cell // 2

        for r, row in enumerate(BACK_ARROW):
            for c, ch in enumerate(row):
                if ch == "X":
                    surf.fill(BLACK, (x0 + c * cell, y0 + r * cell, cell, cell))