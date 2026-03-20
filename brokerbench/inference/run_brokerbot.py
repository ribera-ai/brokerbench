"""Run inference against BrokerBot via the monorepo's /api/generate endpoint.

Usage:
    python -m brokerbench.inference.run_brokerbot \
        --agent_url http://localhost:4100/api/generate \
        --team_id clxxxxxxxxxxxxxxxxx \
        --auth_cookie "better-auth.session_token=..." \
        --dataset all \
        --output_file predictions/brokerbot.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

from rich.console import Console
from tqdm import tqdm

from brokerbench.harness.types import Instance, Prediction

console = Console()


def build_prompt(instance: Instance) -> str:
    """Build a prompt from a benchmark instance.

    Formats the question with optional context and multiple-choice options.

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

    return "\n".join(parts)


def run_brokerbot(
    instances: list[Instance],
    agent_url: str,
    team_id: str,
    output_path: Path,
    auth_cookie: str | None = None,
    template: str = "brokerbot",
) -> list[Prediction]:
    """Run inference against BrokerBot's /api/generate endpoint.

    Sends each instance as a message to the BrokerBot generate endpoint
    and collects the non-streaming response as a prediction.

    Args:
        instances: List of benchmark instances to evaluate.
        agent_url: URL of the /api/generate endpoint.
        team_id: Team ID to scope the request.
        output_path: Path to write prediction JSONL.
        auth_cookie: Session cookie for authentication
            (e.g. "better-auth.session_token=...").
        template: Agent type to use (default: "brokerbot").

    Returns:
        List of Prediction objects.
    """
    predictions: list[Prediction] = []
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        for instance in tqdm(instances, desc="Running BrokerBot"):
            prompt = build_prompt(instance)

            try:
                payload = json.dumps(
                    {
                        "message": prompt,
                        "teamId": team_id,
                        "template": template,
                        "persist": False,
                    }
                ).encode("utf-8")

                headers: dict[str, str] = {
                    "Content-Type": "application/json",
                }
                if auth_cookie:
                    headers["Cookie"] = auth_cookie

                req = Request(
                    agent_url,
                    data=payload,
                    headers=headers,
                    method="POST",
                )
                with urlopen(req, timeout=120) as resp:
                    response_data = json.loads(resp.read().decode("utf-8"))

                raw_output = response_data.get("text", "")
                usage = response_data.get("usage", {})
                steps = response_data.get("steps", 0)

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
                    metadata={
                        "usage": json.dumps(usage),
                        "steps": str(steps),
                    },
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
        default="http://localhost:4100/api/generate",
        help="URL of the /api/generate endpoint (default: http://localhost:4100/api/generate).",
    )
    parser.add_argument(
        "--team_id",
        type=str,
        default=os.environ.get("BROKERBOT_TEAM_ID", ""),
        help="Team ID for the BrokerBot request (or set BROKERBOT_TEAM_ID env var).",
    )
    parser.add_argument(
        "--auth_cookie",
        type=str,
        default=os.environ.get("BROKERBOT_AUTH_COOKIE", ""),
        help=(
            "Session cookie for authentication "
            '(e.g. "better-auth.session_token=..."), '
            "or set BROKERBOT_AUTH_COOKIE env var."
        ),
    )
    parser.add_argument(
        "--template",
        type=str,
        default="brokerbot",
        help="Agent type to use (default: brokerbot).",
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

    if not args.team_id:
        console.print("[red]--team_id is required (or set BROKERBOT_TEAM_ID env var)[/red]")
        sys.exit(1)

    instances = load_instances(args.dataset)
    console.print(f"Loaded {len(instances)} instances")

    auth_cookie = args.auth_cookie if args.auth_cookie else None
    if not auth_cookie:
        console.print(
            "[yellow]Warning: No auth cookie provided. "
            "Requests may fail if the endpoint requires authentication.[/yellow]"
        )

    run_brokerbot(
        instances,
        args.agent_url,
        args.team_id,
        args.output_file,
        auth_cookie=auth_cookie,
        template=args.template,
    )
    console.print(f"[green]Predictions written to {args.output_file}[/green]")


if __name__ == "__main__":
    main()
