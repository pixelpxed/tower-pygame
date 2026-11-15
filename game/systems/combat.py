import pygame
from game.entities.monster import Monster
from game.entities.player import Player

pygame.mixer.init()
_bonk_sound = pygame.mixer.Sound("game/scenes/soundeffect/bonk.mp3")

class Combat:
    @staticmethod
    def player_attack(player: Player, monster: Monster) -> int:
        damage = int(getattr(player, "deal_damage", lambda: getattr(player, "doable_damage", 0))())
        if hasattr(monster, "take_damage"):
            monster.take_damage(damage)
        elif hasattr(monster, "health"):
            monster.health = max(0, monster.health - damage)

        # เล่นเสียง
        if _bonk_sound:
            _bonk_sound.play()

        return damage

    @staticmethod
    def monster_attack(player: Player, monster: Monster) -> int:
        damage = getattr(monster, "attack", getattr(monster, "power", 0))
        player.take_damage(damage)
        return damage

    @staticmethod
    def resolve_instantly(player: Player, monster: Monster) -> tuple[int, int]:
        damage_dealt = 0
        damage_taken = 0
        while player.alive and monster.alive:
            damage_dealt += Combat.player_attack(player, monster)
            if monster.alive:
                damage_taken += Combat.monster_attack(player, monster)
        return damage_dealt, damage_taken

    @staticmethod
    def resolve(player: Player, monster: Monster) -> bool:
        if _bonk_sound:
            _bonk_sound.play()

        monster_power = getattr(monster, "power", getattr(monster, "attack", 0))
        player_damage = getattr(player, "doable_damage", getattr(player, "deal_damage", lambda: 0)())
        if player_damage > monster_power:
            return True

        is_boss = getattr(monster, "kind", "") == "boss"
        if hasattr(player, "lose_life") and not is_boss:
            player.lose_life()
        else:
            player.lives = 0 if is_boss else max(0, player.lives - 1)

        player.position = (0, 0)
        return False
