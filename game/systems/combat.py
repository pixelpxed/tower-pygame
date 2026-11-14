from game.entities.monster import BattleMonster
from game.entities.player import Player


class Combat:
    @staticmethod
    def resolve(player: Player, monster: BattleMonster) -> bool:
        if player.doable_damage > monster.power:
            return True
        player.lives = 0 if monster.kind == "boss" else max(0, player.lives - 1)
        player.position = (0, 0)
        return False
