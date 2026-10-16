"""Tests for provider routing, model detection, and parallel inference."""

from __future__ import annotations

import json
import random
import time
from pathlib import Path

import pytest

from brokerbench.harness.constants import Domain
from brokerbench.harness.types import Instance
from brokerbench.inference.run_api import (
    _is_modern_claude,
    _is_openai_reasoning_model,
    _max_concurrency,
    _run_instances,
)


def _instance(i: int) -> Instance:
    return Instance(
        instance_id=f"test-{i:03d}",
        domain=Domain.LICENSING,
        question=f"Question {i}?",
        choices=["A. a", "B. b"],
        expected_answer="A",
    )


class TestOpenAIReasoningDetection:
    @pytest.mark.parametrize(
        "model",
        ["gpt-5", "gpt-5-mini", "gpt-5.5", "gpt-5.5-pro", "gpt-6", "gpt-6.1-sol", "o3", "o4-mini"],
    )
    def test_reasoning_models(self, model: str) -> None:
        assert _is_openai_reasoning_model(model)

    @pytest.mark.parametrize(
        "model",
        ["gpt-4o", "gpt-4o-mini", "gpt-4.1", "gpt-4-turbo", "gpt-3.5-turbo", "chatgpt-4o-latest"],
    )
    def test_legacy_chat_models(self, model: str) -> None:
        assert not _is_openai_reasoning_model(model)


class TestModernClaudeDetection:
    @pytest.mark.parametrize(
        "model",
        [
            "claude-sonnet-5-5",
            "claude-opus-5-5",
            "claude-haiku-5-5",
            "claude-opus-4-6",
            "claude-sonnet-4-8",
            "claude-fable-5-1",
            "claude-mythos-5-1",
            "anthropic/claude-sonnet-5.5",  # OpenRouter-style id
            "anthropic/claude-fable-5.1",
        ],
    )
    def test_modern_models(self, model: str) -> None:
        assert _is_modern_claude(model)

    @pytest.mark.parametrize(
        "model",
        [
            "claude-sonnet-4-20250514",
            "claude-opus-4-20250514",
            "claude-opus-4-1-20250805",
            "claude-sonnet-4-5-20250929",
            "claude-3-5-sonnet-20241022",
            "claude-3-haiku-20240307",
        ],
    )
    def test_legacy_models(self, model: str) -> None:
        assert not _is_modern_claude(model)


class TestMaxConcurrency:
    def test_cli_wins(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("BROKERBENCH_MAX_CONCURRENCY", "4")
        assert _max_concurrency(2) == 2

    def test_env_fallback(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("BROKERBENCH_MAX_CONCURRENCY", "4")
        assert _max_concurrency(None) == 4

    def test_default(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("BROKERBENCH_MAX_CONCURRENCY", raising=False)
        assert _max_concurrency(None) == 8

    def test_cli_clamped_to_one(self) -> None:
        assert _max_concurrency(0) == 1


class TestRunInstances:
    def test_preserves_dataset_order_under_concurrency(self, tmp_path: Path) -> None:
        instances = [_instance(i) for i in range(30)]

        def predict(instance: Instance) -> str:
            # Random-ish delays so completion order differs from input order.
            time.sleep(random.uniform(0, 0.005))
            return f"A. {instance.instance_id}"

        out = tmp_path / "preds.jsonl"
        preds = _run_instances(instances, "fake-model", out, predict, max_concurrency=8)

        assert [p.instance_id for p in preds] == [i.instance_id for i in instances]
        lines = out.read_text().strip().split("\n")
        assert len(lines) == len(instances)
        assert [json.loads(line)["instance_id"] for line in lines] == [
            i.instance_id for i in instances
        ]

    def test_error_instances_become_error_predictions(self, tmp_path: Path) -> None:
        instances = [_instance(i) for i in range(4)]

        def predict(instance: Instance) -> str:
            if instance.instance_id == "test-002":
                raise RuntimeError("boom")
            return "A. fine"

        out = tmp_path / "preds.jsonl"
        preds = _run_instances(instances, "fake-model", out, predict, max_concurrency=1)

        assert len(preds) == 4
        failed = preds[2]
        assert failed.prediction == ""
        assert failed.metadata is not None
        assert "boom" in failed.metadata["error"]

    def test_mcq_answer_extracted_from_prose(self, tmp_path: Path) -> None:
        instances = [_instance(1)]
        out = tmp_path / "preds.jsonl"
        preds = _run_instances(
            instances, "fake-model", out, lambda inst: "The answer is A.", max_concurrency=1
        )
        assert preds[0].prediction == "A"
