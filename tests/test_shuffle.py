"""Tests for deterministic answer-choice shuffling."""

from __future__ import annotations

import os
from collections import Counter
from pathlib import Path
from unittest import mock

from brokerbench.harness.constants import Domain
from brokerbench.harness.shuffle import (
    shuffle_instance_choices,
    shuffle_instances,
    shuffling_enabled,
)
from brokerbench.harness.types import Instance
from brokerbench.inference import load_instances


def _make_instance(
    instance_id: str = "test-001",
    expected: str = "B",
    choices: list[str] | None = None,
) -> Instance:
    if choices is None:
        choices = [
            "A. Apple, the round red fruit",
            "B. Banana, the curved yellow fruit",
            "C. Cherry, the small red fruit",
            "D. Date, the brown wrinkled fruit",
        ]
    return Instance(
        instance_id=instance_id,
        domain=Domain.LICENSING,
        question="Which is the correct answer?",
        choices=choices,
        expected_answer=expected,
    )


class TestShuffleInstanceChoices:
    def test_preserves_correct_answer_content(self) -> None:
        original = _make_instance(expected="B")
        shuffled = shuffle_instance_choices(original)

        # The expected answer letter may change, but the *content*
        # behind it must still be the banana option.
        new_letter = shuffled.expected_answer
        idx = ord(new_letter) - ord("A")
        assert "Banana" in shuffled.choices[idx]

    def test_deterministic_for_same_id(self) -> None:
        a = shuffle_instance_choices(_make_instance("foo-1", expected="C"))
        b = shuffle_instance_choices(_make_instance("foo-1", expected="C"))
        assert a.choices == b.choices
        assert a.expected_answer == b.expected_answer

    def test_different_ids_get_different_shuffles(self) -> None:
        # With different instance_ids, at least one of the first
        # several pairs should differ.  We test a batch to keep it
        # deterministic without relying on a single id.
        seen: set[tuple[str, ...]] = set()
        for i in range(20):
            instance = _make_instance(f"id-{i}", expected="B")
            shuffled = shuffle_instance_choices(instance)
            seen.add(tuple(shuffled.choices))
        # We should see at least 4 distinct orderings out of 24
        # possible permutations of 4 options.
        assert len(seen) >= 4

    def test_non_mcq_unchanged(self) -> None:
        instance = Instance(
            instance_id="open-001",
            domain=Domain.UNDERWRITING,
            question="Explain DTI.",
            expected_answer="Total monthly debt / gross monthly income",
        )
        shuffled = shuffle_instance_choices(instance)
        assert shuffled.expected_answer == instance.expected_answer
        assert shuffled.choices is None

    def test_round_trip_via_letters(self) -> None:
        """Verify expected_answer always points at the original gold body."""
        for i in range(50):
            inst = _make_instance(f"rt-{i}", expected="C")
            shuffled = shuffle_instance_choices(inst)
            new_idx = ord(shuffled.expected_answer) - ord("A")
            assert "Cherry" in shuffled.choices[new_idx]

    def test_choices_relabeled_in_order(self) -> None:
        inst = _make_instance("rl-001", expected="A")
        shuffled = shuffle_instance_choices(inst)
        assert shuffled.choices is not None
        for i, choice in enumerate(shuffled.choices):
            expected_letter = chr(ord("A") + i)
            assert choice.startswith(f"{expected_letter}. ")

    def test_invalid_expected_answer_left_unchanged(self) -> None:
        inst = _make_instance("bad-001", expected="Z")
        shuffled = shuffle_instance_choices(inst)
        assert shuffled.choices == inst.choices
        assert shuffled.expected_answer == "Z"


class TestShuffleInstances:
    def test_preserves_count(self) -> None:
        instances = [_make_instance(f"i-{i}", expected="B") for i in range(50)]
        shuffled = shuffle_instances(instances)
        assert len(shuffled) == len(instances)

    def test_distribution_more_balanced_than_input(self) -> None:
        # Build a worst-case input: 50 questions all with B as gold.
        instances = [_make_instance(f"i-{i}", expected="B") for i in range(50)]
        shuffled = shuffle_instances(instances)

        positions = Counter(s.expected_answer for s in shuffled)
        # All four positions should appear, and no single position
        # should account for >40% of answers.
        assert set(positions.keys()) == {"A", "B", "C", "D"}
        for letter, count in positions.items():
            assert count <= 0.40 * len(instances), (
                f"Letter {letter} has {count} of {len(instances)} -- still biased"
            )


class TestShufflingEnabled:
    def test_default_on(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("BROKERBENCH_SHUFFLE_CHOICES", None)
            assert shuffling_enabled() is True

    def test_off_via_zero(self) -> None:
        with mock.patch.dict(os.environ, {"BROKERBENCH_SHUFFLE_CHOICES": "0"}):
            assert shuffling_enabled() is False

    def test_off_via_false(self) -> None:
        with mock.patch.dict(os.environ, {"BROKERBENCH_SHUFFLE_CHOICES": "false"}):
            assert shuffling_enabled() is False


class TestLoadedDatasetIsBalanced:
    """Smoke-test the entire built-in dataset for residual bias."""

    def test_built_in_dataset_balanced(self) -> None:
        # Make sure shuffling is on.
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("BROKERBENCH_SHUFFLE_CHOICES", None)
            instances = load_instances("all")

        mcq = [i for i in instances if i.choices]
        assert len(mcq) > 100, "Expected >100 MCQ instances in the built-in dataset"

        positions = Counter(i.expected_answer for i in mcq)
        n = len(mcq)
        # No single letter should account for more than 50% of the
        # gold answers after shuffling.  The pre-shuffle dataset had
        # ~72% of answers on B; this guards against regression.
        for letter, count in positions.items():
            assert count <= 0.50 * n, (
                f"Letter {letter}={count}/{n} ({count / n:.0%}) — answer position bias regression"
            )

    def test_built_in_dataset_files_exist(self) -> None:
        # Sanity check that the JSONL package data is shipping.
        from brokerbench.inference import __file__ as inf_file

        datasets_dir = Path(inf_file).parent.parent / "resources" / "datasets"
        files = sorted(datasets_dir.glob("*.jsonl"))
        assert len(files) >= 6
