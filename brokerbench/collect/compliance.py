"""Dataset collection for Compliance & Regulation domain.

Covers fair housing, agency compliance, RESPA/TILA,
environmental regulations, antitrust, license law,
and data privacy requirements.
"""

from __future__ import annotations

from brokerbench.harness.constants import (
    CognitiveLevel,
    Domain,
    ExamType,
)
from brokerbench.harness.types import Instance

ALL_COMPLIANCE_INSTANCES: list[Instance] = [
    Instance(
        instance_id="comp-001",
        domain=Domain.COMPLIANCE,
        subdomain="fair_housing",
        question=(
            "A property manager refuses to rent to a family with children, citing a "
            "building policy against minors. This violates:"
        ),
        choices=[
            "A. The Americans with Disabilities Act",
            "B. The Fair Housing Act's familial status protections",
            "C. The Equal Credit Opportunity Act",
            "D. RESPA anti-kickback provisions",
        ],
        expected_answer="B",
        explanation=(
            "The Fair Housing Act prohibits discrimination based on familial "
            "status, which includes families with children under 18. The only "
            "exemption is for qualifying senior housing (62+ or 55+ communities)."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="Federal Fair Housing Act protections",
        difficulty="easy",
    ),
    Instance(
        instance_id="comp-002",
        domain=Domain.COMPLIANCE,
        subdomain="fair_housing",
        question=(
            "A real estate agent tells a prospective buyer that a particular "
            "neighborhood is 'not a good fit' based on the racial composition of "
            "the area. This practice is known as:"
        ),
        choices=[
            "A. Redlining",
            "B. Blockbusting",
            "C. Steering",
            "D. Puffing",
        ],
        expected_answer="C",
        explanation=(
            "Steering is the practice of directing prospective buyers or renters "
            "toward or away from certain neighborhoods based on protected "
            "characteristics such as race, color, religion, or national origin."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="Prohibited discriminatory practices",
        difficulty="easy",
    ),
    Instance(
        instance_id="comp-003",
        domain=Domain.COMPLIANCE,
        subdomain="fair_housing",
        question=(
            "An apartment complex built in 1990 has no wheelchair-accessible units. "
            "Under the Fair Housing Act, the owner:"
        ),
        choices=[
            "A. Is exempt because the building was built before the ADA",
            (
                "B. May be in violation because multifamily buildings with 4+ units first "
                "occupied after March 13, 1991 must meet accessibility requirements"
            ),
            "C. Is exempt because the Fair Housing Act does not address accessibility",
            "D. Must retrofit all units immediately",
        ],
        expected_answer="B",
        explanation=(
            "The Fair Housing Act requires that multifamily buildings with 4+ units "
            "first occupied after March 13, 1991 meet specific accessibility "
            "requirements. A 1990 building would be evaluated based on its first "
            "occupancy date relative to this threshold."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="Fair Housing accessibility requirements",
        difficulty="medium",
    ),
    Instance(
        instance_id="comp-004",
        domain=Domain.COMPLIANCE,
        subdomain="agency_compliance",
        question=(
            "A broker discovers that one of their agents has been depositing "
            "earnest money checks into a personal account rather than the brokerage "
            "trust account. The broker should:"
        ),
        choices=[
            "A. Wait until the current transactions close before addressing it",
            (
                "B. Immediately investigate, move funds to the trust account, and report to the "
                "state licensing authority"
            ),
            "C. Simply remind the agent of proper procedures",
            "D. Terminate the agent and keep the situation confidential",
        ],
        expected_answer="B",
        explanation=(
            "Commingling (mixing client funds with personal funds) is a serious "
            "violation. The broker has a supervisory duty to immediately correct "
            "the situation, safeguard client funds, and report the violation to the "
            "regulatory authority."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="Trust account management and commingling",
        difficulty="medium",
    ),
    Instance(
        instance_id="comp-005",
        domain=Domain.COMPLIANCE,
        subdomain="agency_compliance",
        question=(
            "An agent representing a buyer learns that the property has foundation "
            "issues from a friend who is a contractor. The agent:"
        ),
        choices=[
            "A. Has no obligation to share information from informal sources",
            (
                "B. Must disclose all material facts they know to their client, regardless of the "
                "source"
            ),
            "C. Should only disclose if the seller's disclosure mentions it",
            "D. Should advise the buyer to hire their own inspector without mentioning the issue",
        ],
        expected_answer="B",
        explanation=(
            "An agent's fiduciary duty of disclosure requires them to share all "
            "material facts known to them that could affect the client's decision, "
            "regardless of how the information was obtained."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="Material fact disclosure obligations",
        difficulty="medium",
    ),
    Instance(
        instance_id="comp-006",
        domain=Domain.COMPLIANCE,
        subdomain="respa_tila",
        question="Under RESPA, which of the following is prohibited?",
        choices=[
            "A. A seller paying the buyer's closing costs",
            (
                "B. A referral fee paid between a real estate agent and a mortgage broker for "
                "referring business"
            ),
            "C. A buyer shopping for title insurance",
            "D. A lender charging an origination fee",
        ],
        expected_answer="B",
        explanation=(
            "RESPA Section 8 prohibits the payment of kickbacks or referral fees "
            "for the referral of settlement service business. This includes "
            "payments between real estate agents and mortgage brokers for sending "
            "clients to each other."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="RESPA anti-kickback provisions",
        difficulty="easy",
    ),
    Instance(
        instance_id="comp-007",
        domain=Domain.COMPLIANCE,
        subdomain="respa_tila",
        question=(
            "A lender provides a borrower with a Loan Estimate on Monday. The "
            "borrower's interest rate lock expires on Friday. Under TRID, the "
            "earliest the loan can close is:"
        ),
        choices=[
            "A. Tuesday",
            "B. Wednesday",
            "C. Thursday",
            "D. Friday",
        ],
        expected_answer="C",
        explanation=(
            "Under TRID, borrowers must receive the Loan Estimate at least 3 "
            "business days before closing. If delivered Monday, the 3-business-day "
            "waiting period means the earliest closing is Thursday (Tuesday, "
            "Wednesday, Thursday)."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="TRID timing requirements",
        difficulty="medium",
    ),
    Instance(
        instance_id="comp-008",
        domain=Domain.COMPLIANCE,
        subdomain="environmental",
        question=(
            "A buyer is purchasing a home built in 1972. The seller is required by federal law to:"
        ),
        choices=[
            "A. Remove all lead-based paint before closing",
            (
                "B. Provide the buyer with an EPA-approved lead hazard information pamphlet and "
                "disclose known lead-based paint hazards"
            ),
            "C. Pay for a lead inspection",
            "D. Certify the home is lead-free",
        ],
        expected_answer="B",
        explanation=(
            "Federal law requires sellers of homes built before 1978 to provide "
            "buyers with an EPA-approved lead hazard information pamphlet, disclose "
            "any known lead-based paint or hazards, and allow a 10-day inspection "
            "period."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="Lead-based paint disclosure requirements",
        difficulty="easy",
    ),
    Instance(
        instance_id="comp-009",
        domain=Domain.COMPLIANCE,
        subdomain="environmental",
        question=(
            "A commercial property buyer discovers underground storage tanks (USTs) "
            "during due diligence. Under CERCLA, the buyer can claim the innocent "
            "landowner defense ONLY if:"
        ),
        choices=[
            "A. They purchased the property at a discount",
            (
                "B. They conducted all appropriate inquiries before "
                "acquisition and had no knowledge of contamination"
            ),
            "C. The tanks were installed by a previous owner",
            "D. They notify the EPA within 60 days of discovery",
        ],
        expected_answer="B",
        explanation=(
            "The innocent landowner defense under CERCLA requires the buyer to "
            "demonstrate they conducted all appropriate inquiries (Phase I ESA) "
            "before purchase and had no reason to know of the contamination."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="CERCLA liability and defenses",
        difficulty="hard",
    ),
    Instance(
        instance_id="comp-010",
        domain=Domain.COMPLIANCE,
        subdomain="antitrust",
        question=(
            "Three competing brokerages in a market agree to charge the same "
            "commission rate. This is an example of:"
        ),
        choices=[
            "A. Market allocation",
            "B. Group boycott",
            "C. Price fixing",
            "D. Tying arrangement",
        ],
        expected_answer="C",
        explanation=(
            "Price fixing occurs when competing businesses agree to set prices at a "
            "certain level. Commission rates must be independently established by "
            "each brokerage and are always negotiable."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="Antitrust violations in real estate",
        difficulty="easy",
    ),
    Instance(
        instance_id="comp-011",
        domain=Domain.COMPLIANCE,
        subdomain="antitrust",
        question=(
            "Two brokerages agree that one will handle the north side of town and "
            "the other the south side, with neither competing in the other's "
            "territory. This practice is:"
        ),
        choices=[
            "A. Legal market segmentation",
            "B. Illegal market allocation",
            "C. A permitted referral arrangement",
            "D. Protected under the business judgment rule",
        ],
        expected_answer="B",
        explanation=(
            "Market allocation is a per se antitrust violation where competitors "
            "divide markets among themselves by geography, price range, or property "
            "type. Each brokerage must independently decide where to do business."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.BROKER,
        source_outline="Antitrust - market allocation",
        difficulty="easy",
    ),
    Instance(
        instance_id="comp-012",
        domain=Domain.COMPLIANCE,
        subdomain="license_law",
        question=(
            "A real estate salesperson's license has expired. Any commissions "
            "earned on pending transactions:"
        ),
        choices=[
            "A. Are forfeited to the state",
            "B. May still be collected if the work was done while licensed",
            "C. Must be returned to the clients",
            "D. Transfer to the supervising broker permanently",
        ],
        expected_answer="B",
        explanation=(
            "A salesperson may generally collect commissions for work performed "
            "while their license was active, even if the license has since expired. "
            "However, they cannot perform any new licensable activities."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="License status and commission entitlement",
        difficulty="medium",
    ),
    Instance(
        instance_id="comp-013",
        domain=Domain.COMPLIANCE,
        subdomain="license_law",
        question=(
            "A broker is reviewing an advertisement placed by one of their agents "
            "on social media. The ad fails to include the brokerage name. Under "
            "most state regulations, who is responsible?"
        ),
        choices=[
            "A. Only the agent who placed the ad",
            "B. Only the social media platform",
            (
                "C. The supervising broker, because they have oversight responsibility for all "
                "advertising"
            ),
            "D. No one, because social media is not regulated",
        ],
        expected_answer="C",
        explanation=(
            "The supervising broker has ultimate responsibility for ensuring all "
            "advertising by their agents complies with state regulations, including "
            "the requirement that all ads include the brokerage name."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="Broker supervision and advertising compliance",
        difficulty="medium",
    ),
    Instance(
        instance_id="comp-014",
        domain=Domain.COMPLIANCE,
        subdomain="environmental",
        question=(
            "A property owner hires a contractor to renovate a home built in 1965. "
            "Under the EPA's RRP (Renovation, Repair, and Painting) Rule, the "
            "contractor must:"
        ),
        choices=[
            "A. Only wear a dust mask during work",
            "B. Be EPA-certified and follow lead-safe work practices",
            "C. Test for lead only if children live in the home",
            "D. Notify the EPA after completing the work",
        ],
        expected_answer="B",
        explanation=(
            "The EPA's RRP Rule requires that contractors performing renovation, "
            "repair, or painting in pre-1978 housing be EPA-certified, use "
            "lead-safe work practices, and provide the homeowner with an EPA "
            "pamphlet."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="EPA RRP Rule compliance",
        difficulty="medium",
    ),
    Instance(
        instance_id="comp-015",
        domain=Domain.COMPLIANCE,
        subdomain="data_privacy",
        question=(
            "A brokerage collects personal financial information from buyers during "
            "the pre-approval process. Under the Gramm-Leach-Bliley Act, the "
            "brokerage must:"
        ),
        choices=[
            "A. Share the information freely with all parties to the transaction",
            "B. Provide a privacy notice and safeguard nonpublic personal information",
            "C. Only collect information with a court order",
            "D. Destroy all records within 30 days of closing",
        ],
        expected_answer="B",
        explanation=(
            "The Gramm-Leach-Bliley Act requires financial institutions (including "
            "real estate brokerages handling financial data) to provide privacy "
            "notices and protect consumers' nonpublic personal information."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.BROKER,
        source_outline="Data privacy and GLB Act",
        difficulty="medium",
    ),
]


def get_all_instances() -> list[Instance]:
    """Return all compliance & regulation instances.

    Returns:
        List of all Instance objects for the compliance domain.
    """
    return [instance.model_copy(deep=True) for instance in ALL_COMPLIANCE_INSTANCES]
