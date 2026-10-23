from game.entities.monster import BattleMonster
from game.entities.player import Player


class Combat:

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

    @staticmethod
    def resolve_instantly(player: Player, monster: BattleMonster) -> tuple[int, int]:
        damage_dealt = 0
        damage_taken = 0
        while player.alive and monster.alive:
            damage_dealt += Combat.player_attack(player, monster)
            if monster.alive:
                damage_taken += Combat.monster_attack(player, monster)
        return damage_dealt, damage_taken
