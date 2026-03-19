"""Score computation and grading logic for BrokerBench."""

from __future__ import annotations

from pydantic import BaseModel, Field

from brokerbench.harness.constants import Domain, ResolutionStatus


class ScoreDetail(BaseModel):
    """A single scorer's result for one instance."""

    scorer_name: str
    score: float = Field(ge=0.0, le=1.0)
    metadata: dict[str, str] = Field(default_factory=dict)


class InstanceResult(BaseModel):
    """Full evaluation result for a single instance."""

    instance_id: str
    domain: Domain
    status: ResolutionStatus
    scores: list[ScoreDetail] = Field(default_factory=list)
    aggregate_score: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Weighted average of individual scores"
    )
    error: str | None = None


class DomainResult(BaseModel):
    """Aggregated results for a single domain."""

    domain: Domain
    total_instances: int = 0
    resolved_count: int = 0
    error_count: int = 0
    mean_score: float = 0.0
    scores_by_scorer: dict[str, float] = Field(default_factory=dict)


class EvalResult(BaseModel):
    """Top-level evaluation result for a full benchmark run."""

    run_id: str
    model_name: str
    total_instances: int = 0
    composite_score: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Weighted composite across all domains"
    )
    domain_results: dict[Domain, DomainResult] = Field(default_factory=dict)
    instance_results: list[InstanceResult] = Field(default_factory=list)

    def summary(self) -> str:
        """Return a human-readable summary of the evaluation."""
        lines = [
            f"BrokerBench Evaluation: {self.run_id}",
            f"Model: {self.model_name}",
            f"Instances: {self.total_instances}",
            f"Composite Score: {self.composite_score:.1%}",
            "",
            "Domain Breakdown:",
        ]
        for domain, result in self.domain_results.items():
            lines.append(
                f"  {domain.value:<15} "
                f"{result.mean_score:.1%} "
                f"({result.resolved_count}/{result.total_instances} resolved)"
            )
        return "\n".join(lines)
