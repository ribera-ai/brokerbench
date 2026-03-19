"""Scorers for the Underwriting domain.

Implements:
- ComplianceFlagAccuracy: Boolean F1 scoring for compliance flags
- RiskAssessmentQuality: LLM-judge scorer (placeholder for Phase 3)
- FieldExtractionAccuracy: Deterministic field extraction scoring (placeholder for Phase 3)
"""

from __future__ import annotations

from brokerbench.harness.grading import ScoreDetail
from brokerbench.harness.types import Instance, Prediction


def score_compliance_flag(instance: Instance, prediction: Prediction) -> ScoreDetail:
    """Score a yes/no compliance flag question.

    Compares the predicted answer against the expected boolean answer.
    Accepts common variants: yes/no, true/false, pass/fail, flag/clear.

    Args:
        instance: The benchmark instance with expected_answer.
        prediction: The model's prediction.

    Returns:
        ScoreDetail with score 1.0 (correct) or 0.0 (incorrect).
    """
    positive_terms = {"yes", "true", "flag", "fail", "flagged", "non-compliant", "1"}
    negative_terms = {"no", "false", "clear", "pass", "compliant", "0"}

    expected_raw = instance.expected_answer.strip().lower()
    predicted_raw = prediction.prediction.strip().lower()

    expected_positive = expected_raw in positive_terms
    predicted_positive = predicted_raw in positive_terms
    predicted_negative = predicted_raw in negative_terms

    # If prediction doesn't match any known term, mark as incorrect
    if not predicted_positive and not predicted_negative:
        return ScoreDetail(
            scorer_name="compliance_flag_accuracy",
            score=0.0,
            metadata={
                "predicted": predicted_raw,
                "expected": expected_raw,
                "error": "unrecognized_prediction_format",
            },
        )

    is_correct = expected_positive == predicted_positive

    return ScoreDetail(
        scorer_name="compliance_flag_accuracy",
        score=1.0 if is_correct else 0.0,
        metadata={
            "predicted": predicted_raw,
            "expected": expected_raw,
        },
    )
