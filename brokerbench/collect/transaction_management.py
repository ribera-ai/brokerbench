"""Dataset collection for Transaction Management domain.

Covers the end-to-end real estate transaction lifecycle:
offer negotiation, escrow, contingency management, closing
procedures, document management, and post-closing tasks.
"""

from __future__ import annotations

from brokerbench.harness.constants import (
    CognitiveLevel,
    Domain,
    ExamType,
)
from brokerbench.harness.types import Instance

ALL_TRANSACTION_INSTANCES: list[Instance] = [
    Instance(
        instance_id="txn-001",
        domain=Domain.TRANSACTION_MANAGEMENT,
        subdomain="offer_and_negotiation",
        question=(
            "A buyer submits an offer with a 72-hour acceptance deadline. The"
            "seller's agent receives the offer on Monday at 2 PM. By what day and"
            "time must the seller respond to keep the offer alive?"
        ),
        choices=[
            "A. Tuesday at 2 PM",
            "B. Wednesday at 2 PM",
            "C. Thursday at 2 PM",
            "D. Friday at 2 PM",
        ],
        expected_answer="C",
        explanation=(
            "A 72-hour acceptance deadline runs from the time of receipt. Monday 2 "
            "PM + 72 hours = Thursday 2 PM."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="Transaction timeline management",
        difficulty="medium",
    ),
    Instance(
        instance_id="txn-002",
        domain=Domain.TRANSACTION_MANAGEMENT,
        subdomain="offer_and_negotiation",
        question="During a multiple-offer situation, the listing agent should:",
        choices=[
            "A. Disclose the terms of competing offers to all buyers",
            "B. Present all offers to the seller without disclosing competing terms",
            "C. Only present the highest offer to the seller",
            "D. Advise the seller to reject all offers and relist at a higher price",
        ],
        expected_answer="B",
        explanation=(
            "The listing agent must present all offers to the seller. Disclosing "
            "the terms of one offer to competing buyers violates fiduciary duty. "
            "The agent must not suppress or selectively present offers."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="Offer presentation and multiple-offer handling",
        difficulty="medium",
    ),
    Instance(
        instance_id="txn-003",
        domain=Domain.TRANSACTION_MANAGEMENT,
        subdomain="escrow_and_closing",
        question="Earnest money must typically be deposited into an escrow account within:",
        choices=[
            "A. 24 hours of offer acceptance",
            "B. The timeframe specified in the purchase agreement",
            "C. 10 business days of offer submission",
            "D. 30 days of the listing date",
        ],
        expected_answer="B",
        explanation=(
            "The deposit timeline for earnest money is governed by the terms of the "
            "purchase agreement. While some states have statutory default periods, "
            "the contract terms control."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="Escrow procedures and earnest money",
        difficulty="easy",
    ),
    Instance(
        instance_id="txn-004",
        domain=Domain.TRANSACTION_MANAGEMENT,
        subdomain="escrow_and_closing",
        question=(
            "At closing, which document transfers ownership of real property from"
            "the seller to the buyer?"
        ),
        choices=[
            "A. The mortgage note",
            "B. The deed",
            "C. The title insurance policy",
            "D. The settlement statement",
        ],
        expected_answer="B",
        explanation=(
            "The deed is the legal instrument that transfers ownership (title) from "
            "the grantor (seller) to the grantee (buyer). It must be delivered and "
            "accepted to be effective."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="Closing documents and procedures",
        difficulty="easy",
    ),
    Instance(
        instance_id="txn-005",
        domain=Domain.TRANSACTION_MANAGEMENT,
        subdomain="contingency_management",
        question=(
            "A buyer's financing contingency expires in 21 days but their lender"
            "needs 30 days. The buyer's agent should:"
        ),
        choices=[
            "A. Let the contingency expire and hope for the best",
            "B. Request a contingency extension from the seller before expiration",
            "C. Cancel the contract immediately",
            "D. Proceed to closing without financing",
        ],
        expected_answer="B",
        explanation=(
            "The agent should proactively request a written extension of the "
            "financing contingency before it expires. Allowing it to lapse puts the "
            "buyer's earnest money at risk."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="Contingency tracking and deadlines",
        difficulty="medium",
    ),
    Instance(
        instance_id="txn-006",
        domain=Domain.TRANSACTION_MANAGEMENT,
        subdomain="contingency_management",
        question=(
            "An appraisal comes in at $380,000 on a property under contract for"
            "$400,000. The appraisal contingency is still in effect. The buyer may:"
        ),
        choices=[
            "A. Only cancel the contract entirely",
            "B. Negotiate a price reduction, make up the difference in cash, or cancel",
            "C. Force the seller to reduce the price to $380,000",
            "D. Demand a second appraisal at the seller's expense",
        ],
        expected_answer="B",
        explanation=(
            "With an active appraisal contingency, the buyer has several options: "
            "negotiate a lower price, pay the difference out of pocket, combine "
            "both approaches, or exercise the contingency to cancel."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="Appraisal contingency resolution",
        difficulty="hard",
    ),
    Instance(
        instance_id="txn-007",
        domain=Domain.TRANSACTION_MANAGEMENT,
        subdomain="timeline_coordination",
        question=(
            "A transaction coordinator discovers that the buyer's home inspection,"
            "appraisal, and loan approval are all scheduled for the same week, two"
            "weeks before closing. What is the PRIMARY risk?"
        ),
        choices=[
            "A. The seller may back out of the deal",
            (
                "B. If any item reveals issues, there is insufficient time for resolution before "
                "closing"
            ),
            "C. The buyer will have to pay for all services at once",
            "D. The title company cannot process multiple items simultaneously",
        ],
        expected_answer="B",
        explanation=(
            "Stacking critical milestones leaves no buffer time. If the inspection "
            "reveals defects or the appraisal comes in low, there may not be enough "
            "time to negotiate repairs, request extensions, or resolve issues "
            "before closing."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="Transaction timeline risk management",
        difficulty="hard",
    ),
    Instance(
        instance_id="txn-008",
        domain=Domain.TRANSACTION_MANAGEMENT,
        subdomain="document_management",
        question=(
            "Which of the following is NOT typically required at a residential real"
            "estate closing?"
        ),
        choices=[
            "A. Deed of trust or mortgage",
            "B. Settlement statement (Closing Disclosure)",
            "C. A Phase II environmental assessment",
            "D. Title insurance commitment or policy",
        ],
        expected_answer="C",
        explanation=(
            "A Phase II environmental assessment is not a standard requirement for "
            "residential closings. It is typically required only when a Phase I "
            "assessment identifies recognized environmental conditions, usually in "
            "commercial transactions."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="Closing document requirements",
        difficulty="easy",
    ),
    Instance(
        instance_id="txn-009",
        domain=Domain.TRANSACTION_MANAGEMENT,
        subdomain="post_closing",
        question="After closing, the deed must be:",
        choices=[
            "A. Kept in the buyer's safe deposit box to be valid",
            "B. Recorded with the appropriate government office to provide constructive notice",
            "C. Returned to the seller within 30 days",
            "D. Filed with the IRS for tax purposes",
        ],
        expected_answer="B",
        explanation=(
            "Recording the deed with the county recorder's office provides "
            "constructive notice to the world of the new ownership. While recording "
            "is not required for the deed to be valid between the parties, it "
            "protects against subsequent claims."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="Post-closing procedures and recording",
        difficulty="easy",
    ),
    Instance(
        instance_id="txn-010",
        domain=Domain.TRANSACTION_MANAGEMENT,
        subdomain="post_closing",
        question=(
            "A buyer discovers a roof leak three weeks after closing that was not"
            "disclosed by the seller. The buyer's agent had no knowledge of the"
            "leak. Which statement is MOST accurate?"
        ),
        choices=[
            "A. The buyer has no recourse because they accepted the property at closing",
            (
                "B. The buyer may have a claim against the seller for fraudulent nondisclosure if "
                "the seller knew"
            ),
            "C. The buyer's agent is automatically liable for the undisclosed defect",
            "D. The title insurance policy will cover the repair",
        ],
        expected_answer="B",
        explanation=(
            "If the seller had actual knowledge of the roof leak and failed to "
            "disclose it, the buyer may have a claim for fraudulent nondisclosure "
            "or misrepresentation. The buyer's agent is not liable if they had no "
            "knowledge. Title insurance does not cover physical defects."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="Post-closing disputes and remedies",
        difficulty="hard",
    ),
    Instance(
        instance_id="txn-011",
        domain=Domain.TRANSACTION_MANAGEMENT,
        subdomain="offer_and_negotiation",
        question=(
            "A seller accepts an offer but fails to initial a counter-offer"
            "addendum changing the closing date. Is there a binding contract?"
        ),
        choices=[
            "A. Yes, because the seller verbally agreed",
            "B. No, because the addendum was not properly executed",
            "C. Yes, because the original offer was accepted",
            "D. It depends on whether the buyer noticed the missing initials",
        ],
        expected_answer="B",
        explanation=(
            "Under the Statute of Frauds, real estate contracts must be in writing "
            "and signed by the parties to be enforceable. An uninitialed addendum "
            "has not been properly executed, so the modified terms are not binding."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="Contract execution and validity",
        difficulty="hard",
    ),
    Instance(
        instance_id="txn-012",
        domain=Domain.TRANSACTION_MANAGEMENT,
        subdomain="escrow_and_closing",
        question="Prorations at closing ensure that:",
        choices=[
            (
                "A. The buyer and seller each pay their fair share of expenses for their period of "
                "ownership"
            ),
            "B. The buyer pays all expenses from the listing date forward",
            "C. The seller pays all expenses through the end of the calendar year",
            "D. Neither party is responsible for expenses during the escrow period",
        ],
        expected_answer="A",
        explanation=(
            "Prorations divide ongoing expenses (property taxes, HOA dues, "
            "utilities) between buyer and seller based on their respective periods "
            "of ownership, typically using the closing date as the dividing point."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="Proration and settlement calculations",
        difficulty="easy",
    ),
    Instance(
        instance_id="txn-013",
        domain=Domain.TRANSACTION_MANAGEMENT,
        subdomain="contingency_management",
        question=(
            "A home inspection reveals knob-and-tube wiring throughout a 1920s"
            "home. The buyer requests the seller replace all wiring. The seller"
            "refuses. Under a typical inspection contingency, what are the buyer's"
            "options?"
        ),
        choices=[
            "A. Sue the seller for specific performance to force the repair",
            "B. Accept the property as-is, negotiate a credit, or cancel under the contingency",
            "C. Report the seller to the real estate commission",
            "D. Demand the listing agent pay for the repairs",
        ],
        expected_answer="B",
        explanation=(
            "Under a standard inspection contingency, the buyer can accept the "
            "property as-is, negotiate repairs or credits, or cancel the contract "
            "and receive their earnest money back. The seller is not obligated to "
            "make repairs."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="Inspection contingency negotiation",
        difficulty="medium",
    ),
    Instance(
        instance_id="txn-014",
        domain=Domain.TRANSACTION_MANAGEMENT,
        subdomain="timeline_coordination",
        question=(
            "A loan officer informs the buyer's agent that the clear-to-close has"
            "been issued, but the closing disclosure has not yet been delivered to"
            "the buyer. Closing is scheduled for tomorrow. Can the transaction"
            "close on time?"
        ),
        choices=[
            "A. Yes, the closing disclosure can be signed at closing",
            (
                "B. No, TRID requires a 3-business-day waiting "
                "period after delivery of the closing disclosure"
            ),
            "C. Yes, if the buyer waives their right to review",
            "D. No, a 7-day waiting period is required",
        ],
        expected_answer="B",
        explanation=(
            "Under TRID (TILA-RESPA Integrated Disclosures), the borrower must "
            "receive the Closing Disclosure at least 3 business days before "
            "closing. This waiting period cannot be waived in most circumstances."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="TRID compliance and closing timelines",
        difficulty="medium",
    ),
    Instance(
        instance_id="txn-015",
        domain=Domain.TRANSACTION_MANAGEMENT,
        subdomain="document_management",
        question=(
            "A broker reviewing a purchase agreement notices the legal description"
            "does not match the property address. The broker should:"
        ),
        choices=[
            "A. Proceed with the transaction since the address is sufficient",
            "B. Halt the process and have the legal description corrected before proceeding",
            "C. Note it as a minor issue to fix after closing",
            "D. Assume the title company will catch and fix the error",
        ],
        expected_answer="B",
        explanation=(
            "A mismatched legal description is a material defect in the contract. "
            "The broker should ensure it is corrected immediately, as an incorrect "
            "legal description could void the transaction or create title issues."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="Contract review and quality assurance",
        difficulty="medium",
    ),
]


def get_all_instances() -> list[Instance]:
    """Return all transaction management instances.

    Returns:
        List of all Instance objects for the transaction management domain.
    """
    return [
        instance.model_copy(deep=True)
        for instance in ALL_TRANSACTION_INSTANCES
    ]
