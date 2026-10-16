"""Run inference against the benchmark using OpenAI / Anthropic / Google / OpenRouter APIs.

Usage:
    python -m brokerbench.inference.run_api \
        --model_name claude-sonnet-5-5 \
        --dataset brokerbench/resources/datasets/licensing.jsonl \
        --output_file predictions/claude-sonnet-5-5.jsonl \
        --provider anthropic
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from rich.console import Console
from tqdm import tqdm

from brokerbench.harness.types import Instance, Prediction
from brokerbench.harness.utils import extract_mcq_answer
from brokerbench.inference import build_prompt, load_instances

console = Console()

SYSTEM_PROMPT = (
    "You are a knowledgeable real estate professional "
    "taking an evaluation. Answer accurately and concisely."
)

# Reasoning-style frontier models (Claude 5.x adaptive thinking, GPT-5/6,
# Gemini 3/4 thinking, Grok 4, Kimi K3, etc.) routinely emit
# multi-thousand-token chain-of-thought before the final letter.  4096
# is a safe default; override with ``BROKERBENCH_MAX_TOKENS`` for very
# verbose deep-reasoning runs.
_DEFAULT_MAX_TOKENS = 4096

# In-flight request parallelism.  Provider rate limits still apply, so
# keep this modest; override with ``--max_concurrency`` or
# ``BROKERBENCH_MAX_CONCURRENCY``.
_DEFAULT_MAX_CONCURRENCY = 8


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


def _max_concurrency(cli_value: int | None) -> int:
    """Resolve request parallelism: CLI flag > env > default."""
    if cli_value is not None:
        return max(1, cli_value)
    raw = os.environ.get("BROKERBENCH_MAX_CONCURRENCY", "").strip()
    if raw:
        try:
            return max(1, int(raw))
        except ValueError:
            console.print(
                f"[yellow]Invalid BROKERBENCH_MAX_CONCURRENCY={raw!r}; "
                f"using default {_DEFAULT_MAX_CONCURRENCY}[/yellow]"
            )
    return _DEFAULT_MAX_CONCURRENCY


# OpenAI model families that only run as reasoning models.  They reject
# ``temperature`` and ``max_tokens`` on the Chat Completions API, and are
# served through the Responses API here.
_OPENAI_REASONING_RE = re.compile(r"^(gpt-[56]|o[134])")

# Claude models with adaptive thinking (4.6+, 5.x, Fable, Mythos).  These
# do not accept ``temperature``; thinking is managed by the API.
_MODERN_CLAUDE_RE = re.compile(
    r"^(?:anthropic/)?claude-(?:fable|mythos)-|"
    r"^(?:anthropic/)?claude-(?:sonnet|opus|haiku)-(?:4-[6-9]|[5-9]\d*)"
)


def _is_openai_reasoning_model(model_name: str) -> bool:
    """Whether the model runs through the OpenAI Responses API as a reasoner."""
    return bool(_OPENAI_REASONING_RE.match(model_name))


def _is_modern_claude(model_name: str) -> bool:
    """Whether the model has adaptive thinking and rejects ``temperature``."""
    return bool(_MODERN_CLAUDE_RE.search(model_name))


def _call_with_retry(
    fn: Callable[[], str],
    attempts: int = 4,
    base_delay: float = 2.0,
) -> str:
    """Call ``fn`` with exponential backoff on transient failures.

    Args:
        fn: Zero-arg callable returning the model's raw text output.
        attempts: Total attempts before giving up.
        base_delay: Initial backoff in seconds (doubles each retry).

    Returns:
        The raw model output.
    """
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            return fn()
        except Exception as e:
            last_error = e
            if attempt < attempts - 1:
                time.sleep(base_delay * (2**attempt))
    assert last_error is not None
    raise last_error


def _to_prediction(instance: Instance, model_name: str, raw_output: str) -> Prediction:
    """Build a Prediction from raw model output, extracting MCQ letters."""
    answer = raw_output
    if instance.choices:
        extracted = extract_mcq_answer(raw_output)
        if extracted:
            answer = extracted
    return Prediction(
        instance_id=instance.instance_id,
        model_name_or_path=model_name,
        prediction=answer,
        reasoning=raw_output,
        raw_output=raw_output,
    )


def _error_prediction(instance: Instance, model_name: str, error: Exception) -> Prediction:
    """Build a failed Prediction carrying the error in metadata."""
    return Prediction(
        instance_id=instance.instance_id,
        model_name_or_path=model_name,
        prediction="",
        reasoning="",
        raw_output=str(error),
        metadata={"error": str(error)},
    )


def _run_instances(
    instances: list[Instance],
    model_name: str,
    output_path: Path,
    predict: Callable[[Instance], str],
    max_concurrency: int,
) -> list[Prediction]:
    """Run ``predict`` over all instances with bounded parallelism.

    Results are written to ``output_path`` in input order regardless of
    completion order, so prediction files stay stable across runs.

    Args:
        instances: Benchmark instances to evaluate.
        model_name: Model identifier recorded on each prediction.
        output_path: Destination JSONL file.
        predict: Callable returning the raw model text for one instance.
        max_concurrency: Maximum in-flight requests.

    Returns:
        List of Prediction objects in input order.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    predictions: list[Prediction | None] = [None] * len(instances)

    def run_one(index: int, instance: Instance) -> Prediction:
        try:
            raw_output = _call_with_retry(lambda: predict(instance))
            return _to_prediction(instance, model_name, raw_output)
        except Exception as e:
            console.print(f"[yellow]Error on {instance.instance_id}: {e}[/yellow]")
            return _error_prediction(instance, model_name, e)

    if max_concurrency <= 1:
        for i, instance in enumerate(tqdm(instances, desc=f"Running {model_name}")):
            predictions[i] = run_one(i, instance)
    else:
        with ThreadPoolExecutor(max_workers=max_concurrency) as pool:
            futures = {pool.submit(run_one, i, inst): i for i, inst in enumerate(instances)}
            with tqdm(total=len(instances), desc=f"Running {model_name}") as bar:
                for future in as_completed(futures):
                    predictions[futures[future]] = future.result()
                    bar.update(1)

    final = [p for p in predictions if p is not None]
    with open(output_path, "w") as f:
        for pred in final:
            f.write(pred.model_dump_json() + "\n")
    return final


