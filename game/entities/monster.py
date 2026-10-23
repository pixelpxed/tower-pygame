from dataclasses import dataclass


@dataclass(frozen=True)
class Monster:
    name: str
    max_health: int
    attack: int
    gold: int
    image: str = ""

    def to_battle(self) -> "BattleMonster":
        return BattleMonster(self.name, self.max_health, self.max_health, self.attack, self.gold, self.image)


@dataclass
class BattleMonster:
    name: str
    max_health: int
    health: int
    attack: int
    gold: int
    image: str = ""

    @property
    def alive(self) -> bool:
        return self.health > 0

    def take_damage(self, amount: int) -> None:
        self.health = max(0, self.health - max(0, amount))