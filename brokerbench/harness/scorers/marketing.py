"""Scorers for the Marketing/Discovery domain.

Implements:
- SchemaOrgPresence: Deterministic check for structured data (placeholder for Phase 5)
- FAQStructure: Deterministic check for FAQ formatting (placeholder for Phase 5)
- ContentQuality: LLM-judge scorer (placeholder for Phase 5)
"""

from __future__ import annotations

from brokerbench.harness.grading import ScoreDetail
from brokerbench.harness.types import Instance, Prediction


def score_content_quality(instance: Instance, prediction: Prediction) -> ScoreDetail:
    """Score marketing content quality.

    Basic scoring based on response completeness.
    Full implementation will use LLM-judge for quality assessment.

    Args:
        instance: The benchmark instance with expected_answer.
        prediction: The model's prediction.

    Returns:
        ScoreDetail with score based on basic quality heuristics.
    """
    predicted = prediction.prediction.strip()

    # Basic heuristic: non-empty response with reasonable length
    if not predicted:
        score = 0.0
    elif len(predicted) < 50:
        score = 0.25
    elif len(predicted) < 200:
        score = 0.5
    else:
        score = 0.75  # Full scoring requires LLM judge

    return ScoreDetail(
        scorer_name="content_quality",
        score=score,
        metadata={
            "response_length": str(len(predicted)),
        },
    )
