"""Tests for BrokerBench inference utilities."""

from brokerbench.harness.constants import Domain
from brokerbench.harness.types import Instance
from brokerbench.inference.make_datasets.create_prompts import (
    create_mcq_prompt,
    create_open_ended_prompt,
    create_prompt,
)
from brokerbench.inference.run_api import build_prompt


def _make_mcq_instance() -> Instance:
    return Instance(
        instance_id="test-001",
        domain=Domain.LICENSING,
        question="What is the answer?",
        choices=["A. Option A", "B. Option B", "C. Option C", "D. Option D"],
        expected_answer="B",
    )


def _make_open_instance() -> Instance:
    return Instance(
        instance_id="test-002",
        domain=Domain.UNDERWRITING,
        question="Explain the DTI ratio calculation.",
        expected_answer="Total monthly debt / gross monthly income",
    )


class TestBuildPrompt:
    def test_mcq_prompt_includes_choices(self) -> None:
        instance = _make_mcq_instance()
        prompt = build_prompt(instance)
        assert "Option A" in prompt
        assert "Option B" in prompt
        assert "ONLY the letter" in prompt

    def test_open_prompt_no_choices(self) -> None:
        instance = _make_open_instance()
        prompt = build_prompt(instance)
        assert "Explain the DTI" in prompt
        assert "clear, concise" in prompt

    def test_prompt_includes_context(self) -> None:
        instance = _make_mcq_instance()
        instance.context = "The borrower has a DTI of 45%."
        prompt = build_prompt(instance)
        assert "DTI of 45%" in prompt
        assert "Context:" in prompt


class TestCreatePrompts:
    def test_mcq_prompt(self) -> None:
        instance = _make_mcq_instance()
        prompt = create_mcq_prompt(instance)
        assert "Option A" in prompt
        assert "letter of the correct option" in prompt

    def test_open_ended_prompt(self) -> None:
        instance = _make_open_instance()
        prompt = create_open_ended_prompt(instance)
        assert "DTI ratio" in prompt
        assert "detailed answer" in prompt

    def test_create_prompt_dispatches_mcq(self) -> None:
        instance = _make_mcq_instance()
        prompt = create_prompt(instance)
        assert "letter of the correct option" in prompt

    def test_create_prompt_dispatches_open(self) -> None:
        instance = _make_open_instance()
        prompt = create_prompt(instance)
        assert "detailed answer" in prompt
