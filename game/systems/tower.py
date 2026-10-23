import json
from pathlib import Path

from game.entities.monster import BattleMonster


class Tower:
    def __init__(self, data_path: Path):
        self.floors = json.loads(data_path.read_text(encoding="utf-8"))

    def monster_for_floor(self, floor: int) -> BattleMonster:
        entry = self.floors[str(min(floor, len(self.floors)))]
        monster = entry["monster"]
        return BattleMonster(
            monster["name"],
            monster["health"],
            monster["health"],
            monster["attack"],
            monster["gold"],
            monster.get("image", ""),
        )

    def is_complete(self, floor: int) -> bool:
        return floor > len(self.floors)
