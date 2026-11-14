from pathlib import Path
import pygame
from game.settings import COLORS, HEIGHT, WIDTH
from ui.text import draw_text


class EndWinScene:
    def __init__(self, game, on_done=None, script=None):
        self.game = game
        # กำหนด on_done สำรองเมื่อจบฉากนี้ (เช่น กลับไปหน้าเมนูหลัก)
        self.on_done = on_done or getattr(game, "show_menu", game.new_run)

        # Script สำหรับเหตุการณ์ตอนชนะ (สามารถปรับเปลี่ยนข้อความ, รูปภาพ, และเสียงได้ตามต้องการ)
        self.script = script or [
            {
                "bg": "black.jpg",  # เปลี่ยนชื่อไฟล์ภาพฉากชนะตามต้องการ
                "speaker": "Alien Cat",
                "text": "m'aider m'aider ... m'aider ",
                "sound": "talk.mp3"
            },
            {
                "bg": "black.jpg",
                "speaker": "Alien Cat",
                "text": "He betrayed us. . . .",
                "sound": "talk.mp3"
            },
            {
                "bg": "black.jpg",
                "speaker": "Alien Cat",
                "text": " stop .. him .....",
                "sound": "talk.mp3"
            },
            {
                "bg": "black.jpg",
                "speaker": "Alien Cat",
                "text": " . . . ",
                "sound": "fail.mp3"
            },
            {
                "bg": "4.png",
                "speaker": "(You)",
                "text": ". . .",
                "sound": "!.mp3"
            },
            {
                "bg": "end_win0.png",
                "speaker": "(You)",
                "text": "Finally! I got back home!",
                "sound": None
            },
            {
                "bg": "end_win0.png",
                "speaker": "(You)",
                "text": "Hope I won't get kidnapped by aliens again",
                "sound": None
            },
            {
                "bg": "end_win0.png",
                "speaker": "(You)",
                "text": "Let's just go back to sleep. . .",
                "sound": None
            },
            {
                "bg": "2.png",
                "speaker": "(You)",
                "text": ". . .",
                "sound": None
            },
            {
                "bg": "2.png",
                "speaker": ". . .",
                "text": "Thank you for enjoying this journey together",
                "sound": None
            },
            {
                "bg": "2.png",
                "speaker": ". . .",
                "text": "If you found bugs,please report them at ... schegen, ermin, and jah",
                "sound": None
            },
            {
                "bg": "2.png",
                "speaker": ". . .",
                "text": "Bye bye!",
                "sound": None
            },
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

        # จัดการเสียงเพลงพื้นหลัง (Background Music สำหรับฉากชนะ)
        self._manage_background_music()

    def _load_current_background(self):
        """โหลดรูปภาพพื้นหลัง พร้อมปรับให้ขยายแบบ Pixel Art (ไม่เบลอ)"""
        bg_name = self.script[self.current_line_idx]["bg"]
        bg_path = Path("game/scenes/image") / bg_name

        if bg_path.exists():
            image = pygame.image.load(str(bg_path)).convert()
            self.current_bg = pygame.transform.scale(image, (WIDTH, HEIGHT))
        else:
            print(f"[EndWinScene] Warning: Background image not found at {bg_path}")
            surf = pygame.Surface((WIDTH, HEIGHT))
            surf.fill((10, 20, 30))  # สีพื้นหลังโทนสว่าง/อวกาศสำรองกรณีหาภาพไม่พบ
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
        """จัดการเพลงพื้นหลังประจำฉากชนะ"""
        bg_music_path = Path("game/scenes/soundeffect") / "win_theme.mp3"  # เปลี่ยนชื่อเพลงชนะตามต้องการ
        if bg_music_path.exists() and not pygame.mixer.music.get_busy():
            try:
                pygame.mixer.music.load(str(bg_music_path))
                pygame.mixer.music.play(-1)
            except Exception as e:
                print(f"[EndWinScene] Cannot play BGM: {e}")

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
                pygame.mixer.music.stop()
                self.on_done()

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
                self.on_done()

    def update(self, dt):
        """เอฟเฟกต์ตัวอักษรวิ่งทีละตัว และซิงค์เสียงพูดให้มาพร้อมข้อความตัวแรก"""
        if not self.is_finished_typing:
            self.text_timer += dt * 1000
            if self.text_timer >= self.text_speed:
                self.text_timer = 0
                if self.char_index < len(self.target_text):
                    # เติมตัวอักษรทีละตัว
                    self.current_text += self.target_text[self.char_index]
                    self.char_index += 1

                    # ทันทีที่ตัวอักษรตัวแรกปรากฏขึ้น ให้เล่นเสียงพูดทันที
                    if self.char_index == 1 and not self.has_played_sound:
                        self._play_current_sound()
                        self.has_played_sound = True

                    # เสียงพิมพ์ตัวหนังสือ
                    if self.blip_sound and self.char_index % 2 == 0:
                        self.blip_sound.play()
                else:
                    self.is_finished_typing = True

    def draw(self, screen):
        if self.current_bg:
            screen.blit(self.current_bg, (0, 0))

        box_width = WIDTH - 800 if WIDTH > 1000 else WIDTH - 100
        box_height = 130
        box_x = (WIDTH - box_width) // 2
        box_y = HEIGHT - 160
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

        # Stardew Valley Theme Colors
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

        # ขอบไม้
        pygame.draw.rect(screen, c_outline, box_rect, 4)
        pygame.draw.rect(screen, c_wood_dark, box_rect.inflate(-8, -8), 4)
        pygame.draw.rect(screen, c_wood_mid, box_rect.inflate(-16, -16), 4)
        pygame.draw.rect(screen, c_wood_light, box_rect.inflate(-24, -24), 2)

        # มุมกล่อง
        corner_offsets = [
            (box_rect.left + 8, box_rect.top + 8),
            (box_rect.right - 14, box_rect.top + 8),
            (box_rect.left + 8, box_rect.bottom - 14),
            (box_rect.right - 14, box_rect.bottom - 14),
        ]
        for cx, cy in corner_offsets:
            pygame.draw.rect(screen, c_outline, (cx, cy, 6, 6))
            pygame.draw.rect(screen, c_wood_light, (cx + 1, cy + 1, 3, 3))

        # ป้ายชื่อ (Speaker)
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
        text_y = tag_rect.centery - (text_h // 4) - 4

        draw_text(screen, current_speaker, (text_x, text_y), font_size, c_text)

        # แสดงข้อความบทสนทนาภายในกล่อง
        draw_text(screen, self.current_text, (box_rect.x + 25, box_rect.y + 30), 18, c_text)

        # วาดไอคอนสามเหลี่ยมพิกเซลตรงมุมขวาล่างเมื่อพิมพ์จบ
        if self.is_finished_typing:
            btn_rect = pygame.Rect(box_rect.right - 34, box_rect.bottom - 30, 16, 16)
            pygame.draw.rect(screen, c_wood_mid, btn_rect)
            pygame.draw.rect(screen, c_outline, btn_rect, 2)
            draw_text(screen, "▼", (btn_rect.x + 2, btn_rect.y - 1), 12, c_text)