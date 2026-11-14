class Progression:
    @staticmethod
    def reward_for_victory(player, monster) -> None:
        player.power += monster.power
        player.item = monster.item
