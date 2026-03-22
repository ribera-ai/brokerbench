"""State supplement dataset for Texas.

Covers Texas-specific real estate laws,
regulations, disclosure requirements, and practices.
"""

from __future__ import annotations

from brokerbench.harness.constants import (
    CognitiveLevel,
    Domain,
    ExamType,
)
from brokerbench.harness.types import Instance

ALL_TX_INSTANCES: list[Instance] = [
    Instance(
        instance_id="tx-001",
        domain=Domain.LICENSING,
        subdomain="contracts",
        question="In Texas, real estate contracts must use forms promulgated by:",
        choices=[
            "A. The National Association of Realtors",
            "B. The Texas Real Estate Commission (TREC)",
            "C. The Texas Association of Realtors",
            "D. The local MLS",
        ],
        expected_answer="B",
        explanation=(
            "TREC promulgates standardized contract forms that licensees are "
            "required to use in most residential transactions. Use of non-TREC "
            "forms is limited to specific exceptions (e.g., attorney-drafted "
            "contracts)."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="TX TREC promulgated contract forms",
        difficulty="easy",
        metadata={"state": "texas"},
    ),
    Instance(
        instance_id="tx-002",
        domain=Domain.LICENSING,
        subdomain="property_rights",
        question=(
            "Texas is a community property state. This means that property "
            "acquired during marriage:"
        ),
        choices=[
            "A. Belongs solely to the spouse who purchased it",
            "B. Is presumed to be owned equally by both spouses",
            "C. Must be held in a trust",
            "D. Requires court approval to sell",
        ],
        expected_answer="B",
        explanation=(
            "Texas community property law presumes that all property acquired "
            "during marriage is community property, owned equally by both spouses, "
            "unless proven to be separate property."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="TX community property law",
        difficulty="easy",
        metadata={"state": "texas"},
    ),
    Instance(
        instance_id="tx-003",
        domain=Domain.LICENSING,
        subdomain="homestead",
        question="Texas homestead protections provide:",
        choices=[
            "A. A flat $50,000 tax exemption",
            (
                "B. Broad protection from forced sale for most debts, with exceptions for purchase "
                "money liens, taxes, and home equity loans"
            ),
            "C. Complete immunity from all property taxes",
            "D. Free title insurance for primary residences",
        ],
        expected_answer="B",
        explanation=(
            "The Texas Constitution provides strong homestead protections, "
            "preventing forced sale of a homestead for most debts. Exceptions "
            "include purchase money mortgages, property taxes, home equity loans, "
            "and HOA assessments."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="TX homestead protections and exceptions",
        difficulty="medium",
        metadata={"state": "texas"},
    ),
    Instance(
        instance_id="tx-004",
        domain=Domain.LICENSING,
        subdomain="disclosure",
        question="In Texas, the Seller's Disclosure Notice is required for:",
        choices=[
            "A. All property sales without exception",
            (
                "B. Most residential sales, with "
                "exemptions for foreclosures, estate "
                "sales, and new construction by a builder"
            ),
            "C. Only properties built before 1978",
            "D. Only commercial properties",
        ],
        expected_answer="B",
        explanation=(
            "Texas Property Code Section 5.008 requires a Seller's Disclosure "
            "Notice for most residential transactions but provides specific "
            "exemptions including foreclosures, court-ordered transfers, and new "
            "construction sold by the builder."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="TX Seller's Disclosure Notice requirements",
        difficulty="easy",
        metadata={"state": "texas"},
    ),
    Instance(
        instance_id="tx-005",
        domain=Domain.LICENSING,
        subdomain="licensing",
        question=(
            "Texas real estate licensees must complete how many hours of continuing "
            "education every two years?"
        ),
        choices=[
            "A. 12 hours",
            "B. 18 hours including the TREC Legal Update courses",
            "C. 24 hours",
            "D. 30 hours",
        ],
        expected_answer="B",
        explanation=(
            "Texas licensees must complete 18 hours of CE every two-year renewal "
            "period, which must include the TREC Legal Update I and Legal Update II "
            "courses (total 8 hours) plus 10 hours of elective CE."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="TX continuing education requirements",
        difficulty="easy",
        metadata={"state": "texas"},
    ),
]


def get_all_instances() -> list[Instance]:
    """Return all Texas state supplement instances.

    Returns:
        List of all Instance objects for TX state-specific questions.
    """
    return [instance.model_copy(deep=True) for instance in ALL_TX_INSTANCES]
