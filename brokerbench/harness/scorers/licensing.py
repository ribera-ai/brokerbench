"""Scorers for the Licensing Exam domain.

Implements:
- ExamAccuracy: Deterministic multiple-choice scoring
- ExplanationQuality: LLM-judge scorer (placeholder for Phase 2)
- CognitiveDepth: LLM-judge scorer (placeholder for Phase 2)
"""

from __future__ import annotations

from brokerbench.harness.grading import ScoreDetail
from brokerbench.harness.types import Instance, Prediction
from brokerbench.harness.utils import extract_mcq_answer


def score_licensing_mcq(instance: Instance, prediction: Prediction) -> ScoreDetail:
    """Score a licensing exam multiple-choice question.

    Extracts the answer letter from the prediction and compares
    against the expected answer. Case-insensitive.

    Args:
        instance: The benchmark instance with expected_answer.
        prediction: The model's prediction.

    Returns:
        ScoreDetail with score 1.0 (correct) or 0.0 (incorrect).
    """
    expected = instance.expected_answer.strip().upper()
    predicted = prediction.prediction.strip().upper()

    # Try to extract a single letter answer from longer responses
    if len(predicted) > 1 and instance.choices:
        extracted = extract_mcq_answer(prediction.prediction)
        if extracted:
            predicted = extracted

    is_correct = predicted == expected

    return ScoreDetail(
        scorer_name="exam_accuracy",
        score=1.0 if is_correct else 0.0,
        metadata={
            "predicted": predicted,
            "expected": expected,
        },
    )
