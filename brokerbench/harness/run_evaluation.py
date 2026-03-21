"""Main entry point for evaluating predictions against the benchmark.

Usage:
    python -m brokerbench.harness.run_evaluation \
        --predictions_path predictions/claude-3-sonnet.jsonl \
        --dataset_name all \
        --run_id my-eval-run
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table

from brokerbench.harness.constants import DEFAULT_DOMAIN_WEIGHTS, Domain, ResolutionStatus
from brokerbench.harness.grading import DomainResult, EvalResult, InstanceResult, ScoreDetail
from brokerbench.harness.reporting import generate_markdown_report
from brokerbench.harness.types import Instance, Prediction
from brokerbench.harness.utils import extract_mcq_answer

console = Console()

DATASETS_DIR = Path(__file__).parent.parent / "resources" / "datasets"
LOGS_DIR = Path("logs") / "run_evaluation"


def load_instances(dataset_name: str) -> list[Instance]:
    """Load benchmark instances from JSONL dataset files.

    Args:
        dataset_name: Name of dataset file (without .jsonl) or 'all' for all datasets.

    Returns:
        List of Instance objects.
    """
    instances: list[Instance] = []

    if dataset_name == "all":
        for path in sorted(DATASETS_DIR.glob("*.jsonl")):
            instances.extend(_load_jsonl_instances(path))
    else:
        path = DATASETS_DIR / f"{dataset_name}.jsonl"
        if not path.exists():
            console.print(f"[red]Dataset not found: {path}[/red]")
            sys.exit(1)
        instances = _load_jsonl_instances(path)

    return instances


def _load_jsonl_instances(path: Path) -> list[Instance]:
    """Load instances from a single JSONL file."""
    instances: list[Instance] = []
    with open(path) as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                instances.append(Instance(**data))
            except (json.JSONDecodeError, ValueError) as e:
                console.print(f"[yellow]Warning: Skipping line {line_num} in {path}: {e}[/yellow]")
    return instances


def load_predictions(predictions_path: Path) -> dict[str, Prediction]:
    """Load predictions from a JSONL file, keyed by instance_id."""
    predictions: dict[str, Prediction] = {}
    with open(predictions_path) as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                pred = Prediction(**data)
                predictions[pred.instance_id] = pred
            except (json.JSONDecodeError, ValueError) as e:
                console.print(f"[yellow]Warning: Skipping prediction line {line_num}: {e}[/yellow]")
    return predictions


def grade_instance(instance: Instance, prediction: Prediction) -> InstanceResult:
    """Grade a single prediction against its instance.

    Currently implements deterministic scoring only.
    LLM-judge scoring will be added per domain in future phases.
    """
    scores = []

    # Deterministic exact-match scoring (works for MCQ and short-answer)
    pred_answer = prediction.prediction.strip().upper()
    expected_answer = instance.expected_answer.strip().upper()

    # For MCQ, extract just the letter if the prediction includes explanation
    if instance.choices and len(pred_answer) > 1:
        extracted = extract_mcq_answer(prediction.prediction)
        if extracted:
            pred_answer = extracted

    is_correct = pred_answer == expected_answer

    scores.append(
        ScoreDetail(
            scorer_name="exact_match",
            score=1.0 if is_correct else 0.0,
            metadata={"predicted": pred_answer, "expected": expected_answer},
        )
    )

    aggregate = sum(s.score for s in scores) / len(scores) if scores else 0.0

    return InstanceResult(
        instance_id=instance.instance_id,
        domain=instance.domain,
        status=ResolutionStatus.RESOLVED if is_correct else ResolutionStatus.UNRESOLVED,
        scores=scores,
        aggregate_score=aggregate,
    )


def compute_domain_results(
    instance_results: list[InstanceResult],
) -> dict[Domain, DomainResult]:
    """Aggregate instance-level results into domain-level summaries."""
    domain_instances: dict[Domain, list[InstanceResult]] = {}
    for result in instance_results:
        domain_instances.setdefault(result.domain, []).append(result)

    domain_results: dict[Domain, DomainResult] = {}
    for domain, results in domain_instances.items():
        resolved = [r for r in results if r.status == ResolutionStatus.RESOLVED]
        errors = [r for r in results if r.status == ResolutionStatus.ERROR]
        mean_score = sum(r.aggregate_score for r in results) / len(results) if results else 0.0

        # Aggregate per-scorer means
        scorer_totals: dict[str, list[float]] = {}
        for r in results:
            for s in r.scores:
                scorer_totals.setdefault(s.scorer_name, []).append(s.score)
        scores_by_scorer = {name: sum(vals) / len(vals) for name, vals in scorer_totals.items()}

        domain_results[domain] = DomainResult(
            domain=domain,
            total_instances=len(results),
            resolved_count=len(resolved),
            error_count=len(errors),
            mean_score=mean_score,
            scores_by_scorer=scores_by_scorer,
        )

    return domain_results


def compute_composite_score(
    domain_results: dict[Domain, DomainResult],
    weights: dict[Domain, float] | None = None,
) -> float:
    """Compute a weighted composite score across domains."""
    if weights is None:
        weights = DEFAULT_DOMAIN_WEIGHTS

    total_weight = 0.0
    weighted_sum = 0.0
    for domain, result in domain_results.items():
        w = weights.get(domain, 0.0)
        weighted_sum += w * result.mean_score
        total_weight += w

    return weighted_sum / total_weight if total_weight > 0 else 0.0


def run_evaluation(
    predictions_path: Path,
    dataset_name: str = "all",
    run_id: str = "default",
) -> EvalResult:
    """Run the full evaluation pipeline.

    Args:
        predictions_path: Path to JSONL file with model predictions.
        dataset_name: Which dataset to evaluate against ('all' or specific name).
        run_id: Identifier for this evaluation run.

    Returns:
        EvalResult with full scoring breakdown.
    """
    console.print(f"[bold]BrokerBench Evaluation[/bold] — run_id: {run_id}")
    console.print()

    # Load data
    console.print("Loading instances...")
    instances = load_instances(dataset_name)
    console.print(f"  Loaded {len(instances)} instances")

    console.print("Loading predictions...")
    predictions = load_predictions(predictions_path)
    console.print(f"  Loaded {len(predictions)} predictions")

    # Match and grade
    instance_results: list[InstanceResult] = []
    missing_count = 0
    for instance in instances:
        prediction = predictions.get(instance.instance_id)
        if prediction is None:
            missing_count += 1
            instance_results.append(
                InstanceResult(
                    instance_id=instance.instance_id,
                    domain=instance.domain,
                    status=ResolutionStatus.ERROR,
                    error="No prediction found for this instance",
                )
            )
            continue
        result = grade_instance(instance, prediction)
        instance_results.append(result)

    if missing_count > 0:
        console.print(
            f"[yellow]Warning: {missing_count} instances had no matching prediction[/yellow]"
        )

    # Aggregate
    domain_results = compute_domain_results(instance_results)
    composite = compute_composite_score(domain_results)

    # Determine model name from first prediction
    model_name = "unknown"
    if predictions:
        first_pred = next(iter(predictions.values()))
        model_name = first_pred.model_name_or_path

    eval_result = EvalResult(
        run_id=run_id,
        model_name=model_name,
        total_instances=len(instances),
        composite_score=composite,
        domain_results=domain_results,
        instance_results=instance_results,
    )

    # Display results
    _print_results(eval_result)

    # Save report
    _save_report(eval_result, run_id)

    return eval_result


def _print_results(result: EvalResult) -> None:
    """Print evaluation results to console using rich."""
    console.print()
    console.print(f"[bold green]Composite Score: {result.composite_score:.1%}[/bold green]")
    console.print()

    table = Table(title="Domain Breakdown")
    table.add_column("Domain", style="bold")
    table.add_column("Score", justify="right")
    table.add_column("Resolved", justify="right")
    table.add_column("Total", justify="right")

    for domain, dr in result.domain_results.items():
        table.add_row(
            domain.value,
            f"{dr.mean_score:.1%}",
            str(dr.resolved_count),
            str(dr.total_instances),
        )

    console.print(table)


def _save_report(result: EvalResult, run_id: str) -> None:
    """Save evaluation report as JSON and Markdown."""
    output_dir = LOGS_DIR / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    # JSON report
    json_path = output_dir / "report.json"
    with open(json_path, "w") as f:
        f.write(result.model_dump_json(indent=2))
    console.print(f"JSON report saved to {json_path}")

    # Markdown report
    md_path = output_dir / "report.md"
    with open(md_path, "w") as f:
        f.write(generate_markdown_report(result))
    console.print(f"Markdown report saved to {md_path}")


def main() -> None:
    """CLI entry point for run_evaluation."""
    parser = argparse.ArgumentParser(
        description="Evaluate model predictions against the BrokerBench benchmark."
    )
    parser.add_argument(
        "--predictions_path",
        type=Path,
        required=True,
        help="Path to JSONL file with predictions.",
    )
    parser.add_argument(
        "--dataset_name",
        type=str,
        default="all",
        help="Dataset to evaluate against: 'all' or a specific dataset name.",
    )
    parser.add_argument(
        "--run_id",
        type=str,
        default="default",
        help="Identifier for this evaluation run.",
    )
    args = parser.parse_args()

    run_evaluation(
        predictions_path=args.predictions_path,
        dataset_name=args.dataset_name,
        run_id=args.run_id,
    )


if __name__ == "__main__":
    main()
