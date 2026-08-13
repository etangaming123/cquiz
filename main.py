from __future__ import annotations

import math

from quiz_engine.builder import build_quiz_interactive
from quiz_engine.loader import list_quizzes, load_quiz
from quiz_engine.prompts import ReturnToMenu, safe_input
from quiz_engine.runner import run_quiz
from quiz_engine.settings_menu import settings_menu

PAGE_SIZE = 10


def _quiz_titles(paths):
    titles = []
    for path in paths:
        try:
            titles.append(load_quiz(path).title or path.stem)
        except Exception:
            titles.append(f"{path.stem} (invalid quiz file)")
    return titles


def choose_quiz():
    quizzes = list_quizzes()
    if not quizzes:
        print("No quizzes found in quizzes/ yet. You should create one first - read the README.md for instructions.")
        return None
    titles = _quiz_titles(quizzes)
    total_pages = max(1, math.ceil(len(quizzes) / PAGE_SIZE))
    page = 0

    while True:
        start = page * PAGE_SIZE
        page_items = list(enumerate(zip(quizzes, titles), start=1))[start : start + PAGE_SIZE]

        if total_pages > 1:
            print(f"\nAvailable quizzes ({len(quizzes)} total, page {page + 1}/{total_pages}):")
        else:
            print(f"\nAvailable quizzes ({len(quizzes)} total):")
        for i, (path, title) in page_items:
            print(f"  {i}. {title}")

        nav = []
        if page > 0:
            nav.append("< prev page")
        if page < total_pages - 1:
            nav.append("> next page")
        hint = f" ({', '.join(nav)})" if nav else ""
        raw = safe_input(f"Pick a quiz number{hint}, or blank to cancel: ").strip()

        if not raw:
            return None
        if raw == "<":
            if page > 0:
                page -= 1
            else:
                print("Already on the first page.")
            continue
        if raw == ">":
            if page < total_pages - 1:
                page += 1
            else:
                print("Already on the last page.")
            continue
        if not raw.isdigit() or not (1 <= int(raw) <= len(quizzes)):
            print("Invalid choice.")
            continue
        return quizzes[int(raw) - 1]


def main() -> None:
    print("=== etan's character quiz ===")
    while True:
        print("\nWhat would you like to do?")
        print("  1. Take a quiz")
        print("  2. Create a new quiz")
        print("  3. Settings")
        print("  4. Quit")
        try:
            choice = input("> ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

        try:
            if choice == "1":
                path = choose_quiz()
                if path is not None:
                    quiz = load_quiz(path)
                    run_quiz(quiz)
            elif choice == "2":
                build_quiz_interactive()
            elif choice == "3":
                settings_menu()
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Please enter 1, 2, 3, or 4.")
        except ReturnToMenu:
            print("\nReturning to main menu.")


if __name__ == "__main__":
    main()
