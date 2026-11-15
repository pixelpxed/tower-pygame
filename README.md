# Tower Game

A small tower-climbing game built with Python and pygame. The game
shows multiple towers on a shared map. Each tower contains floors with one
enemy per floor; clear every floor in one tower to unlock the next one. The
prototype uses drawn shapes and system fonts, so it runs before optional image,
audio, and font assets are added.

## Run

```bash
python -m pip install -r requirements.txt
python main.py
```

Each battle compares your doable damage with the enemy’s power; you must exceed it to win. Victories add enemy power and replace your item. A normal loss costs one life, while a boss loss ends the run. Stick reduces damage to 90% of power and lightsaber increases it to 110%.

The game data lives in `data/`. Add art and audio under `assets/` without
changing the game systems.