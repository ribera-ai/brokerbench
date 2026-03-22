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
# Install
git clone https://github.com/ribera-ai/brokerbench.git
cd brokerbench
pip install -e .

# Run inference against a model (OpenAI, Anthropic, Google, or OpenRouter)
python -m brokerbench.inference.run_api \
    --model_name gpt-4o \
    --dataset all \
    --output_file predictions/gpt-4o.jsonl \
    --provider openai

# Run Gemini models directly
GEMINI_API_KEY=... python -m brokerbench.inference.run_api \
    --model_name gemini-2.5-pro \
    --dataset all \
    --output_file predictions/gemini-2.5-pro.jsonl \
    --provider google

# Or use OpenRouter to access any model
OPENROUTER_API_KEY=sk-or-... python -m brokerbench.inference.run_api \
    --model_name openai/gpt-4o \
    --dataset all \
    --output_file predictions/gpt-4o-or.jsonl \
    --provider openrouter

# Evaluate predictions
python -m brokerbench.harness.run_evaluation \
    --predictions_path predictions/gpt-4o.jsonl \
    --dataset_name all \
    --run_id my-eval-run

# View report
cat logs/run_evaluation/my-eval-run/report.md
```

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

# Run all baselines (Claude Sonnet 4, Claude Opus 4, Gemini 2.5 Pro, GPT-4o, GPT-5)
./scripts/run_baselines.sh

# Or run a single model
./scripts/run_baselines.sh gemini-2.5-pro

# View results
ls logs/run_evaluation/
```

| Provider | Model | CLI |
|----------|-------|-----|
| Anthropic | `claude-sonnet-4-20250514` | `--provider anthropic` |
| Anthropic | `claude-opus-4-20250514` | `--provider anthropic` |
| Google | `gemini-2.5-pro` | `--provider google` |
| OpenAI | `gpt-4o` | `--provider openai` |
| OpenAI | `gpt-5` | `--provider openai` |

## Running Against BrokerBot

```bash
# Start BrokerBot locally (from monorepo)
# Then run BrokerBench against it
python -m brokerbench.inference.run_brokerbot \
    --agent_url http://localhost:3000/api/agent \
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
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Lint
ruff check brokerbench/ tests/

# Type check
mypy brokerbench/
```

## License

MIT - see [LICENSE](LICENSE).
