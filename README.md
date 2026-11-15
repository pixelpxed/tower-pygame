# Tower Game

A small tower-climbing game built with Python and pygame. The game
shows multiple towers on a shared map. Each tower contains floors with one
enemy per floor; clear every floor in one tower to unlock the next one.

## Run

```bash
python -m pip install -r requirements.txt
python main.py
```

Run it from the project root (asset paths are relative to it).

## Game flow

`Menu (START)` -> `Story` -> `CutScene` -> `Tower map / battles` -> `Ending`

* Win every tower -> **EndWinScene** (good ending) -> menu.
* Lose a battle with lives left -> **DEFEATED** screen (↺ back to the tower, 🏠 menu).
* Lose all lives (or lose to a boss) -> **EndLostScene** (bad ending) -> menu.

## Battle rules

Each battle compares your doable damage with the enemy's power; you must exceed
it to win. Victories add enemy power and replace your item. A normal loss costs
one life, while a boss loss ends the run. Stick reduces damage to 90% of power
and lightsaber increases it to 110%. Attacks are animated with the sprite
sheets in `assets/player` and `assets/enemy`.

## Project layout

| Path | What it is |
| --- | --- |
| `game/game.py` | Game loop, flow between scenes, battle resolution |
| `game/entities`, `game/systems`, `data/` | Battle system (power / items / boss) |
| `game/scenes/tower.py` | Tower map + attack animation |
| `game/scenes/story.py`, `cut_scene.py`, `end_win.py`, `end_lost.py`, `game_over.py`, `menu.py` | Story, cutscene, endings, menus |
| `game/scenes/image`, `game/scenes/soundeffect` | Scene art and sounds |
| `ui/` | HUD, buttons, hearts, power pill |
| `assets/` | Player / enemy sprite sheets (+ `sprite_demo.py`, `preview.gif`) |
| `new/` | Command-line prototype of the battle rules (`python new/cmdline.py`) |
| `legacy/` | Old code kept for reference only (not imported): HP/potion/gold battle and the old GIF cutscene/menu |

The game data lives in `data/`. Add art and audio under `assets/` without
changing the game systems.
