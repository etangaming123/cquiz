from __future__ import annotations


class ReturnToMenu(Exception):
    """Raised when the user hits Ctrl+C on a prompt to bail back to the main menu."""


def safe_input(prompt: str = "") -> str:
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print()
        raise ReturnToMenu()
