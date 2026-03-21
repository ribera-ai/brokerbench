"""Shared utilities for the BrokerBench evaluation harness."""

from __future__ import annotations

import re

# Regex patterns for MCQ answer extraction, tried in order:
# 1. Markdown-bold letter at start of text (e.g. "**B**", "**B.**")
# 2. Standalone letter at the very start of the text (e.g. "B", "B.", "B)")
# 3. Common answer prefix patterns like "Answer: B", "The answer is B"
# 4. Standalone letter on its own line
# 5. Markdown-bold letter anywhere (e.g. "The answer is **B**")
# 6. Bare letter followed by punctuation (fallback)
_MCQ_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"^\s*\*{1,2}([A-Da-d])\b", re.MULTILINE),
    re.compile(r"^\s*([A-Da-d])\s*[\.\)\:]", re.MULTILINE),
    re.compile(r"^\s*([A-Da-d])\s*$", re.MULTILINE),
    re.compile(r"(?:answer|choice|option)\s*(?:is|:)\s*([A-Da-d])\b", re.IGNORECASE),
    re.compile(r"\*{1,2}([A-Da-d])\*{1,2}"),
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
