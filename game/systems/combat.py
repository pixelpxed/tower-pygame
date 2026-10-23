from game.entities.monster import BattleMonster
from game.entities.player import Player


class Combat:
    """Turn-based combat rules."""

    @staticmethod
    def player_attack(player: Player, monster: BattleMonster) -> int:
        damage = player.deal_damage()
        monster.take_damage(damage)
        return damage

    @staticmethod
    def monster_attack(player: Player, monster: BattleMonster) -> int:
        damage = monster.attack
        player.take_damage(damage)
        return damage
