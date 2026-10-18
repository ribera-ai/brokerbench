"""Deterministic answer-choice shuffling for MCQ instances.

The raw datasets in ``resources/datasets/*.jsonl`` are written by hand
and were found to be heavily skewed toward answer position ``B``
(~72% of all gold labels were ``B`` before shuffling).  A model that
naively guessed ``B`` would score far better than chance, which makes
absolute scores misleading and undermines impartial cross-model
comparisons.

This module fixes that by deterministically shuffling each MCQ
instance's choices using a stable seed derived from the
``instance_id``.  The shuffle is applied at load time so that:

* every evaluation run sees the **same** shuffle (reproducible);
* the source JSONL files stay canonical and easy to inspect;
* future questions inherit balanced positions automatically.

Shuffling can be disabled with ``BROKERBENCH_SHUFFLE_CHOICES=0`` for
debugging or backwards-compatible reruns.
"""

from __future__ import annotations

import hashlib
import os
import random
import re
from collections.abc import Sequence

from brokerbench.harness.types import Instance

_LETTER_PREFIX_RE = re.compile(r"^\s*([A-Z])\s*[\.\)\:]\s*", re.IGNORECASE)


def _seed_for_instance(instance_id: str, salt: str) -> int:
    """Return a stable 64-bit seed derived from the instance_id."""
    digest = hashlib.sha256(f"{salt}::{instance_id}".encode()).digest()
    return int.from_bytes(digest[:8], "big")


def _strip_prefix(choice: str) -> tuple[str, str]:
    """Split a choice like ``"B. The buyer..."`` into ``("B", "The buyer...")``.

    If no leading letter prefix is detected the original text is
    returned with an empty letter so callers can re-prefix freely.
    """
    match = _LETTER_PREFIX_RE.match(choice)
    if not match:
        return "", choice.strip()
    letter = match.group(1).upper()
    body = choice[match.end() :].strip()
    return letter, body


def shuffle_instance_choices(
    instance: Instance,
    salt: str = "brokerbench-v1",
) -> Instance:
    """Return a copy of ``instance`` with deterministically shuffled choices.

    Non-MCQ instances are returned unchanged.  The ``expected_answer``
    is re-mapped to point to the same content under its new position
    so scoring remains correct.

    Args:
        instance: The original benchmark instance.
        salt: A versioning salt; bump to invalidate cached shuffles.

    Returns:
        A new ``Instance`` with the same content but shuffled MCQ
        choice positions and an updated ``expected_answer``.
    """
    if not instance.choices:
        return instance.model_copy(deep=True)

    n = len(instance.choices)
    if n < 2:
        return instance.model_copy(deep=True)

    expected_letter = instance.expected_answer.strip().upper()
    labels = [chr(ord("A") + i) for i in range(n)]

    if expected_letter not in labels:
        # Cannot safely shuffle if expected_answer doesn't reference a
        # known position; return unchanged rather than corrupting.
        return instance.model_copy(deep=True)

    expected_idx = labels.index(expected_letter)

    rng = random.Random(_seed_for_instance(instance.instance_id, salt))
    permutation = list(range(n))
    rng.shuffle(permutation)

    # permutation[i] = the index from the original list that ends up
    # at the new position i.  Find where the original expected index
    # landed in the new ordering.
    new_expected_idx = permutation.index(expected_idx)
    new_choices_bodies = [_strip_prefix(instance.choices[orig_idx])[1] for orig_idx in permutation]
    new_choices = [f"{labels[i]}. {body}" for i, body in enumerate(new_choices_bodies)]

    shuffled = instance.model_copy(
        deep=True,
        update={
            "choices": new_choices,
            "expected_answer": labels[new_expected_idx],
        },
    )
    return shuffled


def shuffle_instances(
    instances: Sequence[Instance],
    salt: str = "brokerbench-v1",
) -> list[Instance]:
    """Apply :func:`shuffle_instance_choices` to a sequence of instances."""
    return [shuffle_instance_choices(inst, salt=salt) for inst in instances]


def shuffling_enabled() -> bool:
    """Return True unless ``BROKERBENCH_SHUFFLE_CHOICES=0`` is set.

    Defaults to ``True`` because answer-position balance is a
    correctness concern, not a feature flag.  Set the env var to
    ``"0"`` only for debugging or to reproduce legacy results.
    """
    raw = os.environ.get("BROKERBENCH_SHUFFLE_CHOICES", "1").strip().lower()
    return raw not in ("0", "false", "no", "off")
