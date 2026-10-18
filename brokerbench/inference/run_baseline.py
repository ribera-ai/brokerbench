"""Run naive baselines (always-A/B/C/D and uniform-random) for transparency.

These baselines establish a floor for any meaningful model score.  If
a real model cannot beat ``always-most-common-letter`` on a given
domain, that domain's results should be treated with skepticism --
either the dataset is too small, too biased, or the question content
is degenerate.

Usage::

    python -m brokerbench.inference.run_baseline \\
        --strategy always-a \\
        --dataset all \\
        --output_file predictions/baseline-always-a.jsonl

Strategies:
    always-a, always-b, always-c, always-d, uniform-random,
    most-common (picks the most-common letter in the dataset),
    all (writes one predictions file per strategy).
"""

from __future__ import annotations

import argparse
import random
import sys
from collections import Counter
from pathlib import Path

from rich.console import Console

from brokerbench.harness.types import Instance, Prediction
from brokerbench.inference import load_instances

console = Console()

_FIXED_LETTERS = {
    "always-a": "A",
    "always-b": "B",
    "always-c": "C",
    "always-d": "D",
}
_RANDOM_STRATEGIES = {"uniform-random"}
_DERIVED_STRATEGIES = {"most-common"}
_ALL_STRATEGIES = (
    list(_FIXED_LETTERS.keys()) + sorted(_RANDOM_STRATEGIES) + sorted(_DERIVED_STRATEGIES)
)


def _most_common_letter(instances: list[Instance]) -> str:
    """Return the most-frequent gold letter across MCQ instances."""
    counter: Counter[str] = Counter()
    for inst in instances:
        if inst.choices:
            counter[inst.expected_answer.strip().upper()] += 1
    if not counter:
        return "A"
    return counter.most_common(1)[0][0]


def _predict(strategy: str, instance: Instance, rng: random.Random, derived: str) -> str:
    """Return a single-letter prediction for the given strategy."""
    if not instance.choices:
        # Open-ended: no good naive answer; emit empty string so the
        # harness records UNRESOLVED.
        return ""

    n = len(instance.choices)
    letters = [chr(ord("A") + i) for i in range(n)]

    if strategy in _FIXED_LETTERS:
        letter = _FIXED_LETTERS[strategy]
        return letter if letter in letters else letters[0]
    if strategy == "uniform-random":
        return rng.choice(letters)
    if strategy == "most-common":
        return derived if derived in letters else letters[0]
    raise ValueError(f"Unknown baseline strategy: {strategy}")


def run_baseline(
    instances: list[Instance],
    strategy: str,
    output_path: Path,
    seed: int = 0,
) -> list[Prediction]:
    """Run a single naive baseline strategy and write predictions to ``output_path``."""
    rng = random.Random(seed)
    derived = _most_common_letter(instances) if strategy == "most-common" else ""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    predictions: list[Prediction] = []
    with open(output_path, "w") as f:
        for instance in instances:
            answer = _predict(strategy, instance, rng, derived)
            pred = Prediction(
                instance_id=instance.instance_id,
                model_name_or_path=f"baseline/{strategy}",
                prediction=answer,
                reasoning="naive baseline; no model call",
                raw_output=answer,
                metadata={"baseline_strategy": strategy},
            )
            predictions.append(pred)
            f.write(pred.model_dump_json() + "\n")
    return predictions


def main() -> None:
    """CLI entry point for naive baseline generation."""
    parser = argparse.ArgumentParser(
        description="Generate naive-baseline predictions for BrokerBench."
    )
    parser.add_argument(
        "--strategy",
        type=str,
        default="all",
        choices=[*_ALL_STRATEGIES, "all"],
        help="Baseline strategy to run (or 'all' for every strategy).",
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
        required=False,
        help="Output JSONL file (single strategy) or directory (--strategy all).",
    )
    parser.add_argument("--seed", type=int, default=0, help="RNG seed for random strategies.")
    args = parser.parse_args()

    instances = load_instances(args.dataset)
    console.print(f"Loaded {len(instances)} instances")

    if args.strategy == "all":
        out_dir = args.output_file or Path("predictions/baselines")
        out_dir.mkdir(parents=True, exist_ok=True)
        if out_dir.exists() and not out_dir.is_dir():
            console.print("[red]--output_file must be a directory when --strategy all[/red]")
            sys.exit(1)
        for strat in _ALL_STRATEGIES:
            target = out_dir / f"{strat}.jsonl"
            run_baseline(instances, strat, target, seed=args.seed)
            console.print(f"  wrote {target}")
    else:
        if args.output_file is None:
            args.output_file = Path(f"predictions/baseline-{args.strategy}.jsonl")
        run_baseline(instances, args.strategy, args.output_file, seed=args.seed)
        console.print(f"[green]Predictions written to {args.output_file}[/green]")


if __name__ == "__main__":
    main()
