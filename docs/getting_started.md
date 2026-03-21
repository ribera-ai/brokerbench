# Getting Started with BrokerBench

## Installation

```bash
git clone https://github.com/ribera-ai/brokerbench.git
cd brokerbench
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

## Prerequisites

- Python 3.10+
- API keys for the model you want to evaluate (set as environment variables):
  - `OPENAI_API_KEY` for OpenAI models
  - `ANTHROPIC_API_KEY` for Anthropic models

## Running Your First Evaluation

### 1. Generate Predictions

Run a model against the benchmark dataset:

```bash
python -m brokerbench.inference.run_api \
    --model_name gpt-4o \
    --dataset all \
    --output_file predictions/gpt-4o.jsonl \
    --provider openai
```

### 2. Evaluate Predictions

Grade the predictions against gold labels:

```bash
python -m brokerbench.harness.run_evaluation \
    --predictions_path predictions/gpt-4o.jsonl \
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

## Evaluating BrokerBot

If you have the BrokerBot monorepo running locally:

```bash
python -m brokerbench.inference.run_brokerbot \
    --agent_url http://localhost:3000/api/agent \
    --dataset all \
    --output_file predictions/brokerbot.jsonl

python -m brokerbench.harness.run_evaluation \
    --predictions_path predictions/brokerbot.jsonl \
    --run_id brokerbot-eval
```
