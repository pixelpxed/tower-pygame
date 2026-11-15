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

The game data lives in `data/`. Add art and audio under `assets/` without
changing the game systems.