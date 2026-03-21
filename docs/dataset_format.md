# Dataset Format

BrokerBench uses JSONL (JSON Lines) as the universal interchange format for both datasets and predictions.

## Instance Schema

Each line in a dataset JSONL file represents one benchmark instance:

```json
{
  "instance_id": "licensing-national-042",
  "domain": "licensing",
  "subdomain": "contracts_and_agency",
  "cognitive_level": "analysis",
  "exam_type": "broker",
  "question": "A buyer signs a purchase agreement with a 10-day inspection contingency...",
  "choices": ["A. The contract is void", "B. The buyer may rescind", "C. ...", "D. ..."],
  "expected_answer": "B",
  "explanation": "Under the inspection contingency, the buyer has the right to...",
  "source_outline": "IV. Real Estate Contracts and Agency, D. Sales contract",
  "difficulty": "hard",
  "context": "",
  "metadata": {}
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `instance_id` | string | Unique identifier (e.g., `licensing-national-042`) |
| `domain` | string | One of: `licensing`, `underwriting`, `legal`, `marketing` |
| `question` | string | The question or task prompt |
| `expected_answer` | string | Gold-label expected answer |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `subdomain` | string | Topic area within the domain |
| `choices` | list[string] | Multiple-choice options (licensing domain) |
| `explanation` | string | Explanation of the correct answer |
| `cognitive_level` | string | `knowledge`, `application`, or `analysis` |
| `exam_type` | string | `salesperson` or `broker` |
| `source_outline` | string | Reference to source content outline |
| `difficulty` | string | `easy`, `medium`, or `hard` |
| `context` | string | Additional context (contract excerpt, loan data) |
| `metadata` | dict[str, str] | String key-value pairs for additional data |

## Prediction Schema

```json
{
  "instance_id": "licensing-national-042",
  "model_name_or_path": "claude-3-sonnet",
  "prediction": "B",
  "reasoning": "The inspection contingency gives the buyer the right to...",
  "raw_output": "B. The buyer may rescind...",
  "metadata": {}
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `instance_id` | string | Must match an instance's `instance_id` |
| `model_name_or_path` | string | Identifier for the model |
| `prediction` | string | The model's answer |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `reasoning` | string | Chain-of-thought or explanation |
| `raw_output` | string | Full raw model output |
| `metadata` | dict[str, str] | String key-value pairs for additional data |

## Dataset Files

Built-in datasets are stored in `brokerbench/resources/datasets/`:

| File | Domain | Description |
|------|--------|-------------|
| `licensing_national.jsonl` | Licensing | National exam questions (salesperson + broker) |
| `licensing_broker.jsonl` | Licensing | Broker-specific advanced questions |
| `underwriting.jsonl` | Underwriting | ULAD loan file compliance tasks |
| `legal_contracts.jsonl` | Legal | Contract analysis tasks |
| `marketing.jsonl` | Marketing | Content quality evaluation tasks |
