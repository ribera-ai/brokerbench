"""Dataset collection for Underwriting & Finance domain.

Covers loan qualification, loan types, risk assessment,
compliance flags, income analysis, and property analysis
for residential mortgage underwriting.
"""

from __future__ import annotations

from brokerbench.harness.constants import (
    CognitiveLevel,
    Domain,
    ExamType,
)
from brokerbench.harness.types import Instance

ALL_UNDERWRITING_INSTANCES: list[Instance] = [
    Instance(
        instance_id="uw-001",
        domain=Domain.UNDERWRITING,
        subdomain="loan_qualification",
        question=(
            "A borrower has a gross monthly income of $8,000, a monthly mortgage"
            "payment (PITI) of $2,000, and total monthly debt payments of $3,200."
            "What is the borrower's back-end DTI ratio?"
        ),
        choices=[
            "A. 25%",
            "B. 32%",
            "C. 40%",
            "D. 48%",
        ],
        expected_answer="C",
        explanation=(
            "Back-end DTI = total monthly debt / gross monthly income = $3,200 / "
            "$8,000 = 0.40 or 40%. This includes all recurring debts plus the "
            "proposed housing payment."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="Debt-to-income ratio calculations",
        difficulty="medium",
    ),
    Instance(
        instance_id="uw-002",
        domain=Domain.UNDERWRITING,
        subdomain="loan_qualification",
        question=(
            "A conventional loan applicant has a credit score of 680 and is putting"
            "10% down. The lender will most likely require:"
        ),
        choices=[
            "A. No additional conditions",
            "B. Private mortgage insurance (PMI)",
            "C. A co-signer",
            "D. A larger earnest money deposit",
        ],
        expected_answer="B",
        explanation=(
            "PMI is typically required on conventional loans when the borrower's "
            "down payment is less than 20% of the purchase price (LTV > 80%). The "
            "680 credit score is acceptable for conventional financing."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="PMI requirements and LTV thresholds",
        difficulty="easy",
    ),
    Instance(
        instance_id="uw-003",
        domain=Domain.UNDERWRITING,
        subdomain="loan_types",
        question=(
            "Which loan type is specifically designed for rural properties and does"
            "not require a down payment?"
        ),
        choices=[
            "A. FHA",
            "B. VA",
            "C. USDA",
            "D. Conventional",
        ],
        expected_answer="C",
        explanation=(
            "USDA loans (Rural Development Guaranteed Housing Loans) offer 100% "
            "financing for eligible properties in designated rural areas. Borrowers "
            "must meet income limits and the property must be in an eligible "
            "location."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="Government-backed loan programs",
        difficulty="easy",
    ),
    Instance(
        instance_id="uw-004",
        domain=Domain.UNDERWRITING,
        subdomain="loan_types",
        question=(
            "A veteran with full VA entitlement is purchasing a $400,000 home. The"
            "VA funding fee is 2.15% for first-time use. What is the funding fee"
            "amount?"
        ),
        choices=[
            "A. $4,300",
            "B. $6,450",
            "C. $8,600",
            "D. $12,000",
        ],
        expected_answer="C",
        explanation=(
            "$400,000 x 0.0215 = $8,600. The VA funding fee can be financed into "
            "the loan or paid at closing. Disabled veterans may be exempt from the "
            "funding fee."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="VA loan funding fee calculations",
        difficulty="medium",
    ),
    Instance(
        instance_id="uw-005",
        domain=Domain.UNDERWRITING,
        subdomain="risk_assessment",
        question=(
            "A borrower has stable employment but their credit report shows three"
            "late mortgage payments in the past 12 months. An underwriter would"
            "most likely:"
        ),
        choices=[
            "A. Approve the loan with no conditions",
            "B. Deny the loan or require a satisfactory explanation with compensating factors",
            "C. Ignore the late payments since the borrower is employed",
            "D. Automatically approve with a higher interest rate",
        ],
        expected_answer="B",
        explanation=(
            "Recent mortgage delinquencies are a significant risk factor. The "
            "underwriter will likely require a written explanation (letter of "
            "explanation) and look for compensating factors such as substantial "
            "reserves or a lower LTV."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="Credit risk evaluation and compensating factors",
        difficulty="medium",
    ),
    Instance(
        instance_id="uw-006",
        domain=Domain.UNDERWRITING,
        subdomain="risk_assessment",
        question=(
            "An appraiser notes that comparable sales used in the appraisal are"
            "more than 12 months old and located in a different school district."
            "The underwriter should:"
        ),
        choices=[
            "A. Accept the appraisal as-is since it was done by a licensed appraiser",
            (
                "B. Request additional or more recent comparable sales that better reflect the "
                "subject property's market"
            ),
            "C. Automatically reduce the appraised value by 10%",
            "D. Order a desktop appraisal to replace the field appraisal",
        ],
        expected_answer="B",
        explanation=(
            "Stale or geographically dissimilar comparables weaken the reliability "
            "of the appraisal. The underwriter should request comps that are more "
            "recent (ideally within 6 months) and from the subject's competitive "
            "market area."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="Appraisal review and comparable analysis",
        difficulty="hard",
    ),
    Instance(
        instance_id="uw-007",
        domain=Domain.UNDERWRITING,
        subdomain="compliance_flags",
        question=(
            "A loan file shows that the borrower's employer verification was"
            "completed 120 days before the closing date. Under most agency"
            "guidelines, this verification:"
        ),
        choices=[
            "A. Is still valid and acceptable",
            "B. Must be re-verified because it exceeds the typical 120-day age limit",
            "C. Only needs to be updated if the borrower changed jobs",
            "D. Can be extended with a verbal verification of employment",
        ],
        expected_answer="D",
        explanation=(
            "Most agency guidelines require employment verification to be no older "
            "than 120 days at closing. A verbal verification of employment (VVOE) "
            "within 10 business days of closing can update the original "
            "verification."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="Document age and re-verification requirements",
        difficulty="medium",
    ),
    Instance(
        instance_id="uw-008",
        domain=Domain.UNDERWRITING,
        subdomain="compliance_flags",
        question=(
            "A borrower is using a gift from a family member for the entire 3.5%"
            "FHA down payment. Which of the following is required?"
        ),
        choices=[
            "A. The gift funds must be repaid within 5 years",
            "B. A gift letter stating no repayment is required and documentation of the transfer",
            "C. The gift donor must be added to the mortgage",
            "D. Gift funds cannot be used for FHA down payments",
        ],
        expected_answer="B",
        explanation=(
            "FHA allows 100% of the down payment to come from an eligible gift "
            "donor (family member, employer, etc.). A signed gift letter confirming "
            "no repayment expectation and a paper trail of the funds transfer are "
            "required."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="FHA gift fund requirements",
        difficulty="easy",
    ),
    Instance(
        instance_id="uw-009",
        domain=Domain.UNDERWRITING,
        subdomain="income_analysis",
        question=(
            "A self-employed borrower shows $120,000 in gross income on their tax"
            "returns but has $45,000 in business deductions including $12,000 in"
            "depreciation. For qualifying purposes, the lender will use an income"
            "of approximately:"
        ),
        choices=[
            "A. $120,000",
            "B. $75,000",
            "C. $87,000",
            "D. $45,000",
        ],
        expected_answer="C",
        explanation=(
            "Lenders start with gross income ($120,000), subtract business "
            "deductions ($45,000), then add back non-cash deductions like "
            "depreciation ($12,000): $120,000 - $45,000 + $12,000 = $87,000. "
            "Depreciation is added back because it is a non-cash expense."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="Self-employed borrower income calculation",
        difficulty="hard",
    ),
    Instance(
        instance_id="uw-010",
        domain=Domain.UNDERWRITING,
        subdomain="income_analysis",
        question=(
            "A borrower receives $2,000/month in child support. To use this income"
            "for qualification, the underwriter must verify:"
        ),
        choices=[
            "A. That the payments have been received for at least 3 months",
            (
                "B. That the payments have been received consistently for 6+ months and will "
                "continue for at least 3 more years"
            ),
            "C. Only that a court order exists",
            "D. That the ex-spouse has good credit",
        ],
        expected_answer="B",
        explanation=(
            "To count child support as qualifying income, the underwriter must "
            "document consistent receipt (typically 6-12 months of bank statements "
            "or cancelled checks) and verify the payments will continue for at "
            "least 3 years from closing."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="Non-employment income verification",
        difficulty="medium",
    ),
    Instance(
        instance_id="uw-011",
        domain=Domain.UNDERWRITING,
        subdomain="property_analysis",
        question=(
            "An appraisal reveals that the subject property's roof has less than 2"
            "years of remaining useful life. For an FHA loan, the underwriter will:"
        ),
        choices=[
            "A. Accept the property as-is",
            (
                "B. Require the roof to be repaired or replaced "
                "before closing as an FHA health and safety requirement"
            ),
            "C. Reduce the loan amount by the estimated repair cost",
            "D. Require the buyer to escrow funds for future repair",
        ],
        expected_answer="B",
        explanation=(
            "FHA minimum property requirements (MPRs) require that the roof have at "
            "least 2 years of remaining useful life. If it does not, the roof must "
            "be repaired or replaced prior to closing."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="FHA minimum property requirements",
        difficulty="medium",
    ),
    Instance(
        instance_id="uw-012",
        domain=Domain.UNDERWRITING,
        subdomain="property_analysis",
        question=(
            "A subject property is located in a FEMA-designated Special Flood"
            "Hazard Area (Zone AE). The lender is required to:"
        ),
        choices=[
            "A. Deny the loan application",
            "B. Require the borrower to obtain flood insurance as a condition of the loan",
            "C. Simply disclose the flood zone to the borrower",
            "D. Increase the interest rate by 0.5%",
        ],
        expected_answer="B",
        explanation=(
            "The National Flood Insurance Act requires lenders to mandate flood "
            "insurance for properties in Special Flood Hazard Areas (Zones A and V) "
            "as a condition of making the loan."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="Flood zone requirements and insurance",
        difficulty="easy",
    ),
    Instance(
        instance_id="uw-013",
        domain=Domain.UNDERWRITING,
        subdomain="loan_qualification",
        question=(
            "A borrower is applying for a Qualified Mortgage (QM). Their total DTI"
            "ratio is 44%. Under the QM rule:"
        ),
        choices=[
            "A. The loan automatically qualifies since the DTI is below 50%",
            (
                "B. The loan may qualify under the General QM definition if the lender documents "
                "compensating factors"
            ),
            "C. The loan cannot be a QM because DTI must be below 36%",
            "D. DTI is not considered in QM determination",
        ],
        expected_answer="B",
        explanation=(
            "Under the revised General QM rule, there is no hard DTI cap. Instead, "
            "lenders must verify the borrower's ability to repay using residual "
            "income or compensating factors. A 44% DTI may be acceptable with "
            "strong compensating factors."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="Qualified Mortgage rules and DTI",
        difficulty="hard",
    ),
    Instance(
        instance_id="uw-014",
        domain=Domain.UNDERWRITING,
        subdomain="compliance_flags",
        question=(
            "TRID requires lenders to provide the Closing Disclosure to the"
            "borrower at least how many business days before closing?"
        ),
        choices=[
            "A. 1 business day",
            "B. 3 business days",
            "C. 5 business days",
            "D. 7 business days",
        ],
        expected_answer="B",
        explanation=(
            "TRID (TILA-RESPA Integrated Disclosures) requires the Closing "
            "Disclosure to be received by the borrower at least 3 business days "
            "before consummation (closing)."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="TRID disclosure timing requirements",
        difficulty="easy",
    ),
    Instance(
        instance_id="uw-015",
        domain=Domain.UNDERWRITING,
        subdomain="risk_assessment",
        question=(
            "A borrower is purchasing an investment property with 25% down."
            "Compared to a primary residence purchase, the underwriter should"
            "expect:"
        ),
        choices=[
            "A. Identical underwriting standards",
            (
                "B. Stricter requirements including higher credit scores, larger reserves, and "
                "higher interest rates"
            ),
            "C. Looser requirements since the borrower already owns a home",
            "D. The same DTI limits but a lower appraisal standard",
        ],
        expected_answer="B",
        explanation=(
            "Investment property loans carry higher risk due to the borrower's "
            "reduced incentive to avoid default. Lenders typically require higher "
            "credit scores (often 680-720+), 6+ months of reserves, and charge "
            "higher interest rates."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="Investment property underwriting standards",
        difficulty="hard",
    ),
]


def get_all_instances() -> list[Instance]:
    """Return all underwriting & finance instances.

    Returns:
        List of all Instance objects for the underwriting domain.
    """
    return [instance.model_copy(deep=True) for instance in ALL_UNDERWRITING_INSTANCES]
