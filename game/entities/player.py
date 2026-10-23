from dataclasses import dataclass, field


@dataclass
class Player:
    name: str = "Hero"
    max_health: int = 100
    health: int = 100
    attack: int = 12
    tower: int = 0
    floor: int = 1
    location_tower: int = 0
    location_floor: int = 1
    gold: int = 0
    inventory: list[str] = field(default_factory=list)

    @property
    def alive(self) -> bool:
        return self.health > 0

    def deal_damage(self) -> int:
        return self.attack

    def take_damage(self, amount: int) -> None:
        self.health = max(0, self.health - max(0, amount))

    def heal(self, amount: int) -> None:
        self.health = min(self.max_health, self.health + max(0, amount))

    def reset(self) -> None:
        self.health = self.max_health
        self.tower = 0
        self.floor = 1
        self.location_tower = 0
        self.location_floor = 1
        self.gold = 0
        self.inventory.clear()