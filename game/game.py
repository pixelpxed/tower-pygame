from pathlib import Path

import pygame

from game.entities.player import Player
from game.settings import DATA_DIR, FPS, HEIGHT, TITLE, WIDTH
from game.systems.combat import Combat
from game.systems.progression import Progression
from game.systems.tower import Tower
from game.scenes.cut_scene import CutScene
from game.scenes.end_lost import EndLostScene
from game.scenes.end_win import EndWinScene
from game.scenes.game_over import GameOverScene
from game.scenes.menu import MenuScene
from game.scenes.story import StoryScene
from game.scenes.tower import TowerScene


class Game:
    """Flow / scenes / endings: ezyZip.  Battle rules (power, items, boss): tower-pygame-main(4)."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
        self.monster = None
        self.message = ""
        self.won = False
        self.defeated = set()
        self.tower = Tower(DATA_DIR / "towers.json")
        self.scene = MenuScene(self)
        self.tower_scene = TowerScene(self)

    # ------------------------------------------------------------------ flow
    def new_run(self):
        """START -> Story -> CutScene -> TowerScene (flow จากไฟล์หลัก ezyZip)"""
        self.player.reset()
        self.won = False
        self.message = ""
        self.monster = None
        self.defeated.clear()
        self.scene = StoryScene(self, on_done=self.show_cutscene)

    def show_cutscene(self):
        self.scene = CutScene(self, on_done=self.start_tower)

    def start_tower(self):
        """หลัง CutScene จบ จะพาเข้าสู่หน้าหอคอย/เล่นเกมหลัก"""
        self.play_fight_music()
        self.scene = TowerScene(self)

    def show_menu(self):
        self.scene = MenuScene(self)

    def back_to_tower(self):
        self.monster = None
        self.message = ""
        self.play_fight_music()
        self.scene = TowerScene(self)

    def play_fight_music(self):
        music_path = Path(__file__).resolve().parent / "scenes" / "soundeffect" / "fight-theme.mp3"
        try:
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
        except pygame.error as error:
            print(f"[audio] Could not play {music_path}: {error}")

    # ---------------------------------------------------------------- combat
    def select_enemy(self, tower_index: int, floor_index: int) -> None:
        if tower_index != self.player.tower or (tower_index, floor_index) in self.defeated:
            return
        if not 0 <= tower_index < len(self.tower.towers):
            return
        if not 0 <= floor_index < len(self.tower.floors_for_tower(tower_index)):
            return
        if isinstance(self.scene, TowerScene) and self.scene.attacking:
            return

        previous_position = self.player.position
        self.player.position = (tower_index, floor_index)
        self.monster = self.tower.monster_for_floor(tower_index, floor_index)
        if isinstance(self.scene, TowerScene):
            self.scene.start_attack(
                self.player.doable_damage > self.monster.power,
                previous_position,
                self.player.position,
            )
        else:
            self.player_attack()

    def player_attack(self) -> None:
        monster = self.monster
        if monster is None or not self.player.alive:
            return

        if Combat.resolve(self.player, monster):
            previous_item = self.player.item or "None"
            Progression.reward_for_victory(self.player, monster)
            self.defeated.add(self.player.position)
            self.message = (f"Defeated! Power +{monster.power}. "
                            f"Item: {previous_item} -> {self.player.item or 'None'}.")
            if self.tower.tower_complete(self.player.tower, self.defeated):
                self.player.tower += 1
            if self.player.tower == len(self.tower.towers):
                self.won = True
                self.message = "Every floor has been conquered."
                self.scene = EndWinScene(self)          # ชนะครบทุกหอ -> ending แบบชนะ
            else:
                self.scene = TowerScene(self)
        else:
            if monster.kind == "boss":
                self.message = "You were defeated. Boss defeat: all lives lost."
            else:
                self.message = "You were defeated. Lost one life."
            self.won = False
            if monster.kind != "boss" and self.player.alive:
                self.back_to_tower()
                return
            # แพ้ทุกครั้งผ่านหน้า DEFEATED เพื่อให้เห็นหัวใจลดก่อน
            # (ถ้าหัวใจหมด หน้านี้จะพาไป EndLostScene เอง)
            self.scene = GameOverScene(self)

    def retry_battle(self):
        """ปุ่ม ↺ ในหน้า DEFEATED: แพ้แบบเทียบ Power ผลเดิมเสมอ จึงกลับไปเลือกชั้นใหม่ (ข้อความแพ้ยังค้างให้เห็น)"""
        if not self.player.alive:
            self.scene = EndLostScene(self)
            return
        self.monster = None
        self.play_fight_music()
        self.scene = TowerScene(self)

    # ------------------------------------------------------------------ loop
    def quit(self):
        self.running = False

    def _update_scene(self, dt_ms: int) -> None:
        update = getattr(self.scene, "update", None)
        if update is None:
            return
        if isinstance(self.scene, TowerScene):
            update(dt_ms)               # TowerScene (จาก A) รับหน่วยมิลลิวินาที
        else:
            update(dt_ms / 1000)        # Story / EndWin / EndLost (ezyZip) รับหน่วยวินาที

    def run(self):
        while self.running:
            dt_ms = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                else:
                    self.scene.handle_event(event)
            self._update_scene(dt_ms)
            self.scene.draw(self.screen)
            pygame.display.flip()
        pygame.quit()

    def play_sound(self, filename: str):
        sound_path = DATA_DIR.parent / "game" / "scenes" / "soundeffect" / filename
        sound = pygame.mixer.Sound(sound_path)
        sound.play()
