"""Shared utilities for the BrokerBench evaluation harness."""

from __future__ import annotations

import re

# Regex patterns for MCQ answer extraction, tried in order:
# 1. Standalone letter at the very start of the text (e.g. "B", "B.", "B)")
# 2. Common answer prefix patterns like "Answer: B", "The answer is B"
# 3. Standalone letter on its own line
_MCQ_PATTERNS: list[re.Pattern[str]] = [
    # Markdown-bold letter at the start: **B**, **B.**, **B)**
    re.compile(r"^\s*\*\*([A-Da-d])\*\*", re.MULTILINE),
    re.compile(r"^\s*([A-Da-d])\s*[\.\)\:]", re.MULTILINE),
    re.compile(r"^\s*([A-Da-d])\s*$", re.MULTILINE),
    re.compile(
        r"(?:answer|choice|option)\s*(?:is|:)\s*\*?\*?([A-Da-d])\*?\*?",
        re.IGNORECASE,
    ),
    re.compile(r"\b([A-Da-d])\s*[\.\)\:]"),
]


def extract_mcq_answer(text: str) -> str | None:
    """Extract a single MCQ answer letter (A-D) from model output.

    Uses a series of regex patterns to find the answer letter,
    avoiding false positives from letters embedded in English words.

    Args:
        text: The raw model output text.

    Returns:
        An uppercase letter ``"A"``–``"D"`` if found, otherwise ``None``.
    """
    text = text.strip()
    if not text:
        return None

    # If the text is already a single letter, return it directly
    if len(text) == 1 and text.upper() in "ABCD":
        return text.upper()

    for pattern in _MCQ_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group(1).upper()

    return None
