"""Run inference against the benchmark using OpenAI / Anthropic / OpenRouter APIs.

Usage:
    python -m brokerbench.inference.run_api \
        --model_name claude-3-sonnet \
        --dataset brokerbench/resources/datasets/licensing_national.jsonl \
        --output_file predictions/claude-3-sonnet.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from rich.console import Console
from tqdm import tqdm

from brokerbench.harness.types import Instance, Prediction

console = Console()


def build_prompt(instance: Instance) -> str:
    """Build a model prompt from a benchmark instance.

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
            "\nRespond with ONLY the letter of the correct answer (A, B, C, or D), "
            "followed by a brief explanation."
        )
    else:
        parts.append("\nProvide a clear, concise answer.")

    return "\n".join(parts)


def run_openai(
    instances: list[Instance],
    model_name: str,
    output_path: Path,
) -> list[Prediction]:
    """Run inference using the OpenAI API.

    Args:
        instances: List of benchmark instances to evaluate.
        model_name: OpenAI model identifier (e.g. 'gpt-4o').
        output_path: Path to write prediction JSONL.

    Returns:
        List of Prediction objects.
    """
    try:
        from openai import OpenAI
    except ImportError:
        console.print("[red]openai package not installed. Run: pip install openai[/red]")
        sys.exit(1)

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    predictions: list[Prediction] = []

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        for instance in tqdm(instances, desc=f"Running {model_name}"):
            prompt = build_prompt(instance)
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a knowledgeable real estate professional "
                                "taking an evaluation. Answer accurately and concisely."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0,
                    max_tokens=1024,
                )
                raw_output = response.choices[0].message.content or ""

                # Extract answer letter for MCQ
                answer = raw_output
                if instance.choices:
                    for char in raw_output.strip():
                        if char.upper() in "ABCD":
                            answer = char.upper()
                            break

                pred = Prediction(
                    instance_id=instance.instance_id,
                    model_name_or_path=model_name,
                    prediction=answer,
                    reasoning=raw_output,
                    raw_output=raw_output,
                )
            except Exception as e:
                console.print(f"[yellow]Error on {instance.instance_id}: {e}[/yellow]")
                pred = Prediction(
                    instance_id=instance.instance_id,
                    model_name_or_path=model_name,
                    prediction="",
                    reasoning="",
                    raw_output=str(e),
                    metadata={"error": str(e)},
                )

            predictions.append(pred)
            f.write(pred.model_dump_json() + "\n")

    return predictions


def run_anthropic(
    instances: list[Instance],
    model_name: str,
    output_path: Path,
) -> list[Prediction]:
    """Run inference using the Anthropic API.

    Args:
        instances: List of benchmark instances to evaluate.
        model_name: Anthropic model identifier (e.g. 'claude-3-sonnet-20240229').
        output_path: Path to write prediction JSONL.

    Returns:
        List of Prediction objects.
    """
    try:
        from anthropic import Anthropic
    except ImportError:
        console.print("[red]anthropic package not installed. Run: pip install anthropic[/red]")
        sys.exit(1)

    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
    predictions: list[Prediction] = []

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        for instance in tqdm(instances, desc=f"Running {model_name}"):
            prompt = build_prompt(instance)
            try:
                response = client.messages.create(
                    model=model_name,
                    max_tokens=1024,
                    temperature=0,
                    system=(
                        "You are a knowledgeable real estate professional "
                        "taking an evaluation. Answer accurately and concisely."
                    ),
                    messages=[{"role": "user", "content": prompt}],
                )
                from anthropic.types import TextBlock

                raw_output = ""
                for block in response.content:
                    if isinstance(block, TextBlock):
                        raw_output = block.text
                        break

                # Extract answer letter for MCQ
                answer = raw_output
                if instance.choices:
                    for char in raw_output.strip():
                        if char.upper() in "ABCD":
                            answer = char.upper()
                            break

                pred = Prediction(
                    instance_id=instance.instance_id,
                    model_name_or_path=model_name,
                    prediction=answer,
                    reasoning=raw_output,
                    raw_output=raw_output,
                )
            except Exception as e:
                console.print(f"[yellow]Error on {instance.instance_id}: {e}[/yellow]")
                pred = Prediction(
                    instance_id=instance.instance_id,
                    model_name_or_path=model_name,
                    prediction="",
                    reasoning="",
                    raw_output=str(e),
                    metadata={"error": str(e)},
                )

            predictions.append(pred)
            f.write(pred.model_dump_json() + "\n")

    return predictions


def load_instances(dataset_path: str) -> list[Instance]:
    """Load instances from a JSONL file path or 'all' for built-in datasets.

    Args:
        dataset_path: Path to JSONL file, or 'all' for all built-in datasets.

    Returns:
        List of Instance objects.
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


def main() -> None:
    """CLI entry point for API-based inference."""
    parser = argparse.ArgumentParser(
        description="Run a model against BrokerBench using API inference."
    )
    parser.add_argument(
        "--model_name",
        type=str,
        required=True,
        help="Model identifier (e.g. 'gpt-4o', 'claude-3-sonnet-20240229').",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="Path to dataset JSONL file, or 'all' for all built-in datasets.",
    )
    parser.add_argument(
        "--output_file",
        type=Path,
        required=True,
        help="Path to write prediction JSONL file.",
    )
    parser.add_argument(
        "--provider",
        type=str,
        default="openai",
        choices=["openai", "anthropic"],
        help="API provider to use (default: openai).",
    )
    args = parser.parse_args()

    instances = load_instances(args.dataset)
    console.print(f"Loaded {len(instances)} instances")

    if args.provider == "openai":
        run_openai(instances, args.model_name, args.output_file)
    elif args.provider == "anthropic":
        run_anthropic(instances, args.model_name, args.output_file)

    console.print(f"[green]Predictions written to {args.output_file}[/green]")


if __name__ == "__main__":
    main()
