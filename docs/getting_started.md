# Getting Started with BrokerBench

## Installation

```bash
git clone https://github.com/ribera-ai/brokerbench.git
cd brokerbench
uv sync
```

`uv sync` installs the project plus the dev dependency group
(pytest, ruff, mypy) into `.venv/`.

## Prerequisites

- Python 3.12+ (managed automatically by uv)
- API keys for the model you want to evaluate (set as environment variables):
  - `OPENAI_API_KEY` for OpenAI models
  - `ANTHROPIC_API_KEY` for Anthropic models
  - `GEMINI_API_KEY` for Google models
  - `OPENROUTER_API_KEY` for OpenRouter models

## Running Your First Evaluation

### 1. Generate Predictions

Run a model against the benchmark dataset:

```bash
uv run python -m brokerbench.inference.run_api \
    --model_name gpt-5.5 \
    --dataset all \
    --output_file predictions/gpt-5.5.jsonl \
    --provider openai
```

### 2. Evaluate Predictions

Grade the predictions against gold labels:

```bash
uv run python -m brokerbench.harness.run_evaluation \
    --predictions_path predictions/gpt-5.5.jsonl \
    --dataset_name all \
    --run_id my-first-run
```

### 3. View Results

```bash
cat logs/run_evaluation/my-first-run/report.md
```

The report includes:
- Composite score (weighted average across domains)
- Per-domain breakdown
- Per-scorer breakdown
- Instance-level results in JSON format

## Evaluating an Agent Endpoint

`run_http` runs the bench against any agent that accepts a JSON POST —
the request body is a template (`{message}` is the prompt; `{key}` comes
from `--var`, `{key?}` drops when unset) and `--response_field` picks the
answer text out of the JSON response.

```bash
uv run python -m brokerbench.inference.run_http \
    --endpoint http://localhost:8080/chat \
    --body '{"input": "{message}"}' \
    --response_field text \
    --dataset all \
    --output_file predictions/my-agent.jsonl
```

### BrokerBot

For BrokerBot's V2 agent gateway (`POST /generate`, channel pipeline),
use the built-in preset — `run_brokerbot` is a convenience wrapper with
the same flags:

```bash
uv run python -m brokerbench.inference.run_brokerbot \
    --agent_url http://localhost:4200/generate \
    --team_id $TEAM_ID --user_id $USER_ID \
    --agent_id $AGENT_ID --auth_token $JWT \
    --dataset all \
    --output_file predictions/brokerbot.jsonl

uv run python -m brokerbench.harness.run_evaluation \
    --predictions_path predictions/brokerbot.jsonl \
    --run_id brokerbot-eval
```
