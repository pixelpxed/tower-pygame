class Player:
    def __init__(self, position: tuple, power: int, lives: int, item: str):
        self.position = position
        self.power = power
        self.lives = lives
        self.item = item or None

    def add_power(self, power: int):
        self.power += power

    def get_power(self):
        return self.power

    def set_position(self, position: tuple):
        self.position = position

    def get_position(self):
        return self.position

    def set_item(self, item: str):
        self.item = item or None

    def get_item(self):
        return self.item

    def get_doable_damage(self):
        multiplier = 1
        if self.get_item() == "stick":
            multiplier = 0.9
        elif self.get_item() == "lightsaber":
            multiplier = 1.1

        return self.get_power() * multiplier

    def set_lives(self, lives: int):
        self.lives = lives

    def remove_life(self):
        self.lives -= 1
        return self.get_lives()

    def get_lives(self):
        return self.lives

    def __str__(self):
        return (
            f"Player (Pos: {self.position} / Power: {self.power} / Item: {self.item})"
        )


class Enemy:
    def __init__(self, kind: str, power: int, item: str):
        self.kind = kind
        self.power = power
        self.item = item or None

    def get_power(self):
        return self.power

    def get_item(self):
        return self.item

    def get_kind(self):
        return self.kind

    def __str__(self):
        return f"Enemy (Kind: {self.kind} / Power: {self.power} / Item: {self.item})"


class Level:
    def __init__(self, level_name: str, level_no: int, towers: list, theme: str):
        self.level_name = level_name
        self.level_no = level_no
        self.towers = towers
        self.theme = theme

    def is_completed(self):
        for tower in self.towers:
            if tower.is_completed() == False:
                return False
        return True

    def __str__(self):
        return f"Level (Name: {self.level_name} / No: {self.level_no} / theme: {self.theme})\nTowers: {self.towers}"


class Tower:
    def __init__(self, floors: list):
        self.floors = floors

    def is_completed(self):
        for floor in self.floors:
            if floor.is_completed() == False:
                return False
        return True

    def __str__(self):
        return f"Tower (Floors: {self.floors})"


class Floor:
    def __init__(self, entities: list):
        self.entities = entities

    def remove_entity(self, index: int):
        self.entities.pop(index)

    def is_completed(self):
        return len(self.entities) == 0

    def __str__(self):
        return f"Floor (Entities: {self.entities})"
