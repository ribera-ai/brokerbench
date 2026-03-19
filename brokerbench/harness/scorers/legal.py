"""Scorers for the Legal/Contract domain.

Implements:
- IssueSpotting: Precision/recall for identified contract issues (placeholder for Phase 4)
- ClauseExtraction: Exact match + fuzzy scoring (placeholder for Phase 4)
- RuleApplication: LLM-judge scorer (placeholder for Phase 4)
"""

from __future__ import annotations

from brokerbench.harness.grading import ScoreDetail
from brokerbench.harness.types import Instance, Prediction


def score_issue_spotting(instance: Instance, prediction: Prediction) -> ScoreDetail:
    """Score contract issue-spotting tasks.

    Compares predicted issues against expected issues using
    simple string matching. Full implementation will use
    fuzzy matching and F1 scoring over issue sets.

    Args:
        instance: The benchmark instance with expected_answer.
        prediction: The model's prediction.

    Returns:
        ScoreDetail with score based on exact match for now.
    """
    expected = instance.expected_answer.strip().lower()
    predicted = prediction.prediction.strip().lower()

    is_correct = predicted == expected

    return ScoreDetail(
        scorer_name="issue_spotting",
        score=1.0 if is_correct else 0.0,
        metadata={
            "predicted": predicted[:200],
            "expected": expected[:200],
        },
    )
