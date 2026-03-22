"""Scorers for the Brokerage Management domain.

Implements:
- BrokerageMCQ: Deterministic multiple-choice scoring
- ManagementDecision: LLM-judge scorer for management reasoning
"""

from __future__ import annotations

from brokerbench.harness.grading import ScoreDetail
from brokerbench.harness.scorers.llm_judge import llm_judge_score
from brokerbench.harness.types import Instance, Prediction
from brokerbench.harness.utils import extract_mcq_answer


def score_brokerage_mcq(
    instance: Instance,
    prediction: Prediction,
) -> ScoreDetail:
    """Score a brokerage management multiple-choice question.

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
        scorer_name="brokerage_accuracy",
        score=1.0 if is_correct else 0.0,
        metadata={
            "predicted": predicted,
            "expected": expected,
        },
    )


def score_management_decision(
    instance: Instance,
    prediction: Prediction,
) -> ScoreDetail:
    """Score management decision-making quality.

    Uses the LLM judge to evaluate whether the response
    demonstrates sound business judgment, regulatory awareness,
    and appropriate risk management.

    Args:
        instance: The benchmark instance.
        prediction: The model's prediction.

    Returns:
        ScoreDetail with score in [0, 1].
    """
    rubric = (
        "Score the response on three criteria (equal weight):\n"
        "1. Business judgment -- Is the advice financially and "
        "operationally sound?\n"
        "2. Regulatory compliance -- Does the response account "
        "for applicable laws and regulations?\n"
        "3. Risk management -- Are potential risks identified "
        "and mitigated?\n\n"
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
        scorer_name="management_decision",
    )
