"""Tests for the naive-baseline runner."""

from __future__ import annotations

import json
from pathlib import Path

from brokerbench.harness.constants import Domain
from brokerbench.harness.types import Instance
from brokerbench.inference.run_baseline import (
    _ALL_STRATEGIES,
    _most_common_letter,
    run_baseline,
)


def _make_instance(instance_id: str, expected: str = "B") -> Instance:
    return Instance(
        instance_id=instance_id,
        domain=Domain.LICENSING,
        question="Test?",
        choices=["A. one", "B. two", "C. three", "D. four"],
        expected_answer=expected,
    )


def test_always_letter_strategies_emit_that_letter(tmp_path: Path) -> None:
    instances = [_make_instance(f"id-{i}") for i in range(5)]
    for strategy, letter in [
        ("always-a", "A"),
        ("always-b", "B"),
        ("always-c", "C"),
        ("always-d", "D"),
    ]:
        out = tmp_path / f"{strategy}.jsonl"
        preds = run_baseline(instances, strategy, out)
        assert all(p.prediction == letter for p in preds)
        with open(out) as f:
            lines = [json.loads(line) for line in f if line.strip()]
        assert len(lines) == 5
        assert all(line["prediction"] == letter for line in lines)


def test_uniform_random_is_seedable(tmp_path: Path) -> None:
    instances = [_make_instance(f"id-{i}") for i in range(20)]
    a = run_baseline(instances, "uniform-random", tmp_path / "a.jsonl", seed=42)
    b = run_baseline(instances, "uniform-random", tmp_path / "b.jsonl", seed=42)
    assert [p.prediction for p in a] == [p.prediction for p in b]


def test_most_common_picks_majority_letter(tmp_path: Path) -> None:
    # Bias the dataset toward C.
    instances = [_make_instance(f"id-{i}", expected="C") for i in range(8)]
    instances += [_make_instance(f"id-x-{i}", expected="A") for i in range(2)]
    assert _most_common_letter(instances) == "C"
    preds = run_baseline(instances, "most-common", tmp_path / "out.jsonl")
    assert all(p.prediction == "C" for p in preds)


def test_all_strategies_constant_matches_runner() -> None:
    # Defensive: the script's --strategy choices must include every
    # registered strategy.
    expected = {"always-a", "always-b", "always-c", "always-d", "uniform-random", "most-common"}
    assert set(_ALL_STRATEGIES) == expected
