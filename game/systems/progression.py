from game.entities.monster import Monster
from game.entities.player import Player


class Progression:
    @staticmethod
    def reward_for_victory(player: Player, monster: Monster) -> None:
        player.power += monster.power
        player.item = monster.item
