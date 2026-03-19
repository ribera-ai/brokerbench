"""Run inference against BrokerBot via the monorepo's HTTP API.

Usage:
    python -m brokerbench.inference.run_brokerbot \
        --agent_url http://localhost:3000/api/agent \
        --dataset all \
        --output_file predictions/brokerbot.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

from rich.console import Console
from tqdm import tqdm

from brokerbench.harness.types import Instance, Prediction

console = Console()


def run_brokerbot(
    instances: list[Instance],
    agent_url: str,
    output_path: Path,
) -> list[Prediction]:
    """Run inference against BrokerBot's HTTP API.

    Sends each instance as a chat message to the BrokerBot agent
    and collects the response as a prediction.

    Args:
        instances: List of benchmark instances to evaluate.
        agent_url: URL of the BrokerBot agent API endpoint.
        output_path: Path to write prediction JSONL.

    Returns:
        List of Prediction objects.
    """
    predictions: list[Prediction] = []
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        for instance in tqdm(instances, desc="Running BrokerBot"):
            prompt = instance.question
            if instance.choices:
                prompt += "\n\nOptions:\n"
                for choice in instance.choices:
                    prompt += f"  {choice}\n"
                prompt += (
                    "\nRespond with ONLY the letter of the correct answer "
                    "(A, B, C, or D), followed by a brief explanation."
                )

            try:
                payload = json.dumps({"message": prompt}).encode("utf-8")
                req = Request(
                    agent_url,
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urlopen(req, timeout=60) as resp:
                    response_data = json.loads(resp.read().decode("utf-8"))

                raw_output = response_data.get("response", response_data.get("text", ""))

                # Extract answer letter for MCQ
                answer = raw_output
                if instance.choices:
                    for char in raw_output.strip():
                        if char.upper() in "ABCD":
                            answer = char.upper()
                            break

                pred = Prediction(
                    instance_id=instance.instance_id,
                    model_name_or_path="brokerbot",
                    prediction=answer,
                    reasoning=raw_output,
                    raw_output=raw_output,
                )
            except (URLError, TimeoutError, json.JSONDecodeError) as e:
                console.print(f"[yellow]Error on {instance.instance_id}: {e}[/yellow]")
                pred = Prediction(
                    instance_id=instance.instance_id,
                    model_name_or_path="brokerbot",
                    prediction="",
                    reasoning="",
                    raw_output=str(e),
                    metadata={"error": str(e)},
                )

            predictions.append(pred)
            f.write(pred.model_dump_json() + "\n")

    return predictions


def load_instances(dataset_path: str) -> list[Instance]:
    """Load instances from a JSONL file path or 'all' for built-in datasets."""
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
    """CLI entry point for BrokerBot inference."""
    parser = argparse.ArgumentParser(description="Run BrokerBot against the BrokerBench benchmark.")
    parser.add_argument(
        "--agent_url",
        type=str,
        required=True,
        help="URL of the BrokerBot agent API endpoint.",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="all",
        help="Path to dataset JSONL file, or 'all' for all built-in datasets.",
    )
    parser.add_argument(
        "--output_file",
        type=Path,
        required=True,
        help="Path to write prediction JSONL file.",
    )
    args = parser.parse_args()

    instances = load_instances(args.dataset)
    console.print(f"Loaded {len(instances)} instances")

    run_brokerbot(instances, args.agent_url, args.output_file)
    console.print(f"[green]Predictions written to {args.output_file}[/green]")


if __name__ == "__main__":
    main()
