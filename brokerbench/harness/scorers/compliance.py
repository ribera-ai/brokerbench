"""Scorers for the Compliance & Regulation domain.

Implements:
- ComplianceMCQ: Deterministic multiple-choice scoring
- RegulatoryReasoning: LLM-judge scorer for regulatory analysis
"""

from __future__ import annotations

from brokerbench.harness.grading import ScoreDetail
from brokerbench.harness.scorers.llm_judge import llm_judge_score
from brokerbench.harness.types import Instance, Prediction
from brokerbench.harness.utils import extract_mcq_answer


def score_compliance_mcq(
    instance: Instance,
    prediction: Prediction,
) -> ScoreDetail:
    """Score a compliance multiple-choice question.

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

    if len(predicted) > 1 and instance.choices:
        extracted = extract_mcq_answer(prediction.prediction)
        if extracted:
            predicted = extracted

    is_correct = predicted == expected

    return ScoreDetail(
        scorer_name="compliance_accuracy",
        score=1.0 if is_correct else 0.0,
        metadata={
            "predicted": predicted,
            "expected": expected,
        },
    )


def score_regulatory_reasoning(
    instance: Instance,
    prediction: Prediction,
) -> ScoreDetail:
    """Score regulatory reasoning quality.

    Uses the LLM judge to evaluate whether the model correctly
    identifies the applicable regulation, applies it to the
    facts, and reaches the right conclusion.

    Args:
        instance: The benchmark instance.
        prediction: The model's prediction.

    Returns:
        ScoreDetail with score in [0, 1].
    """
    rubric = (
        "Score the response on three criteria (equal weight):\n"
        "1. Regulatory identification -- Does the response cite "
        "the correct law or regulation?\n"
        "2. Application -- Is the regulation applied correctly "
        "to the scenario?\n"
        "3. Conclusion -- Does the response reach the correct "
        "outcome?\n\n"
        "Gold answer for reference:\n"
        f"{instance.expected_answer}\n\n"
        "Gold explanation:\n"
        f"{instance.explanation}"
    )
    response_text = prediction.reasoning or prediction.prediction
    return llm_judge_score(
        prompt=instance.question,
        prediction=response_text,
        rubric=rubric,
        scorer_name="regulatory_reasoning",
    )
