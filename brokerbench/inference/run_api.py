"""Run inference against the benchmark using OpenAI / Anthropic / Google / OpenRouter APIs.

Usage:
    python -m brokerbench.inference.run_api \
        --model_name claude-3-sonnet \
        --dataset brokerbench/resources/datasets/licensing_national.jsonl \
        --output_file predictions/claude-3-sonnet.jsonl
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from rich.console import Console
from tqdm import tqdm

from brokerbench.harness.types import Instance, Prediction
from brokerbench.harness.utils import extract_mcq_answer
from brokerbench.inference import build_prompt, load_instances

console = Console()

# Reasoning-style frontier models (Claude 4.x thinking, GPT-5, Gemini
# 2.5 Pro thinking, Grok 4, Kimi K2 thinking, etc.) routinely emit
# multi-thousand-token chain-of-thought before the final letter.  4096
# is a safe default; override with ``BROKERBENCH_MAX_TOKENS`` for very
# verbose deep-reasoning runs.
_DEFAULT_MAX_TOKENS = 4096


def _max_tokens() -> int:
    """Resolve max output tokens from the env, falling back to the default."""
    raw = os.environ.get("BROKERBENCH_MAX_TOKENS", "").strip()
    if not raw:
        return _DEFAULT_MAX_TOKENS
    try:
        value = int(raw)
    except ValueError:
        console.print(
            f"[yellow]Invalid BROKERBENCH_MAX_TOKENS={raw!r}; using default {_DEFAULT_MAX_TOKENS}"
            "[/yellow]"
        )
        return _DEFAULT_MAX_TOKENS
    if value < 64:
        console.print(f"[yellow]BROKERBENCH_MAX_TOKENS={value} too small; using 64[/yellow]")
        return 64
    return value


def run_openai(
    instances: list[Instance],
    model_name: str,
    output_path: Path,
) -> list[Prediction]:
    """Run inference using the OpenAI API.

    Args:
        instances: List of benchmark instances to evaluate.
        model_name: OpenAI model identifier (e.g. 'gpt-4o').
        output_path: Path to write prediction JSONL.

    Returns:
        List of Prediction objects.
    """
    try:
        from openai import OpenAI
    except ImportError:
        console.print("[red]openai package not installed. Run: pip install openai[/red]")
        sys.exit(1)

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    predictions: list[Prediction] = []
    max_tokens = _max_tokens()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        for instance in tqdm(instances, desc=f"Running {model_name}"):
            prompt = build_prompt(instance)
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a knowledgeable real estate professional "
                                "taking an evaluation. Answer accurately and concisely."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0,
                    max_tokens=max_tokens,
                )
                raw_output = response.choices[0].message.content or ""

                # Extract answer letter for MCQ
                answer = raw_output
                if instance.choices:
                    extracted = extract_mcq_answer(raw_output)
                    if extracted:
                        answer = extracted

                pred = Prediction(
                    instance_id=instance.instance_id,
                    model_name_or_path=model_name,
                    prediction=answer,
                    reasoning=raw_output,
                    raw_output=raw_output,
                )
            except Exception as e:
                console.print(f"[yellow]Error on {instance.instance_id}: {e}[/yellow]")
                pred = Prediction(
                    instance_id=instance.instance_id,
                    model_name_or_path=model_name,
                    prediction="",
                    reasoning="",
                    raw_output=str(e),
                    metadata={"error": str(e)},
                )

            predictions.append(pred)
            f.write(pred.model_dump_json() + "\n")

    return predictions


def run_anthropic(
    instances: list[Instance],
    model_name: str,
    output_path: Path,
) -> list[Prediction]:
    """Run inference using the Anthropic API.

    Args:
        instances: List of benchmark instances to evaluate.
        model_name: Anthropic model identifier (e.g. 'claude-3-sonnet-20240229').
        output_path: Path to write prediction JSONL.

    Returns:
        List of Prediction objects.
    """
    try:
        from anthropic import Anthropic
    except ImportError:
        console.print("[red]anthropic package not installed. Run: pip install anthropic[/red]")
        sys.exit(1)

    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
    predictions: list[Prediction] = []
    max_tokens = _max_tokens()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        for instance in tqdm(instances, desc=f"Running {model_name}"):
            prompt = build_prompt(instance)
            try:
                response = client.messages.create(
                    model=model_name,
                    max_tokens=max_tokens,
                    temperature=0,
                    system=(
                        "You are a knowledgeable real estate professional "
                        "taking an evaluation. Answer accurately and concisely."
                    ),
                    messages=[{"role": "user", "content": prompt}],
                )
                from anthropic.types import TextBlock

                raw_output = ""
                for block in response.content:
                    if isinstance(block, TextBlock):
                        raw_output = block.text
                        break

                # Extract answer letter for MCQ
                answer = raw_output
                if instance.choices:
                    extracted = extract_mcq_answer(raw_output)
                    if extracted:
                        answer = extracted

                pred = Prediction(
                    instance_id=instance.instance_id,
                    model_name_or_path=model_name,
                    prediction=answer,
                    reasoning=raw_output,
                    raw_output=raw_output,
                )
            except Exception as e:
                console.print(f"[yellow]Error on {instance.instance_id}: {e}[/yellow]")
                pred = Prediction(
                    instance_id=instance.instance_id,
                    model_name_or_path=model_name,
                    prediction="",
                    reasoning="",
                    raw_output=str(e),
                    metadata={"error": str(e)},
                )

            predictions.append(pred)
            f.write(pred.model_dump_json() + "\n")

    return predictions


def run_openrouter(
    instances: list[Instance],
    model_name: str,
    output_path: Path,
) -> list[Prediction]:
    """Run inference using the OpenRouter API.

    OpenRouter uses the OpenAI SDK with a custom base URL.

    Args:
        instances: List of benchmark instances to evaluate.
        model_name: OpenRouter model identifier (e.g. 'openai/gpt-4o',
            'anthropic/claude-3-sonnet').
        output_path: Path to write prediction JSONL.

    Returns:
        List of Prediction objects.
    """
    try:
        from openai import OpenAI
    except ImportError:
        console.print("[red]openai package not installed. Run: pip install openai[/red]")
        sys.exit(1)

    client = OpenAI(
        api_key=os.environ.get("OPENROUTER_API_KEY", ""),
        base_url="https://openrouter.ai/api/v1",
    )
    predictions: list[Prediction] = []
    max_tokens = _max_tokens()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        for instance in tqdm(instances, desc=f"Running {model_name} (OpenRouter)"):
            prompt = build_prompt(instance)
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a knowledgeable real estate professional "
                                "taking an evaluation. Answer accurately and concisely."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0,
                    max_tokens=max_tokens,
                )
                raw_output = response.choices[0].message.content or ""

                # Extract answer letter for MCQ
                answer = raw_output
                if instance.choices:
                    extracted = extract_mcq_answer(raw_output)
                    if extracted:
                        answer = extracted

                pred = Prediction(
                    instance_id=instance.instance_id,
                    model_name_or_path=model_name,
                    prediction=answer,
                    reasoning=raw_output,
                    raw_output=raw_output,
                )
            except Exception as e:
                console.print(f"[yellow]Error on {instance.instance_id}: {e}[/yellow]")
                pred = Prediction(
                    instance_id=instance.instance_id,
                    model_name_or_path=model_name,
                    prediction="",
                    reasoning="",
                    raw_output=str(e),
                    metadata={"error": str(e)},
                )

            predictions.append(pred)
            f.write(pred.model_dump_json() + "\n")

    return predictions


def run_google(
    instances: list[Instance],
    model_name: str,
    output_path: Path,
) -> list[Prediction]:
    """Run inference using the Google Gemini API.

    Args:
        instances: List of benchmark instances to evaluate.
        model_name: Gemini model identifier (e.g. 'gemini-2.5-pro').
        output_path: Path to write prediction JSONL.

    Returns:
        List of Prediction objects.
    """
    try:
        from google import genai
    except ImportError:
        console.print(
            "[red]google-genai package not installed. Run: pip install google-genai[/red]"
        )
        sys.exit(1)

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
    predictions: list[Prediction] = []
    max_tokens = _max_tokens()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        for instance in tqdm(instances, desc=f"Running {model_name}"):
            prompt = build_prompt(instance)
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config={
                        "system_instruction": (
                            "You are a knowledgeable real estate professional "
                            "taking an evaluation. Answer accurately and concisely."
                        ),
                        "temperature": 0,
                        "max_output_tokens": max_tokens,
                    },
                )
                raw_output = response.text or ""

                # Extract answer letter for MCQ
                answer = raw_output
                if instance.choices:
                    extracted = extract_mcq_answer(raw_output)
                    if extracted:
                        answer = extracted

                pred = Prediction(
                    instance_id=instance.instance_id,
                    model_name_or_path=model_name,
                    prediction=answer,
                    reasoning=raw_output,
                    raw_output=raw_output,
                )
            except Exception as e:
                console.print(f"[yellow]Error on {instance.instance_id}: {e}[/yellow]")
                pred = Prediction(
                    instance_id=instance.instance_id,
                    model_name_or_path=model_name,
                    prediction="",
                    reasoning="",
                    raw_output=str(e),
                    metadata={"error": str(e)},
                )

            predictions.append(pred)
            f.write(pred.model_dump_json() + "\n")

    return predictions


def main() -> None:
    """CLI entry point for API-based inference."""
    parser = argparse.ArgumentParser(
        description="Run a model against BrokerBench using API inference."
    )
    parser.add_argument(
        "--model_name",
        type=str,
        required=True,
        help="Model identifier (e.g. 'gpt-4o', 'claude-3-sonnet-20240229',"
        " 'gemini-2.5-pro', 'openai/gpt-4o' for OpenRouter).",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="Path to dataset JSONL file, or 'all' for all built-in datasets.",
    )
    parser.add_argument(
        "--output_file",
        type=Path,
        required=True,
        help="Path to write prediction JSONL file.",
    )
    parser.add_argument(
        "--provider",
        type=str,
        default="openai",
        choices=["openai", "anthropic", "google", "openrouter"],
        help="API provider to use (default: openai).",
    )
    args = parser.parse_args()

    instances = load_instances(args.dataset)
    console.print(f"Loaded {len(instances)} instances")

    if args.provider == "openai":
        run_openai(instances, args.model_name, args.output_file)
    elif args.provider == "anthropic":
        run_anthropic(instances, args.model_name, args.output_file)
    elif args.provider == "google":
        run_google(instances, args.model_name, args.output_file)
    elif args.provider == "openrouter":
        run_openrouter(instances, args.model_name, args.output_file)

    console.print(f"[green]Predictions written to {args.output_file}[/green]")


if __name__ == "__main__":
    main()
