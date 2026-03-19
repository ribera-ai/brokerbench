"""Report generation utilities for BrokerBench evaluation results."""

from __future__ import annotations

from brokerbench.harness.grading import EvalResult


def generate_markdown_report(result: EvalResult) -> str:
    """Generate a detailed Markdown report from evaluation results.

    Args:
        result: The evaluation result to format.

    Returns:
        Formatted Markdown string.
    """
    lines = [
        "# BrokerBench Evaluation Report",
        "",
        f"**Run ID**: {result.run_id}",
        f"**Model**: {result.model_name}",
        f"**Total Instances**: {result.total_instances}",
        f"**Composite Score**: {result.composite_score:.1%}",
        "",
        "---",
        "",
        "## Domain Breakdown",
        "",
        "| Domain | Score | Resolved | Total | Error |",
        "|--------|-------|----------|-------|-------|",
    ]

    for domain, dr in result.domain_results.items():
        lines.append(
            f"| {domain.value} | {dr.mean_score:.1%} | "
            f"{dr.resolved_count} | {dr.total_instances} | {dr.error_count} |"
        )

    lines.extend(["", "---", "", "## Scorer Breakdown", ""])

    for domain, dr in result.domain_results.items():
        if dr.scores_by_scorer:
            lines.append(f"### {domain.value}")
            lines.append("")
            lines.append("| Scorer | Mean Score |")
            lines.append("|--------|-----------|")
            for scorer_name, score in dr.scores_by_scorer.items():
                lines.append(f"| {scorer_name} | {score:.1%} |")
            lines.append("")

    return "\n".join(lines)
