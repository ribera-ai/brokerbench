"""BrokerBench: A benchmark for evaluating real estate AI agents."""

__version__ = "0.1.0"

from brokerbench.harness.constants import CognitiveLevel, Domain
from brokerbench.harness.grading import EvalResult
from brokerbench.harness.types import Instance, Prediction

__all__ = [
    "Domain",
    "CognitiveLevel",
    "EvalResult",
    "Instance",
    "Prediction",
]
