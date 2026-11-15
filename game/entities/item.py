from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    name: str
    description: str
    effect: int
    kind: str = "heal"

    def use(self, player) -> bool:
        if self.kind == "heal":
            before = player.health
            player.heal(self.effect)
            return player.health > before
        if self.kind == "attack":
            player.attack += self.effect
            return True
        return False