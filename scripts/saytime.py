#!/usr/bin/env python3
"""Speak the current time once using the Robot HAT text-to-speech engine.

Usage:
    sudo python3 scripts/saytime.py

Optional arguments:
    --lang CODE   Set TTS language code (default: en-US)
    --prefix TXT  Prepend custom text before the time (e.g., "The time is")
"""

import argparse
from datetime import datetime

from robot_hat import TTS


def format_phrase(prefix: str, timestamp: datetime) -> str:
    hour = timestamp.hour % 12 or 12
    minute = timestamp.minute
    suffix = "AM" if timestamp.hour < 12 else "PM"
    time_part = f"{hour}:{minute:02d} {suffix}"
    prefix = prefix.strip()
    if prefix:
        if not prefix.endswith((" ", "\t")):
            prefix += " "
        return f"{prefix}{time_part}."
    return f"It's {time_part}."


def main() -> int:
    parser = argparse.ArgumentParser(description="Speak the current time once")
    parser.add_argument("--lang", default="en-US", help="TTS language code")
    parser.add_argument("--prefix", default="It's", help="Intro text before the time")
    args = parser.parse_args()

    tts = TTS()
    tts.lang(args.lang)

    now = datetime.now()
    phrase = format_phrase(args.prefix, now)
    print(f"Announcing: {phrase}")
    tts.say(phrase)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
