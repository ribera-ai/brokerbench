"""Shared LLM-judge scoring utility.

Provides a reusable function that sends a prompt + prediction + rubric
to an LLM and returns a structured ScoreDetail.  Used by domain-specific
scorers (ExplanationQuality, CognitiveDepth, RiskAssessment, etc.)
when deterministic scoring is insufficient.

If no LLM client is available the scorer falls back to a heuristic
estimate so that the evaluation pipeline never hard-fails.
"""

from __future__ import annotations

import logging
import os
import re

from brokerbench.harness.grading import ScoreDetail

logger = logging.getLogger(__name__)

# Default model used for LLM-judge scoring when OPENROUTER_API_KEY is set.
_DEFAULT_JUDGE_MODEL = "openai/gpt-4o-mini"


def _call_openrouter(
    prompt: str,
    model: str = _DEFAULT_JUDGE_MODEL,
) -> str | None:
    """Call OpenRouter and return the assistant message text.

    Returns ``None`` when the API key is missing or the request fails,
    allowing callers to fall back to heuristic scoring.
    """
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return None

    try:
        import httpx  # noqa: PLC0415 — deferred import
    except ImportError:
        logger.debug("httpx not installed; skipping LLM-judge call")
        return None

    try:
        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.0,
                "max_tokens": 256,
            },
            timeout=30.0,
        )
        response.raise_for_status()
        data = response.json()
        return str(
            data["choices"][0]["message"]["content"]
        ).strip()
    except Exception:
        logger.warning("LLM-judge call failed", exc_info=True)
        return None


def _extract_score(text: str) -> float | None:
    """Pull the first decimal or integer score (0-1 range) from text."""
    m = re.search(r"\b([01](?:\.\d{1,2})?)\b", text)
    if m:
        val = float(m.group(1))
        if 0.0 <= val <= 1.0:
            return val
    # Also accept "X/10" style
    m2 = re.search(r"(\d+(?:\.\d+)?)\s*/\s*10", text)
    if m2:
        val = float(m2.group(1)) / 10.0
        return max(0.0, min(1.0, val))
    return None


def llm_judge_score(
    prompt: str,
    prediction: str,
    rubric: str,
    scorer_name: str = "llm_judge",
    model: str = _DEFAULT_JUDGE_MODEL,
) -> ScoreDetail:
    """Score a prediction using an LLM judge.

    Constructs a grading prompt from the original question prompt,
    the model's prediction, and a scoring rubric, then asks the
    judge model to return a score between 0.0 and 1.0.

    Falls back to a simple heuristic (response length) when no
    LLM API key is configured.

    Args:
        prompt: The original question / task prompt.
        prediction: The model's response to score.
        rubric: Plain-text rubric the judge should use.
        scorer_name: Name to attach to the returned ScoreDetail.
        model: OpenRouter model identifier for the judge.

    Returns:
        ScoreDetail with a score in [0, 1].
    """
    judge_prompt = (
        "You are an expert grader for real-estate licensing and "
        "brokerage exams.  Score the RESPONSE on a scale from 0.0 "
        "(completely wrong / unhelpful) to 1.0 (perfect).\n\n"
        "## Rubric\n"
        f"{rubric}\n\n"
        "## Question / Prompt\n"
        f"{prompt}\n\n"
        "## Response\n"
        f"{prediction}\n\n"
        "Return ONLY a JSON object: {\"score\": <float 0-1>, "
        "\"reason\": \"<one-sentence justification>\"}"
    )

    llm_output = _call_openrouter(judge_prompt, model=model)

    if llm_output is not None:
        score_val = _extract_score(llm_output)
        if score_val is not None:
            return ScoreDetail(
                scorer_name=scorer_name,
                score=score_val,
                metadata={
                    "method": "llm_judge",
                    "model": model,
                    "raw_judge_output": llm_output[:500],
                },
            )
        # LLM responded but we couldn't parse a score
        logger.warning(
            "Could not extract score from LLM judge output: %s",
            llm_output[:200],
        )

    # ── Heuristic fallback ──────────────────────────────────────────
    prediction_stripped = prediction.strip()
    if not prediction_stripped:
        heuristic_score = 0.0
    elif len(prediction_stripped) < 20:
        heuristic_score = 0.15
    elif len(prediction_stripped) < 80:
        heuristic_score = 0.35
    elif len(prediction_stripped) < 250:
        heuristic_score = 0.55
    else:
        heuristic_score = 0.65

    return ScoreDetail(
        scorer_name=scorer_name,
        score=heuristic_score,
        metadata={
            "method": "heuristic_fallback",
            "response_length": str(len(prediction_stripped)),
        },
    )
