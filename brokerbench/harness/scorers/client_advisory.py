"""Scorers for the Client Advisory domain.

Implements:
- AdvisoryMCQ: Deterministic multiple-choice scoring
- AdvisoryQuality: LLM-judge scorer for advisory reasoning
"""

from __future__ import annotations

from brokerbench.harness.grading import ScoreDetail
from brokerbench.harness.scorers.llm_judge import llm_judge_score
from brokerbench.harness.types import Instance, Prediction
from brokerbench.harness.utils import extract_mcq_answer


def score_advisory_mcq(
    instance: Instance,
    prediction: Prediction,
) -> ScoreDetail:
    """Score a client advisory multiple-choice question.

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
        scorer_name="advisory_accuracy",
        score=1.0 if is_correct else 0.0,
        metadata={
            "predicted": predicted,
            "expected": expected,
        },
    )


def score_advisory_quality(
    instance: Instance,
    prediction: Prediction,
) -> ScoreDetail:
    """Score the quality of client advisory reasoning.

    Uses the LLM judge to evaluate whether the response provides
    appropriate, ethical, and well-reasoned client advice.

    Args:
        instance: The benchmark instance.
        prediction: The model's prediction.

    Returns:
        ScoreDetail with score in [0, 1].
    """
    rubric = (
        "Score the response on four criteria (equal weight):\n"
        "1. Client-centered -- Does it prioritize the client's "
        "best interest?\n"
        "2. Ethical compliance -- Does it stay within the "
        "agent's scope of practice?\n"
        "3. Informativeness -- Does it provide useful, "
        "actionable guidance?\n"
        "4. Risk disclosure -- Are relevant risks and trade-offs "
        "communicated?\n\n"
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
        scorer_name="advisory_quality",
    )
