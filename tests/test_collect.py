"""Tests for BrokerBench dataset collection utilities."""

import json
import tempfile
from pathlib import Path

from brokerbench.collect.licensing import get_sample_instances
from brokerbench.collect.utils import (
    load_instances_jsonl,
    validate_dataset,
    write_instances_jsonl,
)
from brokerbench.harness.constants import Domain
from brokerbench.harness.types import Instance


class TestWriteAndLoadInstances:
    def test_round_trip(self) -> None:
        instances = get_sample_instances()
        assert len(instances) > 0

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.jsonl"
            write_instances_jsonl(instances, path)

            loaded = load_instances_jsonl(path)
            assert len(loaded) == len(instances)

            for orig, loaded_inst in zip(instances, loaded):
                assert orig.instance_id == loaded_inst.instance_id
                assert orig.expected_answer == loaded_inst.expected_answer

    def test_jsonl_format(self) -> None:
        instances = get_sample_instances()

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.jsonl"
            write_instances_jsonl(instances, path)

            with open(path) as f:
                lines = f.readlines()

            assert len(lines) == len(instances)
            for line in lines:
                data = json.loads(line)
                assert "instance_id" in data
                assert "question" in data


class TestValidateDataset:
    def test_valid_dataset(self) -> None:
        instances = get_sample_instances()
        issues = validate_dataset(instances)
        assert len(issues) == 0

    def test_duplicate_ids(self) -> None:
        inst = Instance(
            instance_id="dup-001",
            domain=Domain.LICENSING,
            question="Test?",
            expected_answer="A",
            choices=["A. Yes", "B. No"],
        )
        issues = validate_dataset([inst, inst])
        assert any("Duplicate" in issue for issue in issues)

    def test_empty_question(self) -> None:
        inst = Instance(
            instance_id="empty-q",
            domain=Domain.LICENSING,
            question="",
            expected_answer="A",
            choices=["A. Yes", "B. No"],
        )
        issues = validate_dataset([inst])
        assert any("empty question" in issue for issue in issues)

    def test_invalid_mcq_answer(self) -> None:
        inst = Instance(
            instance_id="bad-ans",
            domain=Domain.LICENSING,
            question="Test?",
            expected_answer="E",
            choices=["A. Yes", "B. No"],
        )
        issues = validate_dataset([inst])
        assert any("not in valid choices" in issue for issue in issues)

    def test_licensing_without_choices(self) -> None:
        inst = Instance(
            instance_id="no-choices",
            domain=Domain.LICENSING,
            question="Test?",
            expected_answer="A",
        )
        issues = validate_dataset([inst])
        assert any("missing choices" in issue for issue in issues)
