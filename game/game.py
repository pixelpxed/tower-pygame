import pygame

from game.entities.item import Item
from game.entities.player import Player
from game.settings import DATA_DIR, FPS, HEIGHT, TITLE, WIDTH
from game.systems.combat import Combat
from game.systems.progression import Progression
from game.systems.tower import Tower
from game.scenes.battle import BattleScene
from game.scenes.game_over import GameOverScene
from game.scenes.menu import MenuScene
from game.scenes.tower import TowerScene
from game.scenes.cut_scene import CutScene

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
        self.message = f"A wild {self.monster.name} appears!"
        self.scene = BattleScene(self)

    def _finish_battle(self):
        """Called after monster is defeated in BattleScene."""
        player = self.player
        monster = self.monster
        tower_index = player.location_tower
        floor_index = player.location_floor - 1
        enemy_id = (tower_index, floor_index)

        self.defeated.add(enemy_id)
        Progression.reward_for_victory(player, monster)
        recovered = player.health
        player.heal(player.max_health)
        recovered = player.health - recovered
        self.message = (
            f"{monster.name} defeated!"
            f" Recovered {recovered} health."
        )

        tower_floor_count = len(self.tower.floors_for_tower(player.tower))
        defeated_tower_floors = sum(
            (player.tower, fi) in self.defeated
            for fi in range(tower_floor_count)
        )
        if defeated_tower_floors == tower_floor_count:
            player.tower += 1
            player.floor = 1
        if player.tower >= len(self.tower.towers):
            self.won = True
            self.message = "Every floor has been conquered."
            self.scene = GameOverScene(self)
            return

        self.scene = TowerScene(self)

    def player_attack(self):
        """Called by BattleScene Attack button."""
        if self.monster is None or not self.monster.alive or not self.player.alive:
            return

        dealt = Combat.player_attack(self.player, self.monster)
        if not self.monster.alive:
            self.message = f"You dealt {dealt} damage. {self.monster.name} is defeated!"
            self._finish_battle()
            return

        taken = Combat.monster_attack(self.player, self.monster)
        self.message = f"You dealt {dealt} dmg. {self.monster.name} dealt {taken} dmg."

        if not self.player.alive:
            self.message = f"You were defeated by {self.monster.name}!"
            self.won = False
            self.scene = GameOverScene(self)

    def player_potion(self):
        """Called by BattleScene Use Potion button."""
        if self.potion.use(self.player):
            self.message = "You used a potion and recovered 25 health."
        else:
            self.message = "Your health is already full!"

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
