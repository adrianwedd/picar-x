#!/usr/bin/env python3
"""Announce the time aloud at the top of every hour between 08:00 and 19:00.

Run this script on the PiCar-X with sudo so the Robot HAT speaker is available:

    sudo python3 scripts/hourly_chime.py

The script uses the Robot HAT TTS engine; adjust the messages or schedule
window below as needed.
"""

from __future__ import annotations

import sys
import time
from datetime import datetime, timedelta

from robot_hat import TTS

START_HOUR = 8   # inclusive, 24-hour clock
END_HOUR = 19    # inclusive, 24-hour clock


def format_timestamp(ts: datetime) -> str:
    hour = ts.hour % 12 or 12
    suffix = "AM" if ts.hour < 12 else "PM"
    return f"It's {hour} {suffix}."


def next_trigger(after: datetime) -> datetime:
    candidate = after.replace(minute=0, second=0, microsecond=0)
    if after.minute > 0 or after.second > 0 or after.microsecond > 0:
        candidate += timedelta(hours=1)

    while True:
        if candidate.hour < START_HOUR:
            candidate = candidate.replace(hour=START_HOUR)
        elif candidate.hour > END_HOUR:
            candidate = (candidate + timedelta(days=1)).replace(
                hour=START_HOUR, minute=0, second=0, microsecond=0
            )
        else:
            break
    return candidate


def sleep_until(target: datetime) -> None:
    while True:
        now = datetime.now()
        remaining = (target - now).total_seconds()
        if remaining <= 0:
            break
        time.sleep(min(remaining, 60))


def main() -> int:
    tts = TTS()
    tts.lang("en-US")

    print(
        f"Hourly chime active between {START_HOUR:02d}:00 and {END_HOUR:02d}:00."
        " Press Ctrl+C to exit."
    )

    next_time = next_trigger(datetime.now())

    try:
        while True:
            sleep_until(next_time)
            # speak only if within the window (guards against race conditions)
            now = datetime.now().replace(second=0, microsecond=0)
            if START_HOUR <= now.hour <= END_HOUR:
                phrase = format_timestamp(now)
                print(f"{now:%Y-%m-%d %H:%M:%S} -> {phrase}")
                tts.say(phrase)
            next_time = next_trigger(now + timedelta(seconds=1))
    except KeyboardInterrupt:
        print("\nHourly chime stopped.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
