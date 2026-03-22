"""Scorers for the Licensing Exam domain.

Implements:
- ExamAccuracy: Deterministic multiple-choice scoring
- ExplanationQuality: LLM-judge scorer for answer explanations
- CognitiveDepth: LLM-judge scorer for cognitive-level alignment
"""

from __future__ import annotations

from brokerbench.harness.grading import ScoreDetail
from brokerbench.harness.scorers.llm_judge import llm_judge_score
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


def score_explanation_quality(
    instance: Instance,
    prediction: Prediction,
) -> ScoreDetail:
    """Score the quality of a licensing-exam explanation.

    Uses the LLM judge to evaluate whether the model's reasoning
    is accurate, complete, and references the correct legal
    principles.  Falls back to heuristic scoring when no API key
    is available.

    Args:
        instance: The benchmark instance (provides the gold explanation).
        prediction: The model's prediction (answer + reasoning).

    Returns:
        ScoreDetail with score in [0, 1].
    """
    rubric = (
        "Score the explanation on four criteria (equal weight):\n"
        "1. Accuracy -- Are the legal facts and principles correct?\n"
        "2. Completeness -- Does it cover all key points from the "
        "gold explanation?\n"
        "3. Clarity -- Is the reasoning easy to follow?\n"
        "4. Relevance -- Does it stay on-topic without filler?\n\n"
        "Gold explanation for reference:\n"
        f"{instance.explanation}"
    )
    response_text = prediction.reasoning or prediction.prediction
    return llm_judge_score(
        prompt=instance.question,
        prediction=response_text,
        rubric=rubric,
        scorer_name="explanation_quality",
    )


def score_cognitive_depth(
    instance: Instance,
    prediction: Prediction,
) -> ScoreDetail:
    """Score whether the response matches the expected cognitive level.

    A Knowledge-level question should elicit recall; an Application
    question should show scenario reasoning; an Analysis question
    should demonstrate evaluation and synthesis.

    Args:
        instance: The benchmark instance (provides cognitive_level).
        prediction: The model's prediction.

    Returns:
        ScoreDetail with score in [0, 1].
    """
    level_name = instance.cognitive_level.value if instance.cognitive_level else "unknown"
    rubric = (
        f"The intended cognitive level is **{level_name}**.\n\n"
        "- knowledge: response should recall facts, definitions, "
        "or rules.\n"
        "- application: response should apply a concept to a "
        "concrete scenario.\n"
        "- analysis: response should evaluate, compare, or "
        "synthesize multiple factors.\n"
        "- expert: response should demonstrate deep professional "
        "judgment integrating multiple domains and nuances.\n\n"
        "Score 1.0 if the depth of reasoning matches the "
        "intended level, 0.5 if partially aligned, 0.0 if "
        "mismatched (e.g. rote recall on an analysis question)."
    )
    response_text = prediction.reasoning or prediction.prediction
    return llm_judge_score(
        prompt=instance.question,
        prediction=response_text,
        rubric=rubric,
        scorer_name="cognitive_depth",
    )
