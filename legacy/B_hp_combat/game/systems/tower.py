import json
from pathlib import Path

from game.entities.monster import BattleMonster


class Tower:
    def __init__(self, data_path: Path):
        data = json.loads(data_path.read_text(encoding="utf-8"))
        self.towers = data["towers"] if isinstance(data, dict) else data

    def floors_for_tower(self, tower: int) -> list[dict]:
        return self.towers[tower]["floors"]

    def monster_for_floor(self, tower: int, floor: int) -> BattleMonster:
        floors = self.floors_for_tower(tower)
        entry = floors[min(floor - 1, len(floors) - 1)]
        monster = entry["monster"]
        return BattleMonster(
            monster["name"],
            monster["health"],
            monster["health"],
            monster["attack"],
            monster["gold"],
            monster.get("image", ""),
        )

    def is_complete(self, tower: int, floor: int) -> bool:
        return tower >= len(self.towers)

    def tower_name(self, tower: int) -> str:
        return self.towers[tower]["name"]
