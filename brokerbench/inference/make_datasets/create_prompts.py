"""Convert raw dataset instances into model-ready prompts.

This module transforms Instance objects into formatted prompts
suitable for different model providers and evaluation modes.
"""

from __future__ import annotations

from brokerbench.harness.types import Instance


def create_mcq_prompt(instance: Instance) -> str:
    """Create a multiple-choice question prompt.

    Args:
        instance: Instance with choices field populated.

    Returns:
        Formatted MCQ prompt string.
    """
    parts = []

    if instance.context:
        parts.append(f"Context:\n{instance.context}\n")

    parts.append(instance.question)

    if instance.choices:
        parts.append("\nOptions:")
        for choice in instance.choices:
            parts.append(f"  {choice}")

    parts.append(
        "\nAnswer with the letter of the correct option (A, B, C, or D), "
        "then explain your reasoning."
    )

    return "\n".join(parts)


def create_open_ended_prompt(instance: Instance) -> str:
    """Create an open-ended question prompt.

    Args:
        instance: Instance without choices (free-response).

    Returns:
        Formatted open-ended prompt string.
    """
    parts = []

    if instance.context:
        parts.append(f"Context:\n{instance.context}\n")

    parts.append(instance.question)
    parts.append("\nProvide a clear, detailed answer.")

    return "\n".join(parts)


def create_prompt(instance: Instance) -> str:
    """Create the appropriate prompt type based on the instance.

    Args:
        instance: The benchmark instance.

    Returns:
        Formatted prompt string.
    """
    if instance.choices:
        return create_mcq_prompt(instance)
    return create_open_ended_prompt(instance)
