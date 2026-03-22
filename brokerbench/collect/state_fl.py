"""State supplement dataset for Florida.

Covers Florida-specific real estate laws,
regulations, disclosure requirements, and practices.
"""

from __future__ import annotations

from brokerbench.harness.constants import (
    CognitiveLevel,
    Domain,
    ExamType,
)
from brokerbench.harness.types import Instance

ALL_FL_INSTANCES: list[Instance] = [
    Instance(
        instance_id="fl-001",
        domain=Domain.LICENSING,
        subdomain="disclosure",
        question="Florida requires sellers to disclose:",
        choices=[
            "A. All property defects, whether known or unknown",
            "B. Known material defects that are not readily observable by the buyer",
            "C. Only defects listed on the state disclosure form",
            "D. Nothing, as Florida is a caveat emptor state with no disclosure requirements",
        ],
        expected_answer="B",
        explanation=(
            "Under Johnson v. Davis (1985), Florida sellers must disclose known "
            "material defects that are not readily observable. Florida does not "
            "require a standardized disclosure form but the duty to disclose exists "
            "under case law."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="FL seller disclosure requirements (Johnson v. Davis)",
        difficulty="medium",
        metadata={"state": "florida"},
    ),
    Instance(
        instance_id="fl-002",
        domain=Domain.LICENSING,
        subdomain="agency",
        question="In Florida, transaction brokers:",
        choices=[
            "A. Represent neither party but facilitate the transaction",
            "B. Owe full fiduciary duties to both parties",
            "C. Can only represent sellers",
            "D. Must disclose their commission to the public",
        ],
        expected_answer="A",
        explanation=(
            "Florida Statute 475.278 establishes transaction broker as the default "
            "relationship. Transaction brokers provide limited representation, "
            "facilitating the transaction without full advocacy for either party."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="FL transaction broker relationship",
        difficulty="easy",
        metadata={"state": "florida"},
    ),
    Instance(
        instance_id="fl-003",
        domain=Domain.LICENSING,
        subdomain="insurance",
        question="Florida's Citizens Property Insurance Corporation:",
        choices=[
            "A. Is the only insurer allowed to sell homeowner's insurance",
            (
                "B. Is the state's insurer of last resort for property owners unable to obtain "
                "private coverage"
            ),
            "C. Provides free hurricane insurance to all homeowners",
            "D. Only covers commercial properties",
        ],
        expected_answer="B",
        explanation=(
            "Citizens is Florida's state-created, not-for-profit insurer of last "
            "resort. It provides property insurance to those unable to find "
            "coverage in the private market, common in high-risk hurricane zones."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="FL Citizens Insurance and wind coverage",
        difficulty="medium",
        metadata={"state": "florida"},
    ),
    Instance(
        instance_id="fl-004",
        domain=Domain.LICENSING,
        subdomain="closing",
        question="In Florida, real estate closings are typically handled by:",
        choices=[
            "A. Real estate agents",
            "B. Title companies or attorneys, as Florida is a title theory state",
            "C. The county clerk's office",
            "D. The buyer's mortgage lender exclusively",
        ],
        expected_answer="B",
        explanation=(
            "Florida closings are typically conducted by title companies or real "
            "estate attorneys. Florida follows title theory for mortgages, and the "
            "closing agent ensures proper transfer of title and disbursement of "
            "funds."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="FL closing practices and title theory",
        difficulty="easy",
        metadata={"state": "florida"},
    ),
    Instance(
        instance_id="fl-005",
        domain=Domain.LICENSING,
        subdomain="taxation",
        question="Florida has no state income tax but funds government services primarily through:",
        choices=[
            "A. Corporate income taxes only",
            "B. Sales tax, property taxes, and documentary stamp taxes",
            "C. Special assessments on all properties",
            "D. Federal subsidies exclusively",
        ],
        expected_answer="B",
        explanation=(
            "Florida's no-income-tax structure is funded by a combination of sales "
            "tax (6% state + county surcharges), property taxes, documentary stamp "
            "taxes on deeds and mortgages, and intangible taxes."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.BROKER,
        source_outline="FL tax structure and real estate implications",
        difficulty="medium",
        metadata={"state": "florida"},
    ),
]


def get_all_instances() -> list[Instance]:
    """Return all Florida state supplement instances.

    Returns:
        List of all Instance objects for FL state-specific questions.
    """
    return [
        instance.model_copy(deep=True)
        for instance in ALL_FL_INSTANCES
    ]
