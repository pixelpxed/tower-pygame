from classes import Enemy, Floor, Level, Player, Tower


def create_level():
    return Level(
        "First Level",
        1,
        [
            Tower([
                Floor([Enemy("enemy", 8, None)]),
                Floor([Enemy("enemy", 4, None)]),
                Floor([Enemy("enemy", 6, None)]),
                Floor([Enemy("enemy", 15, None)]),
                Floor([Enemy("enemy", 84, None)]),
                Floor([Enemy("enemy", 42, None)]),
                Floor([Enemy("enemy", 19, "stick")]),
            ]),
            Tower([
                Floor([Enemy("enemy", 15, None), Enemy("enemy", 6, None)]),
                Floor([Enemy("enemy", 14, "lightsaber")]),
                Floor([Enemy("enemy", 42, None)]),
                Floor([Enemy("enemy", 23, None)]),
                Floor([Enemy("enemy", 14, "stick")]),
                Floor([Enemy("enemy", 47, None)]),
                Floor([Enemy("enemy", 99, None)]),
            ]),
            Tower([
                Floor([Enemy("enemy", 85, "lightsaber"), Enemy("enemy", 25, None)]),
                Floor([Enemy("enemy", 34, None), Enemy("enemy", 12, None)]),
                Floor([Enemy("enemy", 99, None)]),
                Floor([Enemy("enemy", 215, None)]),
                Floor([Enemy("enemy", 69, None)]),
                Floor([Enemy("enemy", 452, None)]),
                Floor([Enemy("enemy", 46, None)]),
                Floor([Enemy("enemy", 420, None)]),
            ]),
            Tower([
                Floor([Enemy("enemy", 334, None)]),
                Floor([Enemy("enemy", 452, None)]),
                Floor([Enemy("enemy", 215, None)]),
                Floor([Enemy("enemy", 69, None)]),
                Floor([Enemy("enemy", 85, None)]),
                Floor([Enemy("enemy", 46, None)]),
                Floor([Enemy("enemy", 426, None)]),
                Floor([Enemy("enemy", 840, None)]),
                Floor([Enemy("boss", 4680, None)]),
            ]),
        ],
        "default",
    )


def display_level(level):
    print("\nCurrent Enemies:\n")
    for tower_index, tower in enumerate(level.towers, 1):
        print(f"Tower {tower_index}:")
        if tower.is_completed():
            print(" - This tower has been defeated.")
        else:
            for floor_index, floor in enumerate(tower.floors, 1):
                if floor.is_completed():
                    print(f" - Floor {floor_index} defeated")
                else:
                    for enemy in floor.entities:
                        print(f" - Floor {floor_index}: {enemy}")
    print()


def main():
    player = Player((0, 0), 5, 3, None)
    level = create_level()

    while player.get_lives() > 0 and not level.is_completed():
        display_level(level)
        print(
            f"Your Power: {player.get_power()}, Lives: {player.get_lives()}, Item: {player.get_item()}\nDoable Damage: {player.get_doable_damage()}"
        )
        print("\n========================================\n")

        try:
            selection = (
                input("Input your attack position (tower floor, e.g. 1 1): ")
                .strip()
                .split()
            )
            if len(selection) != 2:
                raise ValueError
            tower_index, floor_index = (int(value) - 1 for value in selection)
            if tower_index < 0 or floor_index < 0:
                raise IndexError
            floor = level.towers[tower_index].floors[floor_index]
            if floor.is_completed():
                print("That floor has already been defeated.")
                continue
        except (ValueError, IndexError):
            print("Enter a valid tower and floor number, such as 1 1.")
            continue
        except (EOFError, KeyboardInterrupt):
            print("\nGame ended.")
            return

        player.set_position((tower_index, floor_index))
        enemy = floor.entities[0]
        print()

        if player.get_doable_damage() > enemy.get_power():
            player.add_power(enemy.get_power())
            player.set_item(enemy.get_item())
            floor.remove_entity(0)
            print(f"Player won the battle at {(tower_index + 1, floor_index + 1)}")
        else:
            if enemy.get_kind() == "boss":
                print("You fought a boss and lost, you died instantly!")
                player.set_lives(0)
            else:
                player.remove_life()
            print(f"Player lost a battle at {(tower_index + 1, floor_index + 1)}")
            player.set_position((0, 0))

        print("\n========================================\n")

    print("Game Over!\n" if player.get_lives() <= 0 else "\nLevel Cleared!\n")


if __name__ == "__main__":
    main()
