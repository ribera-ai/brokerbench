# BrokerBench

A benchmark for evaluating real estate AI agents. Inspired by [SWE-bench](https://github.com/swe-bench/SWE-bench).

## Overview

BrokerBench measures how well AI agents handle real estate tasks across four domains:

| Domain | Focus | Scoring |
|--------|-------|---------|
| **Licensing** | National exam questions (PSI/Pearson VUE) | MCQ accuracy, explanation quality |
| **Underwriting** | ULAD loan file compliance analysis | Compliance flag F1, field extraction |
| **Legal** | Contract issue-spotting and clause extraction | Precision/recall, rule application |
| **Marketing** | Content quality for AI discoverability | Schema.org, FAQ structure, content quality |

## Quick Start

```bash
# Install (uv — https://docs.astral.sh/uv/)
git clone https://github.com/ribera-ai/brokerbench.git
cd brokerbench
uv sync

# Run inference against a model (OpenAI, Anthropic, Google, or OpenRouter)
uv run python -m brokerbench.inference.run_api \
    --model_name gpt-5.5 \
    --dataset all \
    --output_file predictions/gpt-5.5.jsonl \
    --provider openai

# Run Gemini models directly
GEMINI_API_KEY=... uv run python -m brokerbench.inference.run_api \
    --model_name gemini-4-argon \
    --dataset all \
    --output_file predictions/gemini-4-argon.jsonl \
    --provider google

# Or use OpenRouter to access any model
OPENROUTER_API_KEY=sk-or-... uv run python -m brokerbench.inference.run_api \
    --model_name openai/gpt-5.5 \
    --dataset all \
    --output_file predictions/gpt-5.5-or.jsonl \
    --provider openrouter

# Evaluate predictions
uv run python -m brokerbench.harness.run_evaluation \
    --predictions_path predictions/gpt-5.5.jsonl \
    --dataset_name all \
    --run_id my-eval-run

# View report
cat logs/run_evaluation/my-eval-run/report.md
```

Requests run with bounded parallelism (`--max_concurrency`, default 8;
`BROKERBENCH_MAX_CONCURRENCY` also works). Output files are always
written in dataset order regardless of completion order.

Reasoning models (GPT-5/6, Claude 4.6+/5.x, Gemini 3/4) are called
without `temperature` and get a 4096-token output budget by default —
raise it with `BROKERBENCH_MAX_TOKENS` if a deep-thinking model
truncates.

## Architecture

BrokerBench follows the same three-module architecture as SWE-bench:

```
brokerbench/
  collect/      # Dataset creation & curation
  inference/    # Run models against the benchmark
  harness/      # Evaluation & grading
  resources/    # Static datasets (JSONL)
```

**Data flow**: Datasets (JSONL) -> Inference (model predictions) -> Harness (grading) -> Report

## Dataset Format

Each instance is a JSONL line:

```json
{
  "instance_id": "licensing-national-042",
  "domain": "licensing",
  "subdomain": "contracts_and_agency",
  "cognitive_level": "analysis",
  "question": "A buyer signs a purchase agreement with a 10-day inspection contingency...",
  "choices": ["A. The contract is void", "B. The buyer may rescind", "C. ...", "D. ..."],
  "expected_answer": "B",
  "explanation": "Under the inspection contingency, the buyer has the right to..."
}
```

## Running Baseline Frontier Tests

Run all frontier models to establish baseline scores:

```bash
# Set API keys for the providers you want to benchmark
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...
export GEMINI_API_KEY=...
export OPENROUTER_API_KEY=...   # used for the newer frontier models

# Naive baselines first (always-A/B/C/D, uniform-random, most-common)
./scripts/run_baselines.sh naive

# Then real models
./scripts/run_baselines.sh

# Or run a single model
./scripts/run_baselines.sh gemini-4-argon
./scripts/run_baselines.sh anthropic/claude-fable-5.1

# View results
ls logs/run_evaluation/
```

| Provider   | Model                              | CLI                         |
|------------|------------------------------------|-----------------------------|
| Anthropic  | `claude-sonnet-5-5`                | `--provider anthropic`      |
| Anthropic  | `claude-opus-5-5`                  | `--provider anthropic`      |
| Google     | `gemini-4-argon`                   | `--provider google`         |
| OpenAI     | `gpt-5.5`                          | `--provider openai`         |
| OpenAI     | `gpt-6.1-sol`                      | `--provider openai`         |
| OpenRouter | `anthropic/claude-fable-5.1`       | `--provider openrouter`     |
| OpenRouter | `google/gemini-3.1-pro-preview`    | `--provider openrouter`     |
| OpenRouter | `moonshotai/kimi-k3`               | `--provider openrouter`     |
| OpenRouter | `mistralai/mistral-large-2512`     | `--provider openrouter`     |
| OpenRouter | `x-ai/grok-4.7`                    | `--provider openrouter`     |

Read [`docs/methodology.md`](docs/methodology.md) before publishing
any cross-model comparison — in particular the answer-position
shuffle and the naive baseline floors that every real-model score
should clear.

## Running Against Any Agent Endpoint

`run_http` points the bench at any agent that accepts a JSON POST. The
request body is a template — `{message}` is the benchmark prompt;
`{message_id}`, `{chat_id}`, `{instance_id}` are generated per request;
any other `{key}` is filled from `--var key=value`, and `{key?}` drops the
field when unset. `$ENV` references expand in templates and headers.

```bash
uv run python -m brokerbench.inference.run_http \
    --endpoint http://localhost:8080/chat \
    --body '{"input": "{message}"}' \
    --header 'Authorization: Bearer $MY_AGENT_TOKEN' \
    --response_field text \
    --dataset all \
    --output_file predictions/my-agent.jsonl
```

### BrokerBot preset

The built-in `brokerbot` preset targets the V2 agent gateway's
`POST /generate` (the same channel pipeline Slack/SMS/web chat use). Auth
is a Bearer JWT signed with `BETTER_AUTH_SECRET` or a Better Auth session
token. `run_brokerbot` keeps the same flags as a convenience wrapper.

```bash
# Start the agent gateway locally (from the brokerbot monorepo), then:
uv run python -m brokerbench.inference.run_http \
    --preset brokerbot \
    --var team_id=$TEAM_ID --var user_id=$USER_ID \
    --var agent_id=$AGENT_ID --var auth_token=$JWT \
    --dataset all \
    --output_file predictions/brokerbot.jsonl
```

## Custom Agents

Implement the `CustomAgentAdapter` interface:

```python
from pathlib import Path
from brokerbench.inference.run_custom import CustomAgentAdapter
from brokerbench.harness.types import Instance, Prediction

class MyAgent(CustomAgentAdapter):
    def predict(self, instance: Instance) -> Prediction:
        response = my_agent.ask(instance.question)
        return Prediction(
            instance_id=instance.instance_id,
            model_name_or_path="my-agent",
            prediction=response.answer,
        )

adapter = MyAgent()
adapter.run_benchmark(dataset_path="all", output_path=Path("predictions.jsonl"))
```

## Development

```bash
# Install everything (uv sync includes the dev group by default)
uv sync

# Run tests
uv run pytest tests/ -v

# Lint
uv run ruff check brokerbench/ tests/

# Type check
uv run mypy brokerbench/
```

## License

MIT - see [LICENSE](LICENSE).
