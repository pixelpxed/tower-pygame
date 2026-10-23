"""Shared game configuration."""

from pathlib import Path

WIDTH = 960
HEIGHT = 640
FPS = 60
TITLE = "Tower Game"
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

COLORS = {
    "background": (20, 24, 38),
    "panel": (38, 44, 65),
    "text": (242, 241, 230),
    "muted": (165, 172, 193),
    "accent": (235, 180, 68),
    "danger": (214, 77, 77),
    "success": (86, 190, 116),
}