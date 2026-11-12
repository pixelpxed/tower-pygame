from dataclasses import dataclass


@dataclass
class Player:
    name: str = "Hero"
    power: int = 5
    lives: int = 3
    item: str | None = None
    position: tuple[int, int] = (0, 0)
    tower: int = 0

    @property
    def alive(self) -> bool:
        return self.lives > 0

    @property
    def doable_damage(self) -> float:
        multiplier = {None: 1.0, "stick": 0.9, "lightsaber": 1.1}[self.item]
        return self.power * multiplier

    def reset(self) -> None:
        self.power = 5
        self.lives = 3
        self.item = None
        self.position = (0, 0)
        self.tower = 0
