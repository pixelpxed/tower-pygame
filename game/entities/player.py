from dataclasses import dataclass, field


@dataclass
class Player:
    name: str = "Hero"
    max_health: int = 100
    health: int = 100
    power: int = 5
    tower: int = 0
    floor: int = 1
    location_tower: int = 0
    location_floor: int = 1
    position: tuple[int, int] = (0, 0)
    gold: int = 0
    max_lives: int = 3
    lives: int = 3
    item: str | None = None
    inventory: list[str] = field(default_factory=list)

    @property
    def alive(self) -> bool:
        # เช็คทั้ง HP และ Lives เพื่อให้แน่ใจว่าตัวละครยังเล่นต่อได้
        return self.health > 0 and self.lives > 0

    @property
    def doable_damage(self) -> float:
        # คำนวณความเสียหายโดยอิงจาก item ที่ถืออยู่ (ถ้ามี)
        multiplier_map = {None: 1.0, "stick": 0.9, "lightsaber": 1.1}
        multiplier = multiplier_map.get(self.item, 1.0)
        return self.power * multiplier

    @property
    def attack(self) -> int:
        """ชื่อเดิมของค่าพลังโจมตี ตอนนี้ผูกกับ power (ไอเทมชนิด attack ที่ += จะไปเพิ่ม power)"""
        return self.power

    @attack.setter
    def attack(self, value: int) -> None:
        self.power = value

    def deal_damage(self) -> int:
        return int(self.doable_damage)

    def take_damage(self, amount: int) -> None:
        self.health = max(0, self.health - max(0, amount))

    def heal(self, amount: int) -> None:
        self.health = min(self.max_health, self.health + max(0, amount))

    def lose_life(self) -> None:
        self.lives = max(0, self.lives - 1)

    def reset(self) -> None:
        self.health = self.max_health
        self.power = 5
        self.tower = 0
        self.floor = 1
        self.location_tower = 0
        self.location_floor = 1
        self.position = (0, 0)
        self.gold = 0
        self.item = None
        self.inventory.clear()
        self.lives = self.max_lives