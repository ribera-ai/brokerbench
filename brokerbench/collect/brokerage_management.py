"""Dataset collection for Brokerage Management domain.

Covers agent recruitment, office operations, financial management,
risk management, technology systems, training and development,
team management, and succession planning.
"""

from __future__ import annotations

from brokerbench.harness.constants import (
    CognitiveLevel,
    Domain,
    ExamType,
)
from brokerbench.harness.types import Instance

ALL_BROKERAGE_INSTANCES: list[Instance] = [
    Instance(
        instance_id="brk-001",
        domain=Domain.BROKERAGE_MANAGEMENT,
        subdomain="agent_recruitment",
        question=(
            "A managing broker is evaluating whether to hire agents as independent "
            "contractors or employees. The PRIMARY factor that distinguishes the "
            "two is:"
        ),
        choices=[
            "A. The amount of commission paid",
            "B. The degree of control the broker exercises over how work is performed",
            "C. Whether the agent has a real estate license",
            "D. The number of hours worked per week",
        ],
        expected_answer="B",
        explanation=(
            "The IRS uses a control test to distinguish independent contractors "
            "from employees. The key factor is whether the broker controls how the "
            "work is performed (employee) versus only the results (independent "
            "contractor)."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.BROKER,
        source_outline="Agent classification and employment law",
        difficulty="medium",
    ),
    Instance(
        instance_id="brk-002",
        domain=Domain.BROKERAGE_MANAGEMENT,
        subdomain="agent_recruitment",
        question=(
            "A brokerage wants to attract experienced agents from competitors. "
            "Which strategy carries the MOST legal risk?"
        ),
        choices=[
            "A. Offering a higher commission split",
            "B. Promising specific income levels based on the brokerage's past performance",
            "C. Highlighting the brokerage's training programs",
            "D. Offering a signing bonus",
        ],
        expected_answer="B",
        explanation=(
            "Promising specific income levels could constitute misrepresentation "
            "and may violate state advertising regulations. Income claims must be "
            "substantiated and clearly disclosed as not guaranteed."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="Recruitment practices and legal compliance",
        difficulty="hard",
    ),
    Instance(
        instance_id="brk-003",
        domain=Domain.BROKERAGE_MANAGEMENT,
        subdomain="office_operations",
        question=(
            "A brokerage's trust account is short $5,000 after a monthly "
            "reconciliation. The broker should FIRST:"
        ),
        choices=[
            "A. Cover the shortfall with personal funds and investigate later",
            "B. Immediately investigate the discrepancy and document findings",
            "C. Report the shortage to the state licensing authority",
            "D. Close the trust account and open a new one",
        ],
        expected_answer="B",
        explanation=(
            "The broker should immediately investigate to determine the cause of "
            "the discrepancy. Documentation is critical. Depending on the findings "
            "and state law, reporting to the licensing authority may be required."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="Trust account reconciliation and management",
        difficulty="medium",
    ),
    Instance(
        instance_id="brk-004",
        domain=Domain.BROKERAGE_MANAGEMENT,
        subdomain="office_operations",
        question=(
            "Which of the following is a required element of a brokerage's policy "
            "and procedures manual?"
        ),
        choices=[
            "A. Recipes for the office holiday party",
            "B. Procedures for handling earnest money and trust account deposits",
            "C. Personal investment advice for agents",
            "D. Social media posting schedules",
        ],
        expected_answer="B",
        explanation=(
            "A policy and procedures manual must include procedures for handling "
            "client funds, trust account management, and earnest money deposits. "
            "These are regulatory requirements that protect the public."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.BROKER,
        source_outline="Brokerage policy and procedure requirements",
        difficulty="easy",
    ),
    Instance(
        instance_id="brk-005",
        domain=Domain.BROKERAGE_MANAGEMENT,
        subdomain="financial_management",
        question=(
            "A brokerage earned $2,400,000 in gross commission income last year. "
            "Operating expenses were $1,800,000 including agent splits. The "
            "brokerage's company dollar (net revenue) is:"
        ),
        choices=[
            "A. $2,400,000",
            "B. $1,800,000",
            "C. $600,000",
            "D. $4,200,000",
        ],
        expected_answer="C",
        explanation=(
            "Company dollar = gross commission income minus agent commission splits "
            "and direct transaction costs. $2,400,000 - $1,800,000 = $600,000. This "
            "represents the revenue available to cover overhead and profit."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="Brokerage financial metrics and P&L analysis",
        difficulty="medium",
    ),
    Instance(
        instance_id="brk-006",
        domain=Domain.BROKERAGE_MANAGEMENT,
        subdomain="financial_management",
        question=(
            "A broker is considering opening a second office location. The MOST "
            "important financial metric to evaluate is:"
        ),
        choices=[
            "A. The number of agents in the market",
            "B. The projected break-even point and time to profitability",
            "C. The color scheme of the new office",
            "D. The distance from the original office",
        ],
        expected_answer="B",
        explanation=(
            "Before expanding, a broker must analyze the financial viability "
            "including projected revenue, fixed and variable costs, break-even "
            "volume, and timeline to profitability."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="Expansion planning and financial analysis",
        difficulty="hard",
    ),
    Instance(
        instance_id="brk-007",
        domain=Domain.BROKERAGE_MANAGEMENT,
        subdomain="risk_management",
        question=(
            "A brokerage receives a complaint that one of its agents showed "
            "properties only in certain neighborhoods based on the client's "
            "ethnicity. The broker should:"
        ),
        choices=[
            "A. Dismiss the complaint as the agent's personal matter",
            "B. Investigate immediately, document findings, and take corrective action",
            "C. Wait for the client to file a formal HUD complaint",
            "D. Transfer the agent to a different office",
        ],
        expected_answer="B",
        explanation=(
            "Steering complaints are serious fair housing violations. The broker "
            "has a supervisory duty to investigate promptly, document findings, "
            "take corrective action, and potentially report to the appropriate "
            "authority."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="Fair housing compliance and broker liability",
        difficulty="medium",
    ),
    Instance(
        instance_id="brk-008",
        domain=Domain.BROKERAGE_MANAGEMENT,
        subdomain="risk_management",
        question=(
            "An agent in the brokerage is involved in a transaction where they are "
            "also the buyer. This situation requires:"
        ),
        choices=[
            "A. No special handling since the agent is licensed",
            "B. Full written disclosure of the agent's interest to all parties",
            "C. The agent to use a different brokerage for the transaction",
            "D. Approval from the state real estate commission",
        ],
        expected_answer="B",
        explanation=(
            "When a licensee has a personal interest in a transaction, full written "
            "disclosure to all parties is required. Failure to disclose constitutes "
            "a violation of fiduciary duty and licensing law."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.BROKER,
        source_outline="Conflicts of interest and disclosure requirements",
        difficulty="easy",
    ),
    Instance(
        instance_id="brk-009",
        domain=Domain.BROKERAGE_MANAGEMENT,
        subdomain="technology_systems",
        question=(
            "A brokerage is implementing a new CRM system. From a compliance "
            "perspective, the MOST critical requirement is:"
        ),
        choices=[
            "A. The system must integrate with social media platforms",
            (
                "B. The system must comply with data privacy laws and protect client personal "
                "information"
            ),
            "C. The system must be the most expensive option available",
            "D. The system must have a mobile app",
        ],
        expected_answer="B",
        explanation=(
            "CRM systems store sensitive client information. The brokerage must "
            "ensure the system complies with applicable data privacy laws (state "
            "privacy acts, GLB Act) and has adequate security measures."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="Technology compliance and data security",
        difficulty="medium",
    ),
    Instance(
        instance_id="brk-010",
        domain=Domain.BROKERAGE_MANAGEMENT,
        subdomain="technology_systems",
        question=(
            "A brokerage's website displays property listings with the required IDX "
            "disclaimers. However, the site fails to update listing statuses in "
            "real time. This creates risk because:"
        ),
        choices=[
            "A. Buyers may waste time on properties that are already under contract or sold",
            "B. The website looks outdated",
            "C. Other brokerages may complain about the design",
            "D. The MLS will increase the brokerage's membership fees",
        ],
        expected_answer="A",
        explanation=(
            "Displaying stale listing data can mislead consumers and may violate "
            "MLS rules and state advertising regulations. Brokerages must ensure "
            "their IDX feeds are updated within the timeframes required by their "
            "MLS."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="IDX compliance and consumer protection",
        difficulty="medium",
    ),
    Instance(
        instance_id="brk-011",
        domain=Domain.BROKERAGE_MANAGEMENT,
        subdomain="training_development",
        question=(
            "A broker discovers that several agents are not completing their "
            "required continuing education (CE) hours. The broker should:"
        ),
        choices=[
            "A. Ignore it since CE is the agent's personal responsibility",
            (
                "B. Track CE compliance and ensure agents meet deadlines, as the broker may face "
                "liability for supervising unlicensed agents"
            ),
            "C. Pay for all agents' CE courses to ensure completion",
            "D. Report the agents to the MLS",
        ],
        expected_answer="B",
        explanation=(
            "While CE is ultimately the agent's responsibility, the supervising "
            "broker has a duty to ensure agents under their supervision maintain "
            "active licenses. Allowing agents with lapsed licenses to practice "
            "exposes the brokerage to liability."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="Continuing education tracking and compliance",
        difficulty="medium",
    ),
    Instance(
        instance_id="brk-012",
        domain=Domain.BROKERAGE_MANAGEMENT,
        subdomain="team_management",
        question=(
            "A top-producing agent wants to form a team within the brokerage. The "
            "broker should ensure:"
        ),
        choices=[
            "A. The team leader handles all compliance independently",
            (
                "B. Team advertising complies with state regulations and the brokerage name is "
                "prominently displayed"
            ),
            "C. The team operates as a separate brokerage",
            "D. Team members do not need individual licenses",
        ],
        expected_answer="B",
        explanation=(
            "Teams must operate under the brokerage umbrella. All team advertising "
            "must comply with state regulations, including prominently displaying "
            "the brokerage name. Team leaders do not replace the supervising "
            "broker's oversight responsibilities."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="Team structure and regulatory compliance",
        difficulty="medium",
    ),
    Instance(
        instance_id="brk-013",
        domain=Domain.BROKERAGE_MANAGEMENT,
        subdomain="financial_management",
        question=(
            "A brokerage offers agents three commission split options: 70/30, 80/20 "
            "with a desk fee, or 100% with a flat monthly fee. An agent closing "
            "$200,000 in annual GCI would earn the MOST under which plan?"
        ),
        choices=[
            "A. 70/30 split (no fees)",
            "B. 80/20 split with $500/month desk fee",
            "C. 100% with $2,000/month flat fee",
            "D. All plans yield the same income",
        ],
        expected_answer="C",
        explanation=(
            "70/30: $200,000 x 0.70 = $140,000. 80/20 with desk fee: ($200,000 x "
            "0.80) - ($500 x 12) = $160,000 - $6,000 = $154,000. 100% with flat "
            "fee: $200,000 - ($2,000 x 12) = $200,000 - $24,000 = $176,000. The "
            "100% commission plan with a $2,000/month flat fee yields the highest "
            "net income at $176,000."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="Commission structure analysis and comparison",
        difficulty="hard",
    ),
    Instance(
        instance_id="brk-014",
        domain=Domain.BROKERAGE_MANAGEMENT,
        subdomain="succession_planning",
        question=(
            "A broker-owner is planning to retire in 5 years. The FIRST step in "
            "succession planning should be:"
        ),
        choices=[
            "A. Immediately selling the brokerage to the highest bidder",
            "B. Getting a professional business valuation and identifying potential successors",
            "C. Firing all agents and closing the business",
            "D. Converting all agents to employees",
        ],
        expected_answer="B",
        explanation=(
            "Succession planning begins with understanding the current value of the "
            "business and identifying potential internal or external successors. A "
            "5-year timeline allows for grooming successors and maximizing business "
            "value."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="Business succession planning and valuation",
        difficulty="medium",
    ),
    Instance(
        instance_id="brk-015",
        domain=Domain.BROKERAGE_MANAGEMENT,
        subdomain="team_management",
        question=(
            "A newly licensed agent joins a brokerage and immediately wants to "
            "represent a family member in a complex commercial transaction. The "
            "managing broker should:"
        ),
        choices=[
            "A. Allow it since the agent is licensed",
            (
                "B. Assign a mentor or require co-listing with an "
                "experienced agent to ensure proper representation "
                "and risk management"
            ),
            "C. Refuse to allow the agent to do any transactions for 6 months",
            "D. Have the agent refer the client to another brokerage",
        ],
        expected_answer="B",
        explanation=(
            "While a new agent is legally licensed to practice, a managing broker "
            "has a supervisory duty. Pairing the new agent with an experienced "
            "mentor protects the client, the agent, and the brokerage from "
            "potential errors in a complex transaction."
        ),
        cognitive_level=CognitiveLevel.EXPERT,
        exam_type=ExamType.BROKER,
        source_outline="New agent supervision and mentoring",
        difficulty="hard",
    ),
]


def get_all_instances() -> list[Instance]:
    """Return all brokerage management instances.

    Returns:
        List of all Instance objects for the brokerage management domain.
    """
    return [instance.model_copy(deep=True) for instance in ALL_BROKERAGE_INSTANCES]
