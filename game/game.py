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
        self.tower = Tower(DATA_DIR / "towers.json")
        self.potion = Item("Potion", "Restores health", 25)
        self.scene = MenuScene(self)

    def new_run(self):
        self.player.reset()
        self.won = False
        self.message = ""
        self.scene = TowerScene(self)

    def show_menu(self):
        self.scene = MenuScene(self)

    def start_battle(self):
        if self.tower.is_complete(self.player.floor):
            self.won = True
            self.message = "Every floor has been conquered."
            self.scene = GameOverScene(self)
            return
        self.monster = self.tower.monster_for_floor(self.player.floor)
        self.message = "Choose your action."
        self.scene = BattleScene(self)

    def player_attack(self):
        if not self.monster or not self.monster.alive:
            return
        damage = Combat.player_attack(self.player, self.monster)
        if not self.monster.alive:
            Progression.reward_for_victory(self.player, self.monster)
            self.message = Progression.reward_text(self.monster)
            self.scene = TowerScene(self)
            return
        taken = Combat.monster_attack(self.player, self.monster)
        self.message = f"You dealt {damage} damage and took {taken} damage."
        if not self.player.alive:
            self.won = False
            self.scene = GameOverScene(self)

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