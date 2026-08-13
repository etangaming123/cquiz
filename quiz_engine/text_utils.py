from __future__ import annotations

import shutil
import sys
import textwrap
import time

from .prompts import ReturnToMenu

DEFAULT_WIDTH = 80
MIN_WIDTH = 20

# Typewriter animation speed. Adjust here (not in settings.json) — the
# settings page only exposes an on/off toggle.
TYPEWRITER_CHARS_PER_SECOND = 50

# Delay between each revealed line (answer choices), in seconds.
LINE_REVEAL_DELAY_SECONDS = 0.8


def terminal_width() -> int:
    """Current terminal width, re-checked on every call so a resized window is picked up."""
    return shutil.get_terminal_size((DEFAULT_WIDTH, 24)).columns


def _pause() -> None:
    try:
        time.sleep(LINE_REVEAL_DELAY_SECONDS)
    except KeyboardInterrupt:
        print()
        raise ReturnToMenu()


def _type_out(line: str) -> None:
    delay = 1.0 / TYPEWRITER_CHARS_PER_SECOND
    try:
        for ch in line:
            sys.stdout.write(ch)
            sys.stdout.flush()
            time.sleep(delay)
    except KeyboardInterrupt:
        print()
        raise ReturnToMenu()
    sys.stdout.write("\n")
    sys.stdout.flush()
    _pause()


def _reveal_line(line: str) -> None:
    """Print the whole line at once, then hold for a static beat before the next
    one — unlike _type_out, each line pops in instantly instead of character by
    character."""
    print(line)
    _pause()


def print_line(text: str, animate: bool = False) -> None:
    """Print one already-formatted line (e.g. a results table row), optionally
    revealed with a pause before whatever prints next."""
    if animate:
        _reveal_line(text)
    else:
        print(text)


def print_wrapped(
    text: str,
    width: int,
    indent: str = "",
    subsequent_indent: str | None = None,
    wrap: bool = True,
    typewriter: bool = False,
    line_reveal: bool = False,
) -> None:
    if subsequent_indent is None:
        subsequent_indent = indent
    if not text:
        print(indent.rstrip())
        return
    if wrap:
        lines = textwrap.wrap(
            text,
            width=max(MIN_WIDTH, width),
            initial_indent=indent,
            subsequent_indent=subsequent_indent,
        )
    else:
        lines = [f"{indent}{text}"]

    for line in lines:
        if typewriter:
            _type_out(line)
        elif line_reveal:
            _reveal_line(line)
        else:
            print(line)
