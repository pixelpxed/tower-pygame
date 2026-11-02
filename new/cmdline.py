player_power = 5
player_lives = 3
player_position = (0, 0)

level = [
    [
        {"type": "enemy", "power": 3},
    ],
    [
        {"type": "enemy", "power": 3},
        {"type": "enemy", "power": 3},
    ],
    [
        {"type": "enemy", "power": 3},
        {"type": "enemy", "power": 10},
        {"type": "boss", "power": 16},
    ],
]


def display_level():
    print("\nCurrent Enemies:\n")
    for i in range(len(level)):
        print(f"Tower {i + 1}:")

        if len(level[i]) == 0:
            print(" - This tower has been defeated.")
        else:
            for j in range(len(level[i])):
                print(f" - Floor {j + 1}: {level[i][j]}")
    print()


while True:
    if player_lives <= 0:
        print("\nGame Over!\n")
        break

    if len(level) == 0:
        print("\nLevel Cleared!\n")
        break

    display_level()
    print(f"Your Power: {player_power}, Lives: {player_lives}")

    print("\n========================================\n")

    attack_tower, attack_floor = input(
        "Input your attack postion (tower_index, floor_index ex. 1 1): "
    ).strip().split()

    # Normalize the variable to start at Python index. (0)
    attack_tower, attack_floor = [int(attack_tower) - 1, int(attack_floor) - 1]

    # Fighting Calculation
    print()  # Seperator Line
    if player_power > level[attack_tower][attack_floor]["power"]:
        dead_enemy = level[attack_tower].pop(attack_floor)
        player_power += dead_enemy["power"]
        print(f"Player won the battle at {(attack_tower, attack_floor)}")

        if len(level[attack_tower]) == 0:
            level.pop(attack_tower)
    else:
        if level[attack_tower][attack_floor]["type"] == "boss":
            print(f"You fought a boss and lost, you died instantly!")
            player_lives = 0
        print(f"Player lost a battle at {(attack_tower, attack_floor)}")
        player_lives -= 1
        player_position = (0, 0)

    print("\n========================================\n")
