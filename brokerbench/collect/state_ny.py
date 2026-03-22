"""State supplement dataset for New York.

Covers New York-specific real estate laws,
regulations, disclosure requirements, and practices.
"""

from __future__ import annotations

from brokerbench.harness.constants import (
    CognitiveLevel,
    Domain,
    ExamType,
)
from brokerbench.harness.types import Instance

ALL_NY_INSTANCES: list[Instance] = [
    Instance(
        instance_id="ny-001",
        domain=Domain.LICENSING,
        subdomain="disclosure",
        question="New York's Property Condition Disclosure Act requires:",
        choices=[
            "A. A detailed inspection report from a licensed inspector",
            (
                "B. The seller to complete a disclosure form or pay a $500 credit to the buyer in "
                "lieu of disclosure"
            ),
            "C. Only verbal disclosure of known defects",
            "D. No disclosure for properties in New York City",
        ],
        expected_answer="B",
        explanation=(
            "Under NY Real Property Law Section 462, sellers must complete the "
            "Property Condition Disclosure Statement or pay a $500 credit to the "
            "buyer at closing in lieu of the disclosure."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="NY Property Condition Disclosure Act",
        difficulty="easy",
        metadata={"state": "new_york"},
    ),
    Instance(
        instance_id="ny-002",
        domain=Domain.LICENSING,
        subdomain="agency",
        question="In New York, the agency disclosure form must be presented:",
        choices=[
            "A. Only at closing",
            "B. At the first substantive contact with a buyer or seller",
            "C. After an offer is accepted",
            "D. Only when dual agency exists",
        ],
        expected_answer="B",
        explanation=(
            "New York Real Property Law Section 443 requires agents to present the "
            "agency disclosure form at the first substantive contact with a "
            "prospective buyer or seller, before any confidential information is "
            "shared."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="NY agency disclosure timing requirements",
        difficulty="easy",
        metadata={"state": "new_york"},
    ),
    Instance(
        instance_id="ny-003",
        domain=Domain.LICENSING,
        subdomain="transfer_taxes",
        question="New York's transfer tax (real property transfer tax) is paid by:",
        choices=[
            "A. The buyer in all cases",
            "B. The seller, at a rate that varies based on the sale price and property type",
            "C. Split equally between buyer and seller",
            "D. Neither party; it is waived for residential sales",
        ],
        expected_answer="B",
        explanation=(
            "In New York, the seller typically pays the real property transfer tax. "
            "The rate is $2 per $500 of consideration for residential properties. "
            "NYC has additional transfer taxes and a mansion tax for sales over $1 "
            "million."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="NY transfer tax obligations and rates",
        difficulty="medium",
        metadata={"state": "new_york"},
    ),
    Instance(
        instance_id="ny-004",
        domain=Domain.LICENSING,
        subdomain="rent_regulation",
        question="In New York City, rent-stabilized apartments:",
        choices=[
            "A. Have no restrictions on rent increases",
            "B. Are subject to annual rent increase guidelines set by the Rent Guidelines Board",
            "C. Can only be rented to government employees",
            "D. Are only found in buildings built after 2000",
        ],
        expected_answer="B",
        explanation=(
            "Rent-stabilized apartments in NYC are subject to annual rent increase "
            "limits set by the Rent Guidelines Board. The Housing Stability and "
            "Tenant Protection Act of 2019 significantly strengthened tenant "
            "protections."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="NYC rent stabilization and regulation",
        difficulty="medium",
        metadata={"state": "new_york"},
    ),
    Instance(
        instance_id="ny-005",
        domain=Domain.LICENSING,
        subdomain="licensing",
        question=(
            "New York real estate salespersons must complete a 77-hour qualifyingcourse before:"
        ),
        choices=[
            "A. Showing any properties",
            "B. Taking the state licensing examination",
            "C. Joining a local MLS",
            "D. Attending continuing education classes",
        ],
        expected_answer="B",
        explanation=(
            "New York requires completion of a 77-hour qualifying salesperson "
            "course from an approved school before a candidate is eligible to take "
            "the state licensing examination administered by the Department of "
            "State."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="NY pre-licensing education requirements",
        difficulty="easy",
        metadata={"state": "new_york"},
    ),
]


def get_all_instances() -> list[Instance]:
    """Return all New York state supplement instances.

    Returns:
        List of all Instance objects for NY state-specific questions.
    """
    return [instance.model_copy(deep=True) for instance in ALL_NY_INSTANCES]
