from __future__ import annotations

from .prompts import safe_input
from .settings import Settings, load_settings, save_settings

TOGGLES = [
    ("word_wrap", "Word wrap (wrap text to terminal width)"),
    ("shuffle_questions", "Shuffle question order"),
    ("shuffle_answers", "Shuffle answer choice order"),
    ("show_points_on_answer", "Show points added to each attribute after answering"),
    ("show_live_closest_character", "Show current closest character after each question"),
    ("typewriter_animation", "Typewriter animation for quiz question text"),
]


def _print_settings(settings: Settings) -> None:
    print("\n=== Settings ===")
    for i, (attr, label) in enumerate(TOGGLES, start=1):
        state = "ON " if getattr(settings, attr) else "OFF"
        print(f"  {i}. [{state}] {label}")
    print("  (enter a number to toggle, blank to go back)")


def settings_menu() -> None:
    settings = load_settings()
    while True:
        _print_settings(settings)
        choice = safe_input("> ").strip().lower()
        if choice in ("", "b"):
            return
        if choice.isdigit() and 1 <= int(choice) <= len(TOGGLES):
            attr, _ = TOGGLES[int(choice) - 1]
            setattr(settings, attr, not getattr(settings, attr))
            save_settings(settings)
        else:
            print(f"Enter a number 1-{len(TOGGLES)} to toggle, or press Enter to go back.")
