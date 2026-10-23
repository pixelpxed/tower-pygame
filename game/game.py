import pygame

from game.entities.item import Item
from game.entities.player import Player
from game.settings import DATA_DIR, FPS, HEIGHT, TITLE, WIDTH
from game.systems.combat import Combat
from game.systems.progression import Progression
from game.systems.tower import Tower
from game.scenes.game_over import GameOverScene
from game.scenes.menu import MenuScene
from game.scenes.tower import TowerScene


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
        self.potion = Item("Potion", "Restores health", 25)
        self.scene = MenuScene(self)

    def new_run(self):
        self.player.reset()
        self.won = False
        self.message = ""
        self.defeated.clear()
        self.scene = TowerScene(self)

    def show_menu(self):
        self.scene = MenuScene(self)

    def select_enemy(self, tower_index, floor_index):
        enemy_id = (tower_index, floor_index)
        if tower_index != self.player.tower or enemy_id in self.defeated:
            return

        self.player.location_tower = tower_index
        self.player.location_floor = floor_index + 1
        self.player.floor = floor_index + 1
        self.monster = self.tower.monster_for_floor(tower_index, floor_index + 1)
        dealt, taken = Combat.resolve_instantly(self.player, self.monster)
        if self.monster.alive:
            self.message = f"{self.monster.name} defeated you after {dealt} damage."
            self.won = False
            self.scene = GameOverScene(self)
            return

        self.defeated.add(enemy_id)
        Progression.reward_for_victory(self.player, self.monster)
        recovered = self.player.health
        self.player.heal(self.player.max_health)
        recovered = self.player.health - recovered
        self.message = (
            f"{self.monster.name} defeated! You dealt {dealt} damage and took {taken} damage."
            f" Recovered {recovered} health."
        )
        tower_floor_count = len(self.tower.floors_for_tower(self.player.tower))
        defeated_tower_floors = sum(
            (self.player.tower, floor_index) in self.defeated
            for floor_index in range(tower_floor_count)
        )
        if defeated_tower_floors == tower_floor_count:
            self.player.tower += 1
            self.player.floor = 1
        if self.player.tower >= len(self.tower.towers):
            self.won = True
            self.message = "Every floor has been conquered."
            self.scene = GameOverScene(self)
            return

    def use_potion(self):
        if self.potion.use(self.player):
            self.message = "You recovered 25 health."
        else:
            self.message = "Your health is already full."

    def quit(self):
        self.running = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                else:
                    self.scene.handle_event(event)
            self.scene.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()