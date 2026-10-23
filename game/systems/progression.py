class Progression:
    @staticmethod
    def reward_for_victory(player, monster) -> None:
        player.gold += monster.gold
        player.floor += 1

    @staticmethod
    def reward_text(monster) -> str:
        return f"Victory! You received {monster.gold} gold."