def run_openai(
    instances: list[Instance],
    model_name: str,
    output_path: Path,
    max_concurrency: int = _DEFAULT_MAX_CONCURRENCY,
) -> list[Prediction]:
    """Run inference using the OpenAI API.

    Reasoning models (gpt-5/gpt-6, o-series) are served through the
    Responses API without ``temperature``; legacy chat models use Chat
    Completions with ``temperature=0``.

    Args:
        instances: List of benchmark instances to evaluate.
        model_name: OpenAI model identifier (e.g. 'gpt-5.5').
        output_path: Path to write prediction JSONL.
        max_concurrency: Maximum in-flight requests.

    Returns:
        List of Prediction objects.
    """
    try:
        from openai import OpenAI
    except ImportError:
        console.print("[red]openai package not installed. Run: uv add openai[/red]")
        sys.exit(1)

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    max_tokens = _max_tokens()
    reasoning = _is_openai_reasoning_model(model_name)

    def predict(instance: Instance) -> str:
        prompt = build_prompt(instance)
        if reasoning:
            response = client.responses.create(
                model=model_name,
                instructions=SYSTEM_PROMPT,
                input=prompt,
                max_output_tokens=max_tokens,
            )
            return response.output_text or ""
        chat_response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_completion_tokens=max_tokens,
        )
        return chat_response.choices[0].message.content or ""

    return _run_instances(instances, model_name, output_path, predict, max_concurrency)


def run_anthropic(
    instances: list[Instance],
    model_name: str,
    output_path: Path,
    max_concurrency: int = _DEFAULT_MAX_CONCURRENCY,
) -> list[Prediction]:
    """Run inference using the Anthropic API.

    Claude 4.6+/5.x/Fable/Mythos models use adaptive thinking and reject
    ``temperature``; older Claude models get ``temperature=0``.

    Args:
        instances: List of benchmark instances to evaluate.
        model_name: Anthropic model identifier (e.g. 'claude-sonnet-5-5').
        output_path: Path to write prediction JSONL.
        max_concurrency: Maximum in-flight requests.

    Returns:
        List of Prediction objects.
    """
    try:
        from anthropic import Anthropic
    except ImportError:
        console.print("[red]anthropic package not installed. Run: uv add anthropic[/red]")
        sys.exit(1)

    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
    max_tokens = _max_tokens()
    modern = _is_modern_claude(model_name)

    def predict(instance: Instance) -> str:
        prompt = build_prompt(instance)
        kwargs: dict[str, Any] = {
            "model": model_name,
            "max_tokens": max_tokens,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": prompt}],
        }
        if not modern:
            kwargs["temperature"] = 0
        response = client.messages.create(**kwargs)
        from anthropic.types import TextBlock

        for block in response.content:
            if isinstance(block, TextBlock):
                return block.text
        return ""

    return _run_instances(instances, model_name, output_path, predict, max_concurrency)


