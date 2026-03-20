"""BrokerBench inference — run models against the benchmark."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from rich.console import Console

from brokerbench.harness.types import Instance

console = Console()


def load_instances(dataset_path: str) -> list[Instance]:
    """Load benchmark instances from a JSONL file or all built-in datasets.

    Args:
        dataset_path: Path to a JSONL file, or ``"all"`` to load every
            built-in dataset under ``resources/datasets/``.

    Returns:
        List of :class:`Instance` objects.
    """
    if dataset_path == "all":
        datasets_dir = Path(__file__).parent.parent / "resources" / "datasets"
        instances: list[Instance] = []
        for path in sorted(datasets_dir.glob("*.jsonl")):
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        instances.append(Instance(**json.loads(line)))
        return instances

    path = Path(dataset_path)
    if not path.exists():
        console.print(f"[red]Dataset not found: {path}[/red]")
        sys.exit(1)

    instances = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                instances.append(Instance(**json.loads(line)))
    return instances


def build_prompt(instance: Instance) -> str:
    """Build a model prompt from a benchmark instance.

    Formats the question with optional context and multiple-choice options.
    For non-MCQ instances a generic instruction is appended.

    Args:
        instance: The benchmark instance to create a prompt for.

    Returns:
        Formatted prompt string.
    """
    parts = [instance.question]

    if instance.context:
        parts.insert(0, f"Context:\n{instance.context}\n")

    if instance.choices:
        parts.append("\nOptions:")
        for choice in instance.choices:
            parts.append(f"  {choice}")
        parts.append(
            "\nRespond with ONLY the letter of the correct answer "
            "(A, B, C, or D), followed by a brief explanation."
        )
    else:
        parts.append("\nProvide a clear, concise answer.")

    return "\n".join(parts)
