from __future__ import annotations

import json
from pathlib import Path

from .models import Quiz

QUIZZES_DIR = Path(__file__).resolve().parent.parent / "quizzes"


def list_quizzes() -> list[Path]:
    if not QUIZZES_DIR.exists():
        return []
    return sorted(QUIZZES_DIR.glob("*.json"))


def load_quiz(path: Path) -> Quiz:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Quiz.from_dict(data)


def save_quiz(quiz: Quiz, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(quiz.to_dict(), f, indent=2)
        f.write("\n")
