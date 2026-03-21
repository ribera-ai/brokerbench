"""Tests for BrokerBench scorers."""

from brokerbench.harness.constants import CognitiveLevel, Domain, ExamType
from brokerbench.harness.scorers.legal import score_issue_spotting
from brokerbench.harness.scorers.licensing import score_licensing_mcq
from brokerbench.harness.scorers.marketing import score_content_quality
from brokerbench.harness.scorers.underwriting import score_compliance_flag
from brokerbench.harness.types import Instance, Prediction


def _make_mcq_instance(
    instance_id: str = "test-001",
    expected: str = "B",
) -> Instance:
    return Instance(
        instance_id=instance_id,
        domain=Domain.LICENSING,
        subdomain="contracts_and_agency",
        question="Test question?",
        choices=["A. Option A", "B. Option B", "C. Option C", "D. Option D"],
        expected_answer=expected,
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
    )


def _make_prediction(
    instance_id: str = "test-001",
    prediction: str = "B",
    model: str = "test-model",
) -> Prediction:
    return Prediction(
        instance_id=instance_id,
        model_name_or_path=model,
        prediction=prediction,
    )


# --- Licensing MCQ Scorer ---


class TestLicensingMCQScorer:
    def test_correct_answer(self) -> None:
        instance = _make_mcq_instance(expected="B")
        prediction = _make_prediction(prediction="B")
        result = score_licensing_mcq(instance, prediction)
        assert result.score == 1.0
        assert result.scorer_name == "exam_accuracy"

    def test_incorrect_answer(self) -> None:
        instance = _make_mcq_instance(expected="B")
        prediction = _make_prediction(prediction="C")
        result = score_licensing_mcq(instance, prediction)
        assert result.score == 0.0

    def test_case_insensitive(self) -> None:
        instance = _make_mcq_instance(expected="B")
        prediction = _make_prediction(prediction="b")
        result = score_licensing_mcq(instance, prediction)
        assert result.score == 1.0

    def test_extracts_letter_from_explanation(self) -> None:
        instance = _make_mcq_instance(expected="B")
        prediction = _make_prediction(prediction="B. The buyer may rescind the contract.")
        result = score_licensing_mcq(instance, prediction)
        assert result.score == 1.0

    def test_wrong_letter_in_explanation(self) -> None:
        instance = _make_mcq_instance(expected="B")
        prediction = _make_prediction(prediction="A. This is the wrong answer.")
        result = score_licensing_mcq(instance, prediction)
        assert result.score == 0.0

    def test_does_not_extract_from_prose(self) -> None:
        """Ensure letters embedded in English words are not extracted."""
        instance = _make_mcq_instance(expected="B")
        prediction = _make_prediction(
            prediction="According to the inspection contingency, the answer is B."
        )
        result = score_licensing_mcq(instance, prediction)
        assert result.score == 1.0

    def test_answer_is_pattern(self) -> None:
        instance = _make_mcq_instance(expected="C")
        prediction = _make_prediction(prediction="Based on my analysis, the answer is C.")
        result = score_licensing_mcq(instance, prediction)
        assert result.score == 1.0


# --- Compliance Flag Scorer ---


class TestComplianceFlagScorer:
    def test_correct_yes(self) -> None:
        instance = Instance(
            instance_id="uw-001",
            domain=Domain.UNDERWRITING,
            question="Is this loan compliant?",
            expected_answer="yes",
        )
        prediction = _make_prediction(instance_id="uw-001", prediction="yes")
        result = score_compliance_flag(instance, prediction)
        assert result.score == 1.0

    def test_correct_no(self) -> None:
        instance = Instance(
            instance_id="uw-002",
            domain=Domain.UNDERWRITING,
            question="Is this loan compliant?",
            expected_answer="no",
        )
        prediction = _make_prediction(instance_id="uw-002", prediction="no")
        result = score_compliance_flag(instance, prediction)
        assert result.score == 1.0

    def test_synonym_flag_for_yes(self) -> None:
        instance = Instance(
            instance_id="uw-003",
            domain=Domain.UNDERWRITING,
            question="Is this flagged?",
            expected_answer="flag",
        )
        prediction = _make_prediction(instance_id="uw-003", prediction="yes")
        result = score_compliance_flag(instance, prediction)
        assert result.score == 1.0

    def test_unrecognized_format(self) -> None:
        instance = Instance(
            instance_id="uw-004",
            domain=Domain.UNDERWRITING,
            question="Is this compliant?",
            expected_answer="yes",
        )
        prediction = _make_prediction(instance_id="uw-004", prediction="maybe")
        result = score_compliance_flag(instance, prediction)
        assert result.score == 0.0
        assert result.metadata.get("error") == "unrecognized_prediction_format"


# --- Issue Spotting Scorer ---


class TestIssueSpottingScorer:
    def test_exact_match(self) -> None:
        instance = Instance(
            instance_id="legal-001",
            domain=Domain.LEGAL,
            question="What issue is in this clause?",
            expected_answer="Missing inspection contingency",
        )
        prediction = _make_prediction(
            instance_id="legal-001",
            prediction="Missing inspection contingency",
        )
        result = score_issue_spotting(instance, prediction)
        assert result.score == 1.0

    def test_case_insensitive_match(self) -> None:
        instance = Instance(
            instance_id="legal-002",
            domain=Domain.LEGAL,
            question="What issue?",
            expected_answer="Missing Contingency",
        )
        prediction = _make_prediction(
            instance_id="legal-002",
            prediction="missing contingency",
        )
        result = score_issue_spotting(instance, prediction)
        assert result.score == 1.0


# --- Content Quality Scorer ---


class TestContentQualityScorer:
    def test_empty_response(self) -> None:
        instance = Instance(
            instance_id="mkt-001",
            domain=Domain.MARKETING,
            question="Write a listing description.",
            expected_answer="A great listing.",
        )
        prediction = _make_prediction(instance_id="mkt-001", prediction="")
        result = score_content_quality(instance, prediction)
        assert result.score == 0.0

    def test_short_response(self) -> None:
        instance = Instance(
            instance_id="mkt-002",
            domain=Domain.MARKETING,
            question="Write a listing description.",
            expected_answer="A great listing.",
        )
        prediction = _make_prediction(instance_id="mkt-002", prediction="Nice house.")
        result = score_content_quality(instance, prediction)
        assert result.score == 0.25

    def test_medium_response(self) -> None:
        instance = Instance(
            instance_id="mkt-003",
            domain=Domain.MARKETING,
            question="Write a listing description.",
            expected_answer="A great listing.",
        )
        prediction = _make_prediction(
            instance_id="mkt-003",
            prediction="This is a beautiful 3-bedroom home located in a quiet neighborhood.",
        )
        result = score_content_quality(instance, prediction)
        assert result.score == 0.5

    def test_long_response(self) -> None:
        instance = Instance(
            instance_id="mkt-004",
            domain=Domain.MARKETING,
            question="Write a listing description.",
            expected_answer="A great listing.",
        )
        prediction = _make_prediction(
            instance_id="mkt-004",
            prediction="A" * 201,
        )
        result = score_content_quality(instance, prediction)
        assert result.score == 0.75
