"""Tests for BrokerBench grading and evaluation logic."""

from brokerbench.harness.constants import Domain, ResolutionStatus
from brokerbench.harness.grading import (
    DomainResult,
    EvalResult,
    InstanceResult,
)
from brokerbench.harness.run_evaluation import (
    compute_composite_score,
    compute_domain_results,
    grade_instance,
)
from brokerbench.harness.types import Instance, Prediction


def _make_instance(
    instance_id: str = "test-001",
    domain: Domain = Domain.LICENSING,
    expected: str = "B",
    choices: list[str] | None = None,
) -> Instance:
    if choices is None:
        choices = ["A. Option A", "B. Option B", "C. Option C", "D. Option D"]
    return Instance(
        instance_id=instance_id,
        domain=domain,
        question="Test question?",
        choices=choices,
        expected_answer=expected,
    )


def _make_prediction(
    instance_id: str = "test-001",
    prediction: str = "B",
) -> Prediction:
    return Prediction(
        instance_id=instance_id,
        model_name_or_path="test-model",
        prediction=prediction,
    )


class TestGradeInstance:
    def test_correct_mcq(self) -> None:
        instance = _make_instance(expected="B")
        prediction = _make_prediction(prediction="B")
        result = grade_instance(instance, prediction)
        assert result.status == ResolutionStatus.RESOLVED
        assert result.aggregate_score == 1.0

    def test_incorrect_mcq(self) -> None:
        instance = _make_instance(expected="B")
        prediction = _make_prediction(prediction="A")
        result = grade_instance(instance, prediction)
        assert result.status == ResolutionStatus.UNRESOLVED
        assert result.aggregate_score == 0.0

    def test_extracts_letter(self) -> None:
        instance = _make_instance(expected="C")
        prediction = _make_prediction(prediction="C. The correct answer is C because...")
        result = grade_instance(instance, prediction)
        assert result.status == ResolutionStatus.RESOLVED

    def test_does_not_extract_from_prose(self) -> None:
        """Ensure letters in English words don't get extracted as the answer."""
        instance = _make_instance(expected="B")
        prediction = _make_prediction(
            prediction="According to the inspection contingency, the answer is B."
        )
        result = grade_instance(instance, prediction)
        assert result.status == ResolutionStatus.RESOLVED
        assert result.aggregate_score == 1.0


class TestComputeDomainResults:
    def test_single_domain(self) -> None:
        results = [
            InstanceResult(
                instance_id="t-001",
                domain=Domain.LICENSING,
                status=ResolutionStatus.RESOLVED,
                aggregate_score=1.0,
            ),
            InstanceResult(
                instance_id="t-002",
                domain=Domain.LICENSING,
                status=ResolutionStatus.UNRESOLVED,
                aggregate_score=0.0,
            ),
        ]
        domain_results = compute_domain_results(results)
        assert Domain.LICENSING in domain_results
        dr = domain_results[Domain.LICENSING]
        assert dr.total_instances == 2
        assert dr.resolved_count == 1
        assert dr.mean_score == 0.5

    def test_multiple_domains(self) -> None:
        results = [
            InstanceResult(
                instance_id="l-001",
                domain=Domain.LICENSING,
                status=ResolutionStatus.RESOLVED,
                aggregate_score=1.0,
            ),
            InstanceResult(
                instance_id="u-001",
                domain=Domain.UNDERWRITING,
                status=ResolutionStatus.RESOLVED,
                aggregate_score=1.0,
            ),
        ]
        domain_results = compute_domain_results(results)
        assert len(domain_results) == 2
        assert domain_results[Domain.LICENSING].mean_score == 1.0
        assert domain_results[Domain.UNDERWRITING].mean_score == 1.0


class TestCompositeScore:
    def test_equal_scores(self) -> None:
        domain_results = {
            Domain.LICENSING: DomainResult(
                domain=Domain.LICENSING, mean_score=0.8, total_instances=10
            ),
            Domain.UNDERWRITING: DomainResult(
                domain=Domain.UNDERWRITING, mean_score=0.8, total_instances=10
            ),
            Domain.LEGAL: DomainResult(domain=Domain.LEGAL, mean_score=0.8, total_instances=10),
            Domain.MARKETING: DomainResult(
                domain=Domain.MARKETING, mean_score=0.8, total_instances=10
            ),
        }
        composite = compute_composite_score(domain_results)
        assert abs(composite - 0.8) < 0.01

    def test_weighted_scores(self) -> None:
        domain_results = {
            Domain.LICENSING: DomainResult(
                domain=Domain.LICENSING, mean_score=1.0, total_instances=10
            ),
            Domain.MARKETING: DomainResult(
                domain=Domain.MARKETING, mean_score=0.0, total_instances=10
            ),
        }
        weights = {Domain.LICENSING: 0.5, Domain.MARKETING: 0.5}
        composite = compute_composite_score(domain_results, weights)
        assert abs(composite - 0.5) < 0.01

    def test_empty_results(self) -> None:
        composite = compute_composite_score({})
        assert composite == 0.0


class TestEvalResult:
    def test_summary(self) -> None:
        result = EvalResult(
            run_id="test-run",
            model_name="test-model",
            total_instances=10,
            composite_score=0.75,
            domain_results={
                Domain.LICENSING: DomainResult(
                    domain=Domain.LICENSING,
                    total_instances=10,
                    resolved_count=8,
                    mean_score=0.75,
                ),
            },
        )
        summary = result.summary()
        assert "test-run" in summary
        assert "test-model" in summary
        assert "75.0%" in summary
