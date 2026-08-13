from __future__ import annotations

import math
import random

from .models import Character, Choice, Quiz
from .prompts import safe_input
from .settings import load_settings
from .text_utils import pause, print_line, print_wrapped, terminal_width

TOP_RESULTS_SHOWN = 10


def _vector(profile: dict[str, int], attributes: list[str]) -> list[float]:
    return [float(profile.get(attr, 0)) for attr in attributes]


def cosine_similarity(a: dict[str, int], b: dict[str, int], attributes: list[str]) -> float:
    va = _vector(a, attributes)
    vb = _vector(b, attributes)
    dot = sum(x * y for x, y in zip(va, vb))
    norm_a = math.sqrt(sum(x * x for x in va))
    norm_b = math.sqrt(sum(x * x for x in vb))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def ask_question(
    index: int,
    total: int,
    text: str,
    choices: list[Choice],
    width: int,
    word_wrap: bool,
    typewriter: bool = False,
) -> Choice | None:
    """Ask one question. Returns the chosen Choice, or None if the user typed
    'undo' to go back to the previous question."""
    print()
    header = f"Q{index}/{total}. "
    print_wrapped(
        text, width, indent=header, subsequent_indent=" " * len(header), wrap=word_wrap, typewriter=typewriter
    )
    for i, choice in enumerate(choices, start=1):
        prefix = f"  {i}. "
        print_wrapped(
            choice.text, width, indent=prefix, subsequent_indent=" " * len(prefix), wrap=word_wrap, line_reveal=typewriter
        )
    while True:
        raw = safe_input("Your answer (or 'undo' to go back): ").strip()
        if raw.lower() == "undo":
            return None
        if raw.isdigit() and 1 <= int(raw) <= len(choices):
            return choices[int(raw) - 1]
        print(f"Please enter a number between 1 and {len(choices)}, or 'undo'.")


def score_quiz(quiz: Quiz, user_vector: dict[str, int]) -> list[tuple[Character, float]]:
    results = [
        (char, cosine_similarity(user_vector, char.profile, quiz.attributes) * 100)
        for char in quiz.characters
    ]
    results.sort(key=lambda pair: pair[1], reverse=True)
    return results


def print_results(
    results: list[tuple[Character, float]], width: int, word_wrap: bool = True, typewriter: bool = False
) -> None:
    print("\n" + "=" * 50)
    print("RESULTS — how closely you match each character")
    print("=" * 50)
    pause(typewriter)
    shown = results[:TOP_RESULTS_SHOWN]
    for char, pct in shown:
        bar = "#" * round(pct / 5)
        print_line(f"{char.name:<20} {pct:5.1f}%  {bar}", animate=typewriter)

    remaining = len(results) - len(shown)
    if remaining > 0:
        plural = "s" if remaining != 1 else ""
        print(f"... and {remaining} more character{plural} (truncated)")

    if not results:
        return

    top_char, top_pct = results[0]
    print("\n" + "-" * 50)
    print_wrapped(
        f"You are closest to: {top_char.name} ({top_pct:.1f}% match)", width, wrap=word_wrap, typewriter=typewriter
    )
    if top_char.description:
        print_wrapped(top_char.description, width, wrap=word_wrap, typewriter=typewriter)

    runners_up = [
        (char, pct) for char, pct in results[1:]
        if top_pct - pct <= 5 and pct > 0
    ]
    if runners_up:
        names = ", ".join(f"{c.name} ({p:.1f}%)" for c, p in runners_up)
        print_wrapped(f"(Close runner-up: {names})", width, wrap=word_wrap)


def run_quiz(quiz: Quiz) -> None:
    settings = load_settings()
    width = terminal_width()

    print()
    print_wrapped(quiz.title, width, wrap=settings.word_wrap)
    if quiz.description:
        print_wrapped(quiz.description, width, wrap=settings.word_wrap)
    if settings.typewriter_animation:
        safe_input("\nPress Enter to continue...")

    user_vector: dict[str, int] = {attr: 0 for attr in quiz.attributes}

    questions = list(quiz.questions)
    if settings.shuffle_questions:
        random.shuffle(questions)

    # Shuffle each question's choices once up front, so undoing back to a
    # question shows the same choice order it had the first time.
    choice_sets: list[list[Choice]] = []
    for question in questions:
        choices = list(question.choices)
        if settings.shuffle_answers:
            random.shuffle(choices)
        choice_sets.append(choices)

    answers: list[Choice | None] = [None] * len(questions)

    i = 0
    while i < len(questions):
        question = questions[i]
        choices = choice_sets[i]

        chosen = ask_question(
            i + 1, len(questions), question.text, choices, width, settings.word_wrap, settings.typewriter_animation
        )

        if chosen is None:
            if i == 0:
                print("Nothing to undo yet.")
                continue
            i -= 1
            prev_choice = answers[i]
            if prev_choice is not None:
                for attr, value in prev_choice.points.items():
                    user_vector[attr] = user_vector.get(attr, 0) - value
            answers[i] = None
            print(f"  Undid your answer to Q{i + 1}.")
            continue

        answers[i] = chosen
        for attr, value in chosen.points.items():
            user_vector[attr] = user_vector.get(attr, 0) + value

        if settings.show_points_on_answer and chosen.points:
            deltas = ", ".join(
                f"+{v} {attr}" if v >= 0 else f"{v} {attr}"
                for attr, v in chosen.points.items()
            )
            print(f"  ({deltas})")

        if settings.show_live_closest_character:
            live_results = score_quiz(quiz, user_vector)
            if live_results and live_results[0][1] > 0:
                leader, leader_pct = live_results[0]
                print(f"  Currently closest to: {leader.name} ({leader_pct:.1f}%)")

        i += 1

    results = score_quiz(quiz, user_vector)
    print_results(results, width, word_wrap=settings.word_wrap, typewriter=settings.typewriter_animation)
