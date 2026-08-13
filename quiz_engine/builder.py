from __future__ import annotations

from pathlib import Path

from .loader import QUIZZES_DIR, save_quiz
from .models import Character, Choice, Question, Quiz
from .prompts import safe_input


def _prompt_int(prompt: str, default: int = 0) -> int:
    raw = safe_input(prompt).strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        print(f"  Not a number, using {default}.")
        return default


def _collect_attributes() -> list[str]:
    print("\nDefine the attributes (personality traits) characters will be scored on.")
    print("Example: bravery, wit, kindness, ambition")
    raw = safe_input("Attributes (comma-separated): ").strip()
    attributes = [a.strip() for a in raw.split(",") if a.strip()]
    while not attributes:
        print("Need at least one attribute.")
        raw = safe_input("Attributes (comma-separated): ").strip()
        attributes = [a.strip() for a in raw.split(",") if a.strip()]
    return attributes


def _collect_profile(attributes: list[str], label: str) -> dict[str, int]:
    print(f"  Rate {label} on each attribute (suggested scale 0-5, blank = 0):")
    profile = {}
    for attr in attributes:
        value = _prompt_int(f"    {attr}: ", default=0)
        if value:
            profile[attr] = value
    return profile


def _collect_characters(attributes: list[str]) -> list[Character]:
    print("\nAdd characters (leave id blank to finish).")
    characters: list[Character] = []
    while True:
        char_id = safe_input("\nCharacter id (short slug, e.g. 'hero'): ").strip()
        if not char_id:
            break
        name = safe_input("Display name: ").strip() or char_id
        description = safe_input("Description: ").strip()
        profile = _collect_profile(attributes, name)
        characters.append(Character(id=char_id, name=name, description=description, profile=profile))
    while len(characters) < 2:
        print("Need at least 2 characters to make a meaningful quiz.")
        char_id = safe_input("\nCharacter id: ").strip()
        if not char_id:
            continue
        name = safe_input("Display name: ").strip() or char_id
        description = safe_input("Description: ").strip()
        profile = _collect_profile(attributes, name)
        characters.append(Character(id=char_id, name=name, description=description, profile=profile))
    return characters


def _collect_choices(attributes: list[str]) -> list[Choice]:
    choices: list[Choice] = []
    print("  Add answer choices (leave choice text blank to finish, need at least 2).")
    while True:
        text = safe_input("  Choice text: ").strip()
        if not text:
            if len(choices) >= 2:
                break
            print("  Need at least 2 choices.")
            continue
        points = {}
        for attr in attributes:
            value = _prompt_int(f"    points for {attr} (blank = 0): ", default=0)
            if value:
                points[attr] = value
        choices.append(Choice(text=text, points=points))
    return choices


def _collect_questions(attributes: list[str]) -> list[Question]:
    print("\nAdd questions (leave question text blank to finish).")
    questions: list[Question] = []
    while True:
        text = safe_input("\nQuestion text: ").strip()
        if not text:
            if questions:
                break
            print("Need at least 1 question.")
            continue
        choices = _collect_choices(attributes)
        questions.append(Question(text=text, choices=choices))
    return questions


def build_quiz_interactive() -> Path | None:
    print("\n=== Create a new character quiz ===")
    title = safe_input("Quiz title: ").strip()
    if not title:
        print("Title required. Cancelled.")
        return None
    description = safe_input("Quiz description: ").strip()

    attributes = _collect_attributes()
    characters = _collect_characters(attributes)
    questions = _collect_questions(attributes)

    quiz = Quiz(
        title=title,
        description=description,
        attributes=attributes,
        characters=characters,
        questions=questions,
    )

    default_name = title.lower().replace(" ", "_").strip("_") or "my_quiz"
    filename = safe_input(f"\nSave as filename [{default_name}.json]: ").strip() or f"{default_name}.json"
    if not filename.endswith(".json"):
        filename += ".json"

    out_path = QUIZZES_DIR / filename
    save_quiz(quiz, out_path)
    print(f"\nSaved quiz to {out_path}")
    return out_path
