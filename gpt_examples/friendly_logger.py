"""Friendly logger that prints color-coded, emoji-rich messages.

The output is meant to delight young makers while still carrying
useful hints for mentors (via the optional ``extra`` field).
"""
from __future__ import annotations

import datetime
from typing import Literal

Color = Literal["blue", "green", "yellow", "red", "magenta", "cyan", "gray", "white"]

EMOJI = {
    "info": "ℹ️",
    "move": "🚗",
    "sensor": "🛰️",
    "audio": "🎵",
    "success": "✅",
    "warning": "⚠️",
    "error": "❌",
    "chat": "💬",
}

ANSI = {
    "blue": "\033[94m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "gray": "\033[90m",
    "white": "\033[97m",
    "reset": "\033[0m",
}


def friendly_log(
    category: str,
    message: str,
    color: Color = "white",
    extra: str | None = None,
    *,
    timestamp: bool = True,
) -> None:
    """Print a playful log entry with emoji and colour."""

    emoji = EMOJI.get(category, EMOJI["info"])
    color_code = ANSI.get(color, ANSI["white"])
    time_part = datetime.datetime.now().strftime("%H:%M:%S") if timestamp else ""

    line = f"{emoji} {message}"
    if time_part:
        line = f"[{time_part}] {line}"
    if extra:
        line = f"{line} ({extra})"

    print(f"{color_code}{line}{ANSI['reset']}")


__all__ = ["friendly_log"]
