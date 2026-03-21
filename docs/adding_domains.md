# Adding New Domains

BrokerBench is designed to be extensible. Here's how to add a new evaluation domain.

## 1. Define the Domain

Add your domain to the `Domain` enum in `brokerbench/harness/constants.py`:

```python
class Domain(str, Enum):
    LICENSING = "licensing"
    UNDERWRITING = "underwriting"
    LEGAL = "legal"
    MARKETING = "marketing"
    MY_NEW_DOMAIN = "my_new_domain"  # Add here
```

## 2. Create Dataset Collection

Create a new file in `brokerbench/collect/`:

```python
# brokerbench/collect/my_domain.py

from brokerbench.harness.types import Instance
from brokerbench.harness.constants import Domain

def generate_instances() -> list[Instance]:
    """Generate benchmark instances for the new domain."""
    return [
        Instance(
            instance_id="mydomain-001",
            domain=Domain.MY_NEW_DOMAIN,
            question="Your question here",
            expected_answer="Expected answer",
        ),
        # ... more instances
    ]
```

## 3. Create Scorers

Create a new scorer in `brokerbench/harness/scorers/`:

```python
# brokerbench/harness/scorers/my_domain.py

from brokerbench.harness.grading import ScoreDetail
from brokerbench.harness.types import Instance, Prediction

def score_my_domain(instance: Instance, prediction: Prediction) -> ScoreDetail:
    """Score predictions for the new domain."""
    # Implement your scoring logic
    is_correct = prediction.prediction.strip() == instance.expected_answer.strip()
    return ScoreDetail(
        scorer_name="my_domain_accuracy",
        score=1.0 if is_correct else 0.0,
    )
```

## 4. Generate Dataset File

Write instances to a JSONL file in `brokerbench/resources/datasets/`:

```python
from brokerbench.collect.utils import write_instances_jsonl
from brokerbench.collect.my_domain import generate_instances
from pathlib import Path

instances = generate_instances()
write_instances_jsonl(instances, Path("brokerbench/resources/datasets/my_domain.jsonl"))
```

## 5. Update Domain Weights (Optional)

If you want the new domain included in the composite score, update `DEFAULT_DOMAIN_WEIGHTS` in `brokerbench/harness/constants.py`.

## 6. Add Tests

Add tests for your scorer in `tests/test_scorers.py` and for dataset collection in `tests/test_collect.py`.