def run_openrouter(
    instances: list[Instance],
    model_name: str,
    output_path: Path,
    max_concurrency: int = _DEFAULT_MAX_CONCURRENCY,
) -> list[Prediction]:
    """Run inference using the OpenRouter API.

    OpenRouter uses the OpenAI SDK with a custom base URL.  ``temperature``
    is omitted for reasoning-family models since upstream providers
    (OpenAI reasoning models, Claude 4.6+/5.x) reject it.

    Args:
        instances: List of benchmark instances to evaluate.
        model_name: OpenRouter model identifier (e.g. 'openai/gpt-5.5',
            'anthropic/claude-sonnet-5.5').
        output_path: Path to write prediction JSONL.
        max_concurrency: Maximum in-flight requests.

    Returns:
        List of Prediction objects.
    """
    try:
        from openai import OpenAI
    except ImportError:
        console.print("[red]openai package not installed. Run: uv add openai[/red]")
        sys.exit(1)

    client = OpenAI(
        api_key=os.environ.get("OPENROUTER_API_KEY", ""),
        base_url="https://openrouter.ai/api/v1",
    )
    max_tokens = _max_tokens()
    # The upstream model id follows the provider prefix, e.g. the
    # 'gpt-5.5' in 'openai/gpt-5.5'.
    upstream_id = model_name.split("/", 1)[-1]
    deterministic = not (_is_openai_reasoning_model(upstream_id) or _is_modern_claude(model_name))

    def predict(instance: Instance) -> str:
        prompt = build_prompt(instance)
        kwargs: dict[str, Any] = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": max_tokens,
        }
        if deterministic:
            kwargs["temperature"] = 0
        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content or ""

    return _run_instances(instances, model_name, output_path, predict, max_concurrency)


def run_google(
    instances: list[Instance],
    model_name: str,
    output_path: Path,
    max_concurrency: int = _DEFAULT_MAX_CONCURRENCY,
) -> list[Prediction]:
    """Run inference using the Google Gemini API.

    Args:
        instances: List of benchmark instances to evaluate.
        model_name: Gemini model identifier (e.g. 'gemini-4-argon').
        output_path: Path to write prediction JSONL.
        max_concurrency: Maximum in-flight requests.

    Returns:
        List of Prediction objects.
    """
    try:
        from google import genai
        from google.genai import types as genai_types
    except ImportError:
        console.print("[red]google-genai package not installed. Run: uv add google-genai[/red]")
        sys.exit(1)

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
    max_tokens = _max_tokens()

    def predict(instance: Instance) -> str:
        prompt = build_prompt(instance)
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0,
                max_output_tokens=max_tokens,
            ),
        )
        return response.text or ""

    return _run_instances(instances, model_name, output_path, predict, max_concurrency)


def main() -> None:
    """CLI entry point for API-based inference."""
    parser = argparse.ArgumentParser(
        description="Run a model against BrokerBench using API inference."
    )
    parser.add_argument(
        "--model_name",
        type=str,
        required=True,
        help="Model identifier (e.g. 'gpt-5.5', 'claude-sonnet-5-5',"
        " 'gemini-4-argon', 'openai/gpt-5.5' for OpenRouter).",
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
    parser.add_argument(
        "--max_concurrency",
        type=int,
        default=None,
        help="Max in-flight requests (default: 8, or BROKERBENCH_MAX_CONCURRENCY).",
    )
    args = parser.parse_args()

    instances = load_instances(args.dataset)
    console.print(f"Loaded {len(instances)} instances")

    max_concurrency = _max_concurrency(args.max_concurrency)
    if args.provider == "openai":
        run_openai(instances, args.model_name, args.output_file, max_concurrency)
    elif args.provider == "anthropic":
        run_anthropic(instances, args.model_name, args.output_file, max_concurrency)
    elif args.provider == "google":
        run_google(instances, args.model_name, args.output_file, max_concurrency)
    elif args.provider == "openrouter":
        run_openrouter(instances, args.model_name, args.output_file, max_concurrency)

    console.print(f"[green]Predictions written to {args.output_file}[/green]")


if __name__ == "__main__":
    main()
