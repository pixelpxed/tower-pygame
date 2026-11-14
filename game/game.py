import pygame

from game.entities.item import Item
from game.entities.player import Player
from game.settings import DATA_DIR, FPS, HEIGHT, TITLE, WIDTH
from game.systems.combat import Combat
from game.systems.progression import Progression
from game.systems.tower import Tower
from game.scenes.battle import BattleScene
from game.scenes.game_over import GameOverScene
from game.scenes.end_lost import EndLostScene
from game.scenes.end_win import EndWinScene
from game.scenes.menu import MenuScene
from game.scenes.tower import TowerScene
from game.scenes.cut_scene import CutScene
from game.scenes.story import StoryScene


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
        self.tower = Tower(DATA_DIR / "towers.json")
        self.scene = MenuScene(self)

    def new_run(self):
        self.player.reset()
        self.won = False
        self.message = ""
        self.monster = None
        self.defeated.clear()
        self.scene = StoryScene(self, on_done=self.show_cutscene)

    def show_cutscene(self):
        self.scene = CutScene(self, on_done=self.start_tower)

    def start_tower(self):
        self.scene = TowerScene(self)

    def show_menu(self):
        self.scene = MenuScene(self)

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
                self.scene = GameOverScene(self)
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
                self.scene = GameOverScene(self)

    def quit(self):
        self.running = False

    def run(self):
        while self.running:
            dt_ms = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                else:
                    self.scene.handle_event(event)
            if isinstance(self.scene, TowerScene):
                self.scene.update(dt_ms)
            else:
                update = getattr(self.scene, "update", None)
                if update is not None:
                    update(dt_ms / 1000)
            self.scene.draw(self.screen)
            pygame.display.flip()
        pygame.quit()
