from pathlib import Path
import pygame
from game.settings import COLORS, HEIGHT, WIDTH
from ui.text import draw_text


class StoryScene:
    def __init__(self, game, on_done=None, script=None):
        self.game = game
        self.on_done = on_done or game.new_run
        self.script = [
    {
        "bg": "1.png",
        "speaker": ". . .",
        "text": "As evening fell over the quiet farm...",
        "sound": None
    },
    {
        "bg": "1.png",
        "speaker": ". . .",
        "text": "A cool breeze blew down from the mountains across the open fields.",
        "sound": None
    },
    {
        "bg": "1.png",
        "speaker": ". . .",
        "text": "All the farm animals were resting peacefully in their spots.",
        "sound": None
    },
    {
        "bg": "1.png",
        "speaker": ". . .",
        "text": "Including a certain little orange cat...",
        "sound": None
    },
    {
        "bg": "1.png",
        "speaker": ". . .",
        "text": "Everything seemed completely normal.",
        "sound": None
    },
    {
        "bg": "1.png",
        "speaker": ". . .",
        "text": "Except for one thing...",
        "sound": None
    },
    {
         "bg": "1.png",
        "speaker": ". . .",
        "text": "! ? ! ? !",
        "sound": "!.mp3"
    },
    {
        "bg": "2.png",
        "speaker": "(You)",
        "text": "Zzz z ... .z",
        "sound": "snore.mp3"
    },
    {
        "bg": "2.5.png",
        "speaker": "Alien Cat B1",
        "text": "Why is he sleeping here",
        "sound": "talk.mp3"
    },
    {
        "bg": "2.5.png",
        "speaker": "Alien Cat B2",
        "text": "I think he just sleepy",
        "sound": "talk.mp3"
    },
    {
        "bg": "2.5.png",
        "speaker": "Alien Cat B1",
        "text": "Are you thinking what I'm thinking, B1?",
        "sound": "talk.mp3"
    },
    {
        "bg": "2.5.png",
        "speaker": "Alien Cat B2",
        "text": "I think I am, B2!",
        "sound": "talk.mp3"
    },
    {
        "bg": "3.png",
         "speaker": "B1 & B2",
         "text": "Let's take him back home!",
        "sound": "talk.mp3"
    },
    {
        "bg": "4.png",
        "speaker": "B1 & B2",
        "text": "Muheheheheheh",
        "sound": "realufo.mp3"
    },
    {
        "bg": "5.png",
        "speaker": "B1 & B2",
        "text": "Let's go!!!",
        "sound": None
    },
    {
        "bg": "5.png",
        "speaker": "(You)",
        "text": "HELPPPPPPPPPPPP!!!!",
        "sound": None
    }
]
        self.current_line_idx = 0

        # ตัวแปรเก็บภาพพื้นหลังปัจจุบัน
        self.current_bg = None
        self._load_current_background()

        # ตัวแปรสำหรับการพิมพ์ข้อความทีละตัวอักษร (Typewriter Effect)
        self.current_text = ""
        self.target_text = self.script[0]["text"]
        self.char_index = 0
        self.text_timer = 0
        self.text_speed = 35  # ความเร็วในการพิมพ์ (มิลลิวินาที)
        self.is_finished_typing = False
        self.has_played_sound = False  # ตัวแปรเช็คสถานะการเล่นเสียงประจำบรรทัด

        # โหลดเสียง Soundboard พื้นฐาน (สำหรับเสียงพิมพ์ตัวหนังสือ)
        self.blip_sound = self._load_sound("text_blip.wav")

        # จัดการเสียงเพลงพื้นหลัง (Background Music สำหรับช่วง 1.png)
        self._manage_background_music()

    def _load_current_background(self):
        """โหลดรูปภาพพื้นหลัง พร้อมปรับให้ขยายแบบ Pixel Art (ไม่เบลอ)"""
        bg_name = self.script[self.current_line_idx]["bg"]
        bg_path = Path("game/scenes/image") / bg_name

        if bg_path.exists():
            image = pygame.image.load(str(bg_path)).convert()
            # ใช้ pygame.transform.scale ปกติ แต่ถ้าต้องการให้แตกเป็นเม็ดพิกเซลชัดๆ
            # สามารถใช้ pygame.transform.scale แบบพิกเซลได้ หรือถ้าภาพต้นฉบับคมอยู่แล้ว ตัวนี้เอาอยู่ครับ
            self.current_bg = pygame.transform.scale(image, (WIDTH, HEIGHT))
        else:
            print(f"[StoryScene] Warning: Background image not found at {bg_path}")
            surf = pygame.Surface((WIDTH, HEIGHT))
            surf.fill((10, 10, 15))
            self.current_bg = surf

    def _load_sound(self, name):
        sound_path = Path("game/scenes/soundeffect") / name
        if sound_path.exists():
            try:
                return pygame.mixer.Sound(str(sound_path))
            except:
                pass
        return None

    def _manage_background_music(self):
        """จัดการเพลงพื้นหลัง: ถ้าอยู่หน้า 1.png ให้เล่นวนไปเรื่อยๆ ถ้าพ้นแล้วให้หยุด"""
        current_bg = self.script[self.current_line_idx]["bg"]
        bg_music_path = Path("game/scenes/soundeffect") / "farm.mp3"

        if current_bg == "1.png":
            if bg_music_path.exists() and not pygame.mixer.music.get_busy():
                try:
                    pygame.mixer.music.load(str(bg_music_path))
                    pygame.mixer.music.play(-1)
                except Exception as e:
                    print(f"[StoryScene] Cannot play BGM: {e}")
        else:
            pygame.mixer.music.stop()

    def _play_current_sound(self):
        sound_name = self.script[self.current_line_idx].get("sound")
        if sound_name:
            sound = self._load_sound(sound_name)
            if sound:
                sound.play()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._progress_text()
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
                self._progress_text()
            elif event.key == pygame.K_ESCAPE:
                self._finish()

    def _progress_text(self):
        if not self.is_finished_typing:
            self.current_text = self.target_text
            self.char_index = len(self.target_text)
            self.is_finished_typing = True

            # ถ้ากดคลิกข้ามตอนกำลังพิมพ์ แล้วเสียงยังไม่เคยเล่น ให้เล่นเสียงดักไว้เลย
            if not self.has_played_sound:
                self._play_current_sound()
                self.has_played_sound = True
        else:
            self.current_line_idx += 1
            if self.current_line_idx < len(self.script):
                self.target_text = self.script[self.current_line_idx]["text"]
                self.current_text = ""
                self.char_index = 0
                self.is_finished_typing = False
                self.has_played_sound = False  # รีเซ็ตสถานะเสียงสำหรับบรรทัดใหม่

                self._load_current_background()
                self._manage_background_music()
            else:
                pygame.mixer.music.stop()
                self._finish()

    def update(self, dt):
        if not self.is_finished_typing:
            self.text_timer += dt * 1000
            if self.text_timer >= self.text_speed:
                self.text_timer = 0
                if self.char_index < len(self.target_text):
                    # เติมตัวอักษรทีละตัว
                    self.current_text += self.target_text[self.char_index]
                    self.char_index += 1

                    # ทันทีที่ตัวอักษรตัวแรกปรากฏขึ้น (char_index == 1) ให้สั่งเล่นเสียงพูดทันที!
                    if self.char_index == 1 and not self.has_played_sound:
                        self._play_current_sound()
                        self.has_played_sound = True

                    # เสียงก๊อกแก๊กพิมพ์ตัวหนังสือ
                    if self.blip_sound and self.char_index % 2 == 0:
                        self.blip_sound.play()
                else:
                    self.is_finished_typing = True

    def draw(self, screen):
        if self.current_bg:
            screen.blit(self.current_bg, (0, 0))

        box_width = WIDTH -  800
        box_height = 130
        box_x = (WIDTH - box_width) // 2
        box_y = HEIGHT - 160
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

        #Stardew
        c_outline = (58, 25, 11)
        c_wood_dark = (145, 72, 24)
        c_wood_mid = (204, 118, 43)
        c_wood_light = (242, 165, 78)
        c_bg_main = (248, 203, 134)
        c_bg_shadow = (232, 174, 102)
        c_text = (58, 25, 11)

        pygame.draw.rect(screen, c_bg_main, box_rect)
        shadow_rect = pygame.Rect(box_rect.x, box_rect.bottom - 30, box_rect.width, 30)
        pygame.draw.rect(screen, c_bg_shadow, shadow_rect)

        #ขอบไม้
        pygame.draw.rect(screen, c_outline, box_rect, 4)
        pygame.draw.rect(screen, c_wood_dark, box_rect.inflate(-8, -8), 4)
        pygame.draw.rect(screen, c_wood_mid, box_rect.inflate(-16, -16), 4)
        pygame.draw.rect(screen, c_wood_light, box_rect.inflate(-24, -24), 2)

        #มุมกล่อง
        corner_offsets = [
            (box_rect.left + 8, box_rect.top + 8),
            (box_rect.right - 14, box_rect.top + 8),
            (box_rect.left + 8, box_rect.bottom - 14),
            (box_rect.right - 14, box_rect.bottom - 14),
        ]
        for cx, cy in corner_offsets:
            pygame.draw.rect(screen, c_outline, (cx, cy, 6, 6))
            pygame.draw.rect(screen, c_wood_light, (cx + 1, cy + 1, 3, 3))

        #ป้ายชื่อ
        current_speaker = self.script[self.current_line_idx]["speaker"]
        tag_width = max(110, len(current_speaker) * 12 + 24)
        tag_height = 32
        tag_rect = pygame.Rect(box_rect.x + 20, box_rect.y - 20, tag_width, tag_height)

        pygame.draw.rect(screen, c_bg_main, tag_rect)
        pygame.draw.rect(screen, c_outline, tag_rect, 3)
        pygame.draw.rect(screen, c_wood_mid, tag_rect.inflate(-6, -6), 3)

        font_size = 25
        temp_font = pygame.font.Font(None, 32)
        text_w, text_h = temp_font.size(current_speaker)
        text_x = tag_rect.centerx - (text_w // 4) - 20
        text_y = tag_rect.centery - (text_h // 4) - 2

        draw_text(screen, current_speaker, (text_x, text_y), font_size, c_text)
        draw_text(screen, self.current_text, (box_rect.x + 25, box_rect.y + 30), 20, c_text)

        # 5. วาดไอคอนสามเหลี่ยมพิกเซลตรงมุมขวาล่างเมื่อพิมพ์จบ
        if self.is_finished_typing:
            btn_rect = pygame.Rect(box_rect.right - 34, box_rect.bottom - 30, 16, 16)
            pygame.draw.rect(screen, c_wood_mid, btn_rect)
            pygame.draw.rect(screen, c_outline, btn_rect, 2)
            draw_text(screen, "▼", (btn_rect.x + 2, btn_rect.y - 1), 12, c_text)

    def _finish(self):
        pygame.mixer.music.stop()
        pygame.mixer.stop()
        self.on_done()