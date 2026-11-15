import math
import random
from pathlib import Path
import pygame

from game.settings import HEIGHT, WIDTH
from ui.text import draw_text

IMAGE_DIR = Path("game/scenes/image")
SOUND_DIR = Path("game/scenes/soundeffect")

IMAGES = ["1.png", "2.5.png", "2.png", "3.png", "4.png", "5.png", "black.jpg"]
SOUND = "glitch.mp3"
DURATION_MS = 4500
START_INTERVAL = 380
END_INTERVAL = 60
SHAKE_PX = 14
WOBBLE_DEG = 5
FLASH_EFFECTS = True

SKIP_HINT = "Press ESC to skip"

TINTS = [(255, 40, 120), (40, 220, 255), (255, 230, 40), (140, 80, 255), (60, 255, 120)]


def _ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


class CutScene:
    def __init__(self, game, on_done=None):
        self.game = game
        self.on_done = on_done or getattr(game, "start_tower", game.new_run)
        self.finished = False
        self.start_ticks = None
        self.last_switch = 0
        self.idx = 0
        self.tint = TINTS[0]
        self.inverted = False

        self.frames = [f for f in (self._load(n) for n in IMAGES) if f is not None]
        self.fade_surface = pygame.Surface((WIDTH, HEIGHT)).convert()
        self.fade_surface.fill((0, 0, 0))
        self.tint_surface = pygame.Surface((WIDTH, HEIGHT)).convert()

    def _load(self, name):
        path = IMAGE_DIR / name
        if not path.exists():
            print(f"[cutscene] {path} not found. Skipping this image.")
            return None
        try:
            img = pygame.image.load(str(path)).convert()
            return pygame.transform.scale(img, (WIDTH, HEIGHT))
        except pygame.error as err:
            print(f"[cutscene] Could not load {path}: {err}")
            return None

    def _finish(self):
        if self.finished:
            return
        self.finished = True
        pygame.mixer.stop()
        self.on_done()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (
                pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
            self._finish()

    def _switch(self):
        self.idx = (self.idx + 1) % len(self.frames)
        self.tint = random.choice(TINTS)
        self.inverted = FLASH_EFFECTS and random.random() < 0.25

    def _draw_skip_hint(self, screen):
        pos = (WIDTH // 2, HEIGHT - 32)
        draw_text(screen, SKIP_HINT, (pos[0] + 2, pos[1] + 2), 20, (0, 0, 0), center=True)
        draw_text(screen, SKIP_HINT, pos, 20, (255, 255, 255), center=True)

    def draw(self, screen):
        if not self.frames:
            self._finish()
            return

        now = pygame.time.get_ticks()
        if self.start_ticks is None:
            self.start_ticks = now
            self.last_switch = now
            if SOUND and (SOUND_DIR / SOUND).exists():
                try:
                    pygame.mixer.Sound(str(SOUND_DIR / SOUND)).play()
                except pygame.error:
                    pass

        elapsed = now - self.start_ticks
        p = min(1.0, elapsed / DURATION_MS)
        speed = _ease(p)  # 0 -> 1 : ยิ่งนานยิ่งเร็วขึ้น

        interval = START_INTERVAL + (END_INTERVAL - START_INTERVAL) * speed
        if now - self.last_switch >= interval:
            self.last_switch = now
            self._switch()

        frame = self.frames[self.idx]
        if self.inverted:
            inv = pygame.Surface((WIDTH, HEIGHT))
            inv.fill((255, 255, 255))
            inv.blit(frame, (0, 0), special_flags=pygame.BLEND_RGB_SUB)
            frame = inv

        beat = (now - self.last_switch) / max(1, interval)  # 0..1 ภายในแต่ละภาพ
        punch = (1.0 - min(1.0, beat)) ** 2  # แรงสุดตอนเพิ่งสลับ
        zoom = 1.08 + 0.12 * punch * (0.5 + speed)
        angle = WOBBLE_DEG * math.sin(elapsed / 90.0) * (0.3 + speed) if WOBBLE_DEG else 0
        if angle:
            frame = pygame.transform.rotozoom(frame, angle, zoom * 1.1)
        else:
            frame = pygame.transform.scale(
                frame, (int(WIDTH * zoom), int(HEIGHT * zoom)))

        shake = SHAKE_PX * (0.3 + speed)
        ox = random.uniform(-shake, shake)
        oy = random.uniform(-shake, shake)
        rect = frame.get_rect(center=(WIDTH // 2 + ox, HEIGHT // 2 + oy))
        screen.fill((0, 0, 0))
        screen.blit(frame, rect)

        if FLASH_EFFECTS and punch > 0.05:
            self.tint_surface.fill(tuple(int(c * punch * 0.55) for c in self.tint))
            screen.blit(self.tint_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

        alpha = 0
        if elapsed < 250:
            if FLASH_EFFECTS:
                self.tint_surface.fill((255, 255, 255))
                self.tint_surface.set_alpha(int(255 * (1 - elapsed / 250)))
                screen.blit(self.tint_surface, (0, 0))
                self.tint_surface.set_alpha(None)
        elif elapsed > DURATION_MS - 400:
            alpha = int(255 * (elapsed - (DURATION_MS - 400)) / 400)

        alpha = max(0, min(255, alpha))
        if alpha:
            self.fade_surface.set_alpha(alpha)
            screen.blit(self.fade_surface, (0, 0))
        self._draw_skip_hint(screen)

        if elapsed >= DURATION_MS:
            self._finish()