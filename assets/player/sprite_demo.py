"""ตัวอย่าง pygame: เล่นแอนิเมชันฟันดาบจากสไปรท์ชีต
กด SPACE = ฟัน | F = สลับซ้าย/ขวา | ESC = ออก
ติดตั้ง: pip install pygame
"""
import json, os
import pygame

HERE = os.path.dirname(os.path.abspath(__file__))
SCALE = 4  # ขยายแบบ pixel art (ไม่เบลอ)


class Animation:
    def __init__(self, frames, durations, loop=False):
        self.frames, self.durations, self.loop = frames, durations, loop
        self.reset()

    def reset(self):
        self.index, self.timer, self.done = 0, 0, False

    def update(self, dt_ms):
        if self.done:
            return
        self.timer += dt_ms
        while self.timer >= self.durations[self.index]:
            self.timer -= self.durations[self.index]
            if self.index + 1 < len(self.frames):
                self.index += 1
            elif self.loop:
                self.index = 0
            else:
                self.done = True
                break

    @property
    def image(self):
        return self.frames[self.index]


def load_frames(meta):
    sheet = pygame.image.load(os.path.join(HERE, meta["sheet"])).convert_alpha()
    w, h = meta["frame_width"], meta["frame_height"]
    return [sheet.subsurface((f["index"] * w, 0, w, h)).copy() for f in meta["frames"]]


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Lightsaber cat (orange)")
    clock = pygame.time.Clock()

    with open(os.path.join(HERE, "attack.json"), encoding="utf-8") as fp:
        meta = json.load(fp)
    frames = load_frames(meta)
    durations = [f["duration_ms"] for f in meta["frames"]]

    idle = frames[0]
    attack = Animation(frames, durations)
    attacking, flip = False, False

    running = True
    while running:
        dt = clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE and not attacking:
                    attacking = True
                    attack.reset()
                elif e.key == pygame.K_f:
                    flip = not flip

        if attacking:
            attack.update(dt)
            if attack.done:
                attacking = False
        img = attack.image if attacking else idle
        if flip:
            img = pygame.transform.flip(img, True, False)
        img = pygame.transform.scale(img, (img.get_width() * SCALE, img.get_height() * SCALE))

        screen.fill((40, 44, 60))
        # วางโดยให้ "เท้า" อยู่ตำแหน่งเดิมทุกเฟรม (เฟรมทุกอันขนาด 100x100 เท้าอยู่แถวเดียวกัน)
        screen.blit(img, img.get_rect(midbottom=(320, 440)))
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
