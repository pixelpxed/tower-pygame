from pathlib import Path

import pygame
from game.settings import HEIGHT, WIDTH
from PIL import Image

HERE = Path(__file__).resolve().parent


class _SkipButton:
    def __init__(self, rect, callback):
        self.rect, self.callback = rect, callback
        font = pygame.font.SysFont("couriernew,consolas,dejavusansmono,monospace", 22, bold=True)
        small = font.render(">", False, (238, 250, 57))
        self.label = pygame.transform.scale(small, (50, 50))

    def handle_event(self, event):
        if (event.type == pygame.MOUSEBUTTONUP and event.button == 1
                and self.rect.collidepoint(event.pos)):
            self.callback()

    def draw(self, screen):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        r = self.rect.inflate(10, 4) if hover else self.rect
        pygame.draw.rect(screen, (0, 0, 0), r.move(0, 4), border_radius=r.h // 2)
        bg_color = (30, 35, 30) if hover else (12, 14, 18)
        pygame.draw.rect(screen, bg_color, r, border_radius=r.h // 2)
        screen.blit(self.label, self.label.get_rect(center=r.center))


def _find(name):
    for path in (HERE / name,
                 HERE.parents[1] / "assets" / "images" / name,
                 HERE.parents[1] / name,
                 Path("game/scenes") / name):
        if path.exists():
            return path
    return None


class CutScene:
    def __init__(self, game, on_done=None, gif_name="cut.gif", duration_ms=10000, fade_ms=2000):
        self.game = game
        self.on_done = on_done or game.new_run
        self.duration_ms = duration_ms
        self.fade_ms = fade_ms
        self.finished = False
        self.start_ticks = None

        self.frames = self._preload_gif(gif_name)
        self.total_gif_duration = sum(dur for _, dur in self.frames) if self.frames else 1000

        self.fade_surface = pygame.Surface((WIDTH, HEIGHT)).convert()
        self.fade_surface.fill((0, 0, 0))

        margin, w, h = 24, 80, 80
        self.skip = _SkipButton(pygame.Rect(WIDTH - margin - w, HEIGHT - margin - h, w, h),self._finish)

    def _preload_gif(self, name):
        if Image is None:
            print("[cutscene] Pillow is not installed. Skipping cutscene.")
            return []
        path = _find(name)
        if path is None:
            print(f"[cutscene] {name} not found. Skipping cutscene.")
            return []

        frames = []
        try:
            with Image.open(path) as img:
                for frame_idx in range(getattr(img, "n_frames", 1)):
                    img.seek(frame_idx)
                    frame = img.convert("RGB")
                    if frame.size != (WIDTH, HEIGHT):
                        frame = frame.resize((WIDTH, HEIGHT))
                    surf = pygame.image.frombytes(frame.tobytes(), frame.size, "RGB").convert()
                    duration = max(20, img.info.get("duration", 40))
                    frames.append((surf, duration))
        except Exception as err:
            print(f"[cutscene] Could not process {path}: {err}")
        return frames

    def _get_current_frame(self, elapsed):
        if not self.frames:
            return None
        loop_time = elapsed % self.total_gif_duration
        accum = 0
        for surf, duration in self.frames:
            accum += duration
            if loop_time < accum:
                return surf
        return self.frames[-1][0]

    def _finish(self):
        if self.finished:
            return
        self.finished = True
        self.on_done()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (
                pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN):
            self._finish()
            return
        self.skip.handle_event(event)

    def draw(self, screen):
        now = pygame.time.get_ticks()
        if self.start_ticks is None:
            self.start_ticks = now
        elapsed = now - self.start_ticks

        screen.fill((0, 0, 0))

        frame_surf = self._get_current_frame(elapsed)
        if frame_surf is not None:
            screen.blit(frame_surf, (0, 0))

        alpha = 0
        if elapsed < self.fade_ms:
            # Fade In
            progress = elapsed / self.fade_ms
            alpha = int(255 * (1.0 - progress))
        elif elapsed > (self.duration_ms - self.fade_ms):
            # Fade Out
            progress = (elapsed - (self.duration_ms - self.fade_ms)) / self.fade_ms
            alpha = int(255 * progress)

        alpha = max(0, min(255, alpha))
        if alpha > 0:
            self.fade_surface.set_alpha(alpha)
            screen.blit(self.fade_surface, (0, 0))

        self.skip.draw(screen)
        if elapsed >= self.duration_ms and not self.finished:
            self._finish()