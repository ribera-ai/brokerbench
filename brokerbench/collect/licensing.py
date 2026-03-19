"""Dataset collection for Licensing Exam domain.

Generates original exam-style questions from Pearson VUE / PSI
national real estate licensing exam content outlines.
"""

from __future__ import annotations

from brokerbench.harness.constants import CognitiveLevel, Domain, ExamType
from brokerbench.harness.types import Instance

# Placeholder: In Phase 2, this module will contain logic to
# generate and curate 80+ original licensing exam questions
# covering all 8 topic areas at all 3 cognitive levels.

SAMPLE_LICENSING_INSTANCES: list[Instance] = [
    Instance(
        instance_id="licensing-national-001",
        domain=Domain.LICENSING,
        subdomain="contracts_and_agency",
        question=(
            "A buyer signs a purchase agreement that includes a 10-day inspection "
            "contingency. On day 8, the inspector discovers significant foundation "
            "damage. The buyer wants to cancel the contract. Which of the following "
            "is correct?"
        ),
        choices=[
            "A. The contract is automatically void due to the foundation damage",
            "B. The buyer may rescind the contract within the inspection period",
            "C. The buyer must proceed with the purchase but can negotiate repairs",
            "D. The seller must repair the foundation before closing",
        ],
        expected_answer="B",
        explanation=(
            "Under the inspection contingency, the buyer has the right to rescind "
            "the contract within the specified inspection period if unsatisfactory "
            "conditions are discovered. The contingency gives the buyer an option, "
            "not an obligation, to cancel."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="IV. Real Estate Contracts and Agency, D. Sales contract",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-002",
        domain=Domain.LICENSING,
        subdomain="property_value_and_appraisal",
        question=(
            "Which appraisal approach is most appropriate for valuing a unique, "
            "owner-occupied commercial property with no recent comparable sales?"
        ),
        choices=[
            "A. Sales comparison approach",
            "B. Cost approach",
            "C. Income capitalization approach",
            "D. Gross rent multiplier approach",
        ],
        expected_answer="B",
        explanation=(
            "The cost approach is most appropriate when the property is unique "
            "and there are few or no comparable sales. It estimates value by "
            "calculating the cost to reproduce or replace the improvements, "
            "minus depreciation, plus land value."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="III. Property Value and Appraisal, B. Appraisal process",
        difficulty="hard",
    ),
    Instance(
        instance_id="licensing-national-003",
        domain=Domain.LICENSING,
        subdomain="real_estate_math",
        question=(
            "A property sold for $425,000. The buyer obtained an 80% LTV loan at "
            "6.5% annual interest. What is the buyer's monthly interest payment "
            "for the first month?"
        ),
        choices=[
            "A. $1,841.67",
            "B. $2,302.08",
            "C. $2,760.42",
            "D. $1,472.92",
        ],
        expected_answer="A",
        explanation=(
            "Loan amount = $425,000 x 0.80 = $340,000. "
            "Annual interest = $340,000 x 0.065 = $22,100. "
            "Monthly interest = $22,100 / 12 = $1,841.67."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="VIII. Real Estate Math Calculations",
        difficulty="medium",
    ),
]


def get_sample_instances() -> list[Instance]:
    """Return sample licensing exam instances for testing.

    Returns:
        List of sample Instance objects.
    """
    return SAMPLE_LICENSING_INSTANCES.copy()
