from __future__ import annotations

import json
from dataclasses import asdict, dataclass, fields
from pathlib import Path

SETTINGS_PATH = Path(__file__).resolve().parent.parent / "settings.json"


@dataclass
class Settings:
    word_wrap: bool = True
    shuffle_questions: bool = False
    shuffle_answers: bool = False
    show_points_on_answer: bool = False
    show_live_closest_character: bool = False
    typewriter_animation: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Settings":
        known = {f.name for f in fields(Settings)}
        filtered = {k: v for k, v in data.items() if k in known}
        return Settings(**filtered)


def load_settings() -> Settings:
    if not SETTINGS_PATH.exists():
        return Settings()
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return Settings()
    return Settings.from_dict(data)


def save_settings(settings: Settings) -> None:
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings.to_dict(), f, indent=2)
        f.write("\n")
