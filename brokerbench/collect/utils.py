"""Shared utilities for dataset collection and curation."""

from __future__ import annotations

import json
from pathlib import Path

from brokerbench.harness.types import Instance


def write_instances_jsonl(instances: list[Instance], output_path: Path) -> None:
    """Write a list of Instance objects to a JSONL file.

    Args:
        instances: List of benchmark instances to write.
        output_path: Path to the output JSONL file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        for instance in instances:
            f.write(instance.model_dump_json() + "\n")


def load_instances_jsonl(path: Path) -> list[Instance]:
    """Load a list of Instance objects from a JSONL file.

    Args:
        path: Path to the JSONL file.

    Returns:
        List of Instance objects.
    """
    instances: list[Instance] = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            instances.append(Instance(**data))
    return instances


def validate_dataset(instances: list[Instance]) -> list[str]:
    """Validate a dataset for common issues.

    Args:
        instances: List of instances to validate.

    Returns:
        List of warning/error messages (empty if valid).
    """
    issues: list[str] = []
    seen_ids: set[str] = set()

    for i, instance in enumerate(instances):
        # Check for duplicate IDs
        if instance.instance_id in seen_ids:
            issues.append(f"Duplicate instance_id: {instance.instance_id}")
        seen_ids.add(instance.instance_id)

        # Check for empty questions
        if not instance.question.strip():
            issues.append(f"Instance {instance.instance_id}: empty question")

        # Check for empty expected answers
        if not instance.expected_answer.strip():
            issues.append(f"Instance {instance.instance_id}: empty expected_answer")

        # Check MCQ instances have choices
        if instance.domain.value == "licensing" and not instance.choices:
            issues.append(f"Instance {instance.instance_id}: licensing question missing choices")

        # Check MCQ answer is valid
        if instance.choices:
            valid_letters = [chr(65 + j) for j in range(len(instance.choices))]
            if instance.expected_answer.strip().upper() not in valid_letters:
                issues.append(
                    f"Instance {instance.instance_id}: "
                    f"expected_answer '{instance.expected_answer}' "
                    f"not in valid choices {valid_letters}"
                )

    return issues
