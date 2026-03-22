"""Dataset collection for Client Advisory domain.

Covers buyer counseling, seller counseling, investment advisory,
negotiation strategy, relocation services, estate planning referrals,
market analysis, and disclosure guidance.
"""

from __future__ import annotations

from brokerbench.harness.constants import (
    CognitiveLevel,
    Domain,
    ExamType,
)
from brokerbench.harness.types import Instance

ALL_CLIENT_ADVISORY_INSTANCES: list[Instance] = [
    Instance(
        instance_id="adv-001",
        domain=Domain.CLIENT_ADVISORY,
        subdomain="buyer_counseling",
        question=(
            "A first-time homebuyer asks their agent whether they should waive the "
            "home inspection to make their offer more competitive. The agent should "
            "advise:"
        ),
        choices=[
            "A. Always waive the inspection to win in a competitive market",
            (
                "B. Never waive inspections; explain the risks and let the buyer make an informed "
                "decision"
            ),
            "C. Only waive for new construction homes",
            "D. Waive the inspection but increase the earnest money",
        ],
        expected_answer="B",
        explanation=(
            "An agent should never pressure a client to waive inspections. The "
            "agent's duty is to inform the buyer of the risks of waiving (hidden "
            "defects, costly repairs) and let the buyer make their own informed "
            "decision."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="Buyer counseling and risk disclosure",
        difficulty="medium",
    ),
    Instance(
        instance_id="adv-002",
        domain=Domain.CLIENT_ADVISORY,
        subdomain="buyer_counseling",
        question=(
            "A buyer is pre-approved for $500,000 but finds a home they love listed "
            "at $520,000. The buyer asks the agent if they should offer over their "
            "pre-approval amount. The agent should:"
        ),
        choices=[
            "A. Encourage the offer since real estate always appreciates",
            (
                "B. Explain the financing gap risk and suggest "
                "the buyer consult their lender before making "
                "an offer above pre-approval"
            ),
            "C. Write the offer at $520,000 without discussion",
            "D. Tell the buyer they cannot make an offer above pre-approval",
        ],
        expected_answer="B",
        explanation=(
            "The agent should explain that offering above pre-approval creates a "
            "financing gap the buyer must cover with cash. The buyer should consult "
            "their lender about a potential pre-approval increase before "
            "committing."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="Financial counseling and pre-approval guidance",
        difficulty="medium",
    ),
    Instance(
        instance_id="adv-003",
        domain=Domain.CLIENT_ADVISORY,
        subdomain="seller_counseling",
        question=(
            "A seller wants to list their home $50,000 above the CMA-supported "
            "price range. The listing agent should:"
        ),
        choices=[
            "A. List at the seller's requested price without discussion",
            (
                "B. Present the CMA data, explain the risks of overpricing, and document the "
                "seller's decision if they insist"
            ),
            "C. Refuse to take the listing",
            "D. Secretly list at a lower price",
        ],
        expected_answer="B",
        explanation=(
            "The agent should present market data, explain that overpricing leads "
            "to longer days on market and potential price reductions. If the seller "
            "insists, document their decision and agree on a review timeline."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="Pricing strategy and market analysis counseling",
        difficulty="medium",
    ),
    Instance(
        instance_id="adv-004",
        domain=Domain.CLIENT_ADVISORY,
        subdomain="seller_counseling",
        question=(
            "A seller asks their agent whether they should accept an offer that "
            "includes a sale contingency from the buyer. The MOST important factors "
            "to analyze include:"
        ),
        choices=[
            "A. Only the offered price",
            (
                "B. The buyer's timeline for selling, the strength "
                "of the buyer's existing listing, and the seller's "
                "own timeline urgency"
            ),
            "C. The buyer's credit score",
            "D. Whether the buyer's agent is from a well-known brokerage",
        ],
        expected_answer="B",
        explanation=(
            "A sale contingency adds risk that the transaction may not close. The "
            "agent should evaluate the buyer's home's market position, listing "
            "status, price point, and how the seller's timeline is affected."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="Contingent offer evaluation and advising",
        difficulty="hard",
    ),
    Instance(
        instance_id="adv-005",
        domain=Domain.CLIENT_ADVISORY,
        subdomain="investment_advisory",
        question=(
            "A client asks their agent about the potential return on a rental "
            "property priced at $300,000 that generates $2,400/month in gross rent."
            "The gross rent multiplier (GRM) is:"
        ),
        choices=[
            "A. 8.0",
            "B. 10.4",
            "C. 12.5",
            "D. 125",
        ],
        expected_answer="B",
        explanation=(
            "GRM = Purchase Price / Annual Gross Rent = $300,000 / ($2,400 x 12) = "
            "$300,000 / $28,800 = 10.42 (approximately 10.4). Lower GRM generally "
            "indicates a better investment value."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="Investment property analysis and GRM calculation",
        difficulty="medium",
    ),
    Instance(
        instance_id="adv-006",
        domain=Domain.CLIENT_ADVISORY,
        subdomain="investment_advisory",
        question=(
            "A client is deciding between two investment properties. Property A has "
            "a cap rate of 8% and Property B has a cap rate of 5%. Assuming similar "
            "risk profiles, which statement is MOST accurate?"
        ),
        choices=[
            "A. Property B is always the better investment",
            "B. Property A offers a higher rate of return relative to its price",
            "C. Cap rates are irrelevant to investment decisions",
            "D. Both properties will appreciate at the same rate",
        ],
        expected_answer="B",
        explanation=(
            "Cap rate = NOI / Purchase Price. A higher cap rate indicates a higher "
            "income return relative to the purchase price. However, lower cap rates "
            "may reflect lower risk or higher appreciation potential, so context "
            "matters."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="Cap rate comparison and investment counseling",
        difficulty="hard",
    ),
    Instance(
        instance_id="adv-007",
        domain=Domain.CLIENT_ADVISORY,
        subdomain="negotiation_strategy",
        question=(
            "During negotiations, the buyer's agent receives a counteroffer that "
            "expires in 24 hours. The buyer wants to submit a counter-counteroffer."
            "The agent should advise:"
        ),
        choices=[
            "A. Ignore the deadline since it is not legally enforceable",
            (
                "B. Respond before the deadline expires, as the seller's counteroffer can be "
                "withdrawn at any time before acceptance"
            ),
            "C. Wait until the last minute to create urgency",
            "D. Verbally accept and send paperwork later",
        ],
        expected_answer="B",
        explanation=(
            "A counteroffer can be withdrawn at any time before acceptance. The "
            "agent should advise the buyer to respond promptly. Waiting risks the "
            "seller accepting another offer or withdrawing the counteroffer."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="Counteroffer timing and negotiation strategy",
        difficulty="medium",
    ),
    Instance(
        instance_id="adv-008",
        domain=Domain.CLIENT_ADVISORY,
        subdomain="negotiation_strategy",
        question=(
            "A buyer's agent is representing a client in a multiple-offer "
            "situation. The listing agent indicates there are 5 offers. The buyer's "
            "agent should:"
        ),
        choices=[
            (
                "A. Advise the buyer to submit their absolute best offer with terms that make it "
                "stand out"
            ),
            "B. Submit a lowball offer to test the seller's motivation",
            "C. Contact other buyer's agents to coordinate offer terms",
            "D. Withdraw from the negotiation to avoid competition",
        ],
        expected_answer="A",
        explanation=(
            "In a multiple-offer situation, the buyer may only get one chance. The "
            "agent should advise submitting the strongest possible offer, including "
            "competitive price, strong earnest money, flexible closing date, and "
            "minimal contingencies."
        ),
        cognitive_level=CognitiveLevel.EXPERT,
        exam_type=ExamType.BROKER,
        source_outline="Multiple-offer strategy and competitive positioning",
        difficulty="hard",
    ),
    Instance(
        instance_id="adv-009",
        domain=Domain.CLIENT_ADVISORY,
        subdomain="relocation_services",
        question=(
            "A corporate relocation client needs to purchase a home within 60 days."
            "The agent should FIRST:"
        ),
        choices=[
            "A. Start showing properties immediately",
            (
                "B. Assess the client's needs, budget, preferred "
                "areas, and any corporate relocation benefits "
                "or restrictions"
            ),
            "C. Recommend the client rent for a year first",
            "D. Refer the client to another agent who specializes in relocation",
        ],
        expected_answer="B",
        explanation=(
            "With a tight timeline, a thorough needs assessment is critical. "
            "Understanding corporate relocation benefits (buyout programs, closing "
            "cost coverage) and restrictions helps the agent efficiently target "
            "appropriate properties."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="Relocation client management and needs assessment",
        difficulty="medium",
    ),
    Instance(
        instance_id="adv-010",
        domain=Domain.CLIENT_ADVISORY,
        subdomain="relocation_services",
        question=(
            "A relocating buyer asks the agent to recommend specific schools for "
            "their children. The agent should:"
        ),
        choices=[
            "A. Provide personal opinions about the best schools",
            (
                "B. Direct the client to objective third-party school rating resources and the "
                "school district's website"
            ),
            "C. Rank the schools based on the agent's preferences",
            "D. Refuse to discuss schools entirely",
        ],
        expected_answer="B",
        explanation=(
            "Agents should avoid making subjective recommendations about schools, "
            "as this could be perceived as steering (a Fair Housing violation). "
            "Instead, direct clients to objective resources like state education "
            "department data or GreatSchools.org."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="Fair housing compliance in client advisory",
        difficulty="medium",
    ),
    Instance(
        instance_id="adv-011",
        domain=Domain.CLIENT_ADVISORY,
        subdomain="estate_planning",
        question=(
            "An elderly client wants to add their adult child to the deed of their "
            "home to avoid probate. The agent should:"
        ),
        choices=[
            "A. Prepare the deed change themselves",
            (
                "B. Advise the client to consult an estate "
                "planning attorney, as adding someone to a deed "
                "has tax and liability implications"
            ),
            "C. Refuse to discuss the matter",
            "D. Recommend the client sell the home to their child for $1",
        ],
        expected_answer="B",
        explanation=(
            "Adding someone to a deed can trigger gift tax implications, expose the "
            "property to the added person's creditors, and affect the stepped-up "
            "basis at death. The agent should refer the client to an estate "
            "planning attorney."
        ),
        cognitive_level=CognitiveLevel.EXPERT,
        exam_type=ExamType.BROKER,
        source_outline="Estate planning referrals and scope of practice",
        difficulty="hard",
    ),
    Instance(
        instance_id="adv-012",
        domain=Domain.CLIENT_ADVISORY,
        subdomain="market_analysis",
        question=(
            "A buyer asks the agent whether now is a good time to buy, given rising "
            "interest rates. The agent should:"
        ),
        choices=[
            "A. Guarantee that prices will drop soon",
            (
                "B. Present current market data, explain the relationship between rates and "
                "purchasing power, and help the buyer evaluate their personal financial situation"
            ),
            "C. Advise waiting indefinitely for rates to decrease",
            "D. Ignore the question and focus on showing homes",
        ],
        expected_answer="B",
        explanation=(
            "Agents should not predict market direction. Instead, present objective "
            "data on current market conditions, explain how rates affect monthly "
            "payments and purchasing power, and help the client make an informed "
            "decision based on their situation."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="Market analysis and financial guidance",
        difficulty="medium",
    ),
    Instance(
        instance_id="adv-013",
        domain=Domain.CLIENT_ADVISORY,
        subdomain="market_analysis",
        question=(
            "A seller's market has an average days-on-market of 5 days and 1.2 "
            "months of inventory. A listing agent should advise their seller that:"
        ),
        choices=[
            "A. They can price 20% above market value with no consequences",
            (
                "B. Market conditions strongly favor sellers, but proper preparation and pricing "
                "still matter for achieving the best outcome"
            ),
            "C. They should wait for an even stronger seller's market",
            "D. They do not need to make any repairs or stage the home",
        ],
        expected_answer="B",
        explanation=(
            "Even in a strong seller's market, proper pricing, preparation, and "
            "presentation maximize results. Overpricing can still result in a "
            "property sitting unsold. The agent should balance optimism with "
            "realistic expectations."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="Market conditions interpretation and seller advisory",
        difficulty="medium",
    ),
    Instance(
        instance_id="adv-014",
        domain=Domain.CLIENT_ADVISORY,
        subdomain="disclosure_guidance",
        question=(
            "A seller discloses to their listing agent that the basement floods "
            "during heavy rain. The agent should:"
        ),
        choices=[
            "A. Tell the seller to omit this from the disclosure form",
            (
                "B. Ensure the condition is properly disclosed on "
                "the seller's disclosure and advise the seller to "
                "consider remediation before listing"
            ),
            "C. Only disclose if a buyer specifically asks about flooding",
            "D. Reduce the listing price by 50% without explaining why",
        ],
        expected_answer="B",
        explanation=(
            "Material defects must be disclosed. The agent should ensure the seller "
            "properly discloses the flooding issue and discuss whether remediation "
            "before listing would be beneficial. Concealing known defects exposes "
            "both seller and agent to liability."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="Material fact disclosure and seller counseling",
        difficulty="medium",
    ),
    Instance(
        instance_id="adv-015",
        domain=Domain.CLIENT_ADVISORY,
        subdomain="disclosure_guidance",
        question=(
            "A buyer's agent discovers during a showing that the property may have "
            "unpermitted additions (a finished garage conversion). The agent "
            "should:"
        ),
        choices=[
            "A. Ignore it since it is the seller's responsibility to disclose",
            (
                "B. Inform the buyer of the observation, recommend "
                "verifying permits with the local building "
                "department, and factor this into the offer strategy"
            ),
            "C. Report the seller to the building department immediately",
            "D. Advise the buyer to proceed without investigation",
        ],
        expected_answer="B",
        explanation=(
            "The buyer's agent has a duty to inform their client of observations "
            "that could affect the property's value or legality. Unpermitted work "
            "can affect insurance, financing, and resale value."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="Due diligence and unpermitted construction advisory",
        difficulty="hard",
    ),
]


def get_all_instances() -> list[Instance]:
    """Return all client advisory instances.

    Returns:
        List of all Instance objects for the client advisory domain.
    """
    return [instance.model_copy(deep=True) for instance in ALL_CLIENT_ADVISORY_INSTANCES]
