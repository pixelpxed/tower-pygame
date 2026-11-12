import json
from pathlib import Path

from game.entities.monster import Monster


class Tower:
    def __init__(self, data_path: Path):
        data = json.loads(data_path.read_text(encoding="utf-8"))
        self.towers = data["towers"]
        if not isinstance(self.towers, list) or not self.towers:
            raise ValueError("Tower data must contain at least one tower")
        for tower in self.towers:
            if not isinstance(tower["floors"], list) or not tower["floors"]:
                raise ValueError("Each tower must contain at least one floor")
            for floor in tower["floors"]:
                Monster(**floor["monster"])

    def floors_for_tower(self, tower: int) -> list[dict]:
        if not 0 <= tower < len(self.towers):
            raise IndexError("Invalid tower index")
        return self.towers[tower]["floors"]

    def monster_for_floor(self, tower: int, floor: int) -> Monster:
        floors = self.floors_for_tower(tower)
        if not 0 <= floor < len(floors):
            raise IndexError("Invalid floor index")
        return Monster(**floors[floor]["monster"])

    def tower_complete(self, tower: int, defeated: set[tuple[int, int]]) -> bool:
        return all((tower, floor) in defeated for floor in range(len(self.floors_for_tower(tower))))

    def tower_name(self, tower: int) -> str:
        return self.towers[tower]["name"]
