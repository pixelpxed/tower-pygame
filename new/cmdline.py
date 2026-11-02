try:
    from .classes import Enemy, Floor, Level, Player, Tower
except ImportError:
    from classes import Enemy, Floor, Level, Player, Tower


def create_level():
    return Level(
        "First Level",
        1,
        [
            Tower([Floor([Enemy("enemy", 3, None)])]),
            Tower(
                [Floor([Enemy("enemy", 3, "stick")]), Floor([Enemy("enemy", 3, None)])]
            ),
            Tower(
                [
                    Floor([Enemy("enemy", 3, "lightsaber")]),
                    Floor([Enemy("enemy", 10, None)]),
                    Floor([Enemy("boss", 16, None)]),
                ]
            ),
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
