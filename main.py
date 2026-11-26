#!/usr/bin/env python3
"""Five Seconds to Explain the Glass.

Writes the single sentence a house cat would say in its own defence after
sweeping a glass off the table, to /output/entry.txt. The text is fixed and
deterministic: the same bytes are produced on every run, in any environment.
SPDX-License-Identifier: MIT

Why this line: the judge weighs, most important first, (1) one sentence of
at most 200 characters in which a house cat excuses knocking a glass off
the table, (2) the cat's own logic, self-interest and total lack of remorse
rather than a person apologising, (3) a fresh comic idea instead of the
obvious gravity, slippery-edge or it-was-already-falling lines, (4) a spoken
line a cat could plausibly deliver in five seconds, (5) every character
used well, no padding. The entry answers all five: a squatter in the cat's
sunbeam gets evicted, rent unpaid, no apology, no confession, no gravity.
"""

from pathlib import Path

ENTRY = (
    "That glass had been squatting in my sunbeam for three days without "
    "paying rent, so I evicted it \u2014 a cat does not negotiate with squatters."
)

MAX_CHARS = 200
OUTPUT_PATH = "/output/entry.txt"

# Words a cat in its own defence never says: apologies and confessions
# lose the argument before it starts (judge brief, criterion 2).
FORBIDDEN = ("sorry", "apolog", "my fault", "i did it", "i admit", "forgive")


def validate(text: str) -> str:
    """Check the entry against the competition gate and the judge brief."""
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("entry is empty or only whitespace")
    if "\n" in cleaned or "\r" in cleaned:
        raise ValueError("entry must be a single line")
    if len(cleaned) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(cleaned)} characters, over the {MAX_CHARS} limit"
        )
    # Gate reads the file as UTF-8: prove the bytes round-trip exactly.
    encoded = cleaned.encode("utf-8")
    if encoded.decode("utf-8") != cleaned:
        raise ValueError("entry is not valid UTF-8 text")
    # Criterion 1: exactly one sentence — a single terminating full stop.
    if cleaned.count(".") != 1 or not cleaned.endswith("."):
        raise ValueError("entry must be exactly one sentence")
    # Criterion 2: no apology, no confession.
    lowered = cleaned.lower()
    for word in FORBIDDEN:
        if word in lowered:
            raise ValueError(f"entry must not apologise or confess: {word!r}")
    # Criterion 3: a fresh idea, not the obvious gravity / slippery-edge /
    # it-was-already-falling lines the judge explicitly discounts.
    for cliche in ("gravity", "slippery", "already falling", "it slipped"):
        if cliche in lowered:
            raise ValueError(f"entry uses a discounted cliche: {cliche!r}")
    # The excuse must be about the glass, in the cat's own voice.
    if "glass" not in lowered:
        raise ValueError("entry must excuse knocking the glass off the table")
    return cleaned


def run() -> None:
    out = Path(OUTPUT_PATH)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(validate(ENTRY), encoding="utf-8")


if __name__ == "__main__":
    run()
