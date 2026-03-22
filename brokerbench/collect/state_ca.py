"""State supplement dataset for California.

Covers California-specific real estate laws,
regulations, disclosure requirements, and practices.
"""

from __future__ import annotations

from brokerbench.harness.constants import (
    CognitiveLevel,
    Domain,
    ExamType,
)
from brokerbench.harness.types import Instance

ALL_CA_INSTANCES: list[Instance] = [
    Instance(
        instance_id="ca-001",
        domain=Domain.LICENSING,
        subdomain="disclosure",
        question=(
            "In California, the Transfer Disclosure Statement (TDS) must beprovided by the seller:"
        ),
        choices=[
            "A. Only if the buyer requests it",
            "B. For all residential properties of 1-4 units, with limited exceptions",
            "C. Only for commercial properties",
            "D. Only for new construction",
        ],
        expected_answer="B",
        explanation=(
            "California Civil Code Section 1102 requires sellers of residential "
            "property (1-4 units) to provide a TDS. Exceptions include "
            "foreclosures, court-ordered sales, and transfers between co-owners."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="CA Transfer Disclosure Statement",
        difficulty="easy",
        metadata={"state": "california"},
    ),
    Instance(
        instance_id="ca-002",
        domain=Domain.LICENSING,
        subdomain="disclosure",
        question=(
            "A California listing agent must complete which additional disclosure"
            "form that is unique to the state?"
        ),
        choices=[
            "A. Federal Lead Disclosure",
            "B. Agent Visual Inspection Disclosure (AVID)",
            "C. HUD Settlement Statement",
            "D. Uniform Residential Loan Application",
        ],
        expected_answer="B",
        explanation=(
            "California requires agents to conduct a reasonably competent and "
            "diligent visual inspection of the property and disclose findings on "
            "the AVID form, per Civil Code Section 2079."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="CA Agent Visual Inspection Disclosure",
        difficulty="easy",
        metadata={"state": "california"},
    ),
    Instance(
        instance_id="ca-003",
        domain=Domain.LICENSING,
        subdomain="natural_hazards",
        question=(
            "California's Natural Hazard Disclosure Statement (NHD) must disclose"
            "whether the property is located in:"
        ),
        choices=[
            "A. A school district boundary",
            (
                "B. Zones for flooding, fire, seismic "
                "hazards, and other state-mapped "
                "natural hazard areas"
            ),
            "C. A historic district",
            "D. A homeowners association",
        ],
        expected_answer="B",
        explanation=(
            "The NHD requires disclosure of the property's location relative to six "
            "state-mapped natural hazard zones including special flood hazard "
            "areas, dam inundation zones, very high fire hazard severity zones, "
            "wildland fire areas, earthquake fault zones, and seismic hazard zones."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="CA Natural Hazard Disclosure requirements",
        difficulty="medium",
        metadata={"state": "california"},
    ),
    Instance(
        instance_id="ca-004",
        domain=Domain.LICENSING,
        subdomain="agency",
        question="In California, dual agency:",
        choices=[
            "A. Is prohibited in all circumstances",
            "B. Is permitted only with informed written consent of both buyer and seller",
            "C. Is automatically assumed in every transaction",
            "D. Requires approval from the DRE",
        ],
        expected_answer="B",
        explanation=(
            "California Civil Code Section 2079.17 permits dual agency but requires "
            "the agent to obtain informed written consent from both parties. The "
            "agent must explain the limitations of dual representation."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="CA dual agency requirements",
        difficulty="medium",
        metadata={"state": "california"},
    ),
    Instance(
        instance_id="ca-005",
        domain=Domain.LICENSING,
        subdomain="taxation",
        question="California's Proposition 13 limits annual property tax increases to:",
        choices=[
            "A. 5% per year",
            "B. 2% per year based on the assessed value",
            "C. 10% per year",
            "D. No limit exists",
        ],
        expected_answer="B",
        explanation=(
            "Proposition 13 (1978) caps the property tax rate at 1% of assessed "
            "value and limits annual increases in assessed value to no more than "
            "2%, unless there is a change in ownership or new construction."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.BROKER,
        source_outline="CA Proposition 13 property tax limitations",
        difficulty="medium",
        metadata={"state": "california"},
    ),
]


def get_all_instances() -> list[Instance]:
    """Return all California state supplement instances.

    Returns:
        List of all Instance objects for CA state-specific questions.
    """
    return [instance.model_copy(deep=True) for instance in ALL_CA_INSTANCES]
