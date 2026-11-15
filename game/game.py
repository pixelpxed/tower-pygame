from pathlib import Path
from collections.abc import Callable

import pygame

from game.entities.item import Item
from game.entities.player import Player
from game.settings import DATA_DIR, FPS, HEIGHT, TITLE, WIDTH
from game.systems.combat import Combat
from game.systems.progression import Progression
from game.systems.tower import Tower
from game.scenes.battle import BattleScene
from game.scenes.end_lost import EndLostScene
from game.scenes.end_win import EndWinScene
from game.scenes.menu import MenuScene
from game.scenes.tower import TowerScene
from game.scenes.cut_scene import CutScene
from game.scenes.story import StoryScene

FADE_DURATION_MS = 300


class Game:
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
        self.sound_effects = {}
        self.tower = Tower(DATA_DIR / "towers.json")
        self.scene = MenuScene(self)
        self._transition_phase = None
        self._transition_alpha = 0
        self._pending_scene = None
        self._transition_snapshot = None
        self._fade_surface = pygame.Surface((WIDTH, HEIGHT))
        self._fade_surface.fill((0, 0, 0))

    def _transition_to(self, scene_factory: Callable[[], object]) -> None:
        if self._transition_phase is not None:
            return
        self._pending_scene = scene_factory
        self._transition_snapshot = self.screen.copy()
        self._transition_phase = "out"
        self._transition_alpha = 0

    def _build_tower_scene(self):
        self.play_fight_music()
        return TowerScene(self)

    def _update_transition(self, dt_ms: int) -> None:
        change = dt_ms * 255 / FADE_DURATION_MS
        if self._transition_phase == "out":
            self._transition_alpha = min(255, self._transition_alpha + change)
            if self._transition_alpha == 255:
                self.scene = self._pending_scene()
                self._pending_scene = None
                self._transition_snapshot = None
                self._transition_phase = "in"
        else:
            self._transition_alpha = max(0, self._transition_alpha - change)
            if self._transition_alpha == 0:
                self._transition_phase = None

    def _draw_transition(self) -> None:
        if self._transition_phase is not None:
            self._fade_surface.set_alpha(round(self._transition_alpha))
            self.screen.blit(self._fade_surface, (0, 0))

    def play_sound(self, filename: str) -> None:
        sound_path = Path(__file__).resolve().parent / "scenes" / "soundeffect" / filename
        if not sound_path.exists():
            print(f"[audio] Sound effect not found: {sound_path}")
            return

        try:
            sound = self.sound_effects.get(filename)
            if sound is None:
                sound = pygame.mixer.Sound(str(sound_path))
                self.sound_effects[filename] = sound
            sound.play()
        except pygame.error as error:
            print(f"[audio] Could not play {sound_path}: {error}")

    def new_run(self):
        self.player.reset()
        self.won = False
        self.message = ""
        self.monster = None
        self.defeated.clear()
        self._transition_to(lambda: StoryScene(self, on_done=self.show_cutscene))

    def show_cutscene(self):
        self._transition_to(lambda: CutScene(self, on_done=self.start_tower))

    def play_fight_music(self):
        music_path = Path(__file__).resolve().parent / "scenes" / "soundeffect" / "fight-theme.mp3"
        try:
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
        except pygame.error as error:
            print(f"[audio] Could not play {music_path}: {error}")

    def start_tower(self):
        self._transition_to(self._build_tower_scene)

    def retry_battle(self):
        self.player.reset()
        self.won = False
        self.message = ""
        self.monster = None
        self.defeated.clear()
        self._transition_to(self._build_tower_scene)

    def show_menu(self):
        self._transition_to(lambda: MenuScene(self))

    def select_enemy(self, tower_index: int, floor_index: int) -> None:
        if tower_index != self.player.tower or (tower_index, floor_index) in self.defeated:
            return
        if not 0 <= tower_index < len(self.tower.towers):
            return
        if not 0 <= floor_index < len(self.tower.floors_for_tower(tower_index)):
            return
        if isinstance(self.scene, TowerScene) and self.scene.attacking:
            return

        self.player.position = (tower_index, floor_index)
        self.monster = self.tower.monster_for_floor(tower_index, floor_index)
        if isinstance(self.scene, TowerScene):
            self.scene.start_attack(self.player.doable_damage > self.monster.power)
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
                self._transition_to(lambda: EndWinScene(self))
            else:
                self.scene = TowerScene(self)
        else:
            if monster.kind == "boss":
                self.message = "You were defeated. Boss defeat: all lives lost."
            else:
                self.message = "You were defeated. Lost one life."
            if self.player.alive:
                self.scene = TowerScene(self)
            else:
                self.won = False
                self._transition_to(lambda: EndLostScene(self))

    def quit(self):
        self.running = False

    def run(self):
        while self.running:
            dt_ms = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif self._transition_phase is None:
                    self.scene.handle_event(event)
            if self._transition_phase is not None:
                self._update_transition(dt_ms)
            elif isinstance(self.scene, TowerScene):
                self.scene.update(dt_ms)
            else:
                update = getattr(self.scene, "update", None)
                if update is not None:
                    update(dt_ms / 1000)
            if self._transition_phase == "out" and self._transition_snapshot is not None:
                self.screen.blit(self._transition_snapshot, (0, 0))
            else:
                self.scene.draw(self.screen)
            self._draw_transition()
            pygame.display.flip()
        pygame.quit()
