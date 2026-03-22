"""Dataset collection for Licensing Exam domain.

Generates original exam-style questions from Pearson VUE / PSI
national real estate licensing exam content outlines.

Covers all 8 topic areas at all 3 cognitive levels (Knowledge,
Application, Analysis) for both Salesperson and Broker exam types.
"""

from __future__ import annotations

from brokerbench.harness.constants import CognitiveLevel, Domain, ExamType
from brokerbench.harness.types import Instance

# ---------------------------------------------------------------------------
# Topic I: Real Property Characteristics, Legal Descriptions & Property Use
# ---------------------------------------------------------------------------
_TOPIC_I: list[Instance] = [
    Instance(
        instance_id="licensing-national-001",
        domain=Domain.LICENSING,
        subdomain="real_property_characteristics",
        question="Which of the following is considered real property?",
        choices=[
            "A. A refrigerator in a rental unit",
            "B. A built-in dishwasher permanently installed in the kitchen",
            "C. A window air conditioning unit",
            "D. A portable storage shed sitting on blocks",
        ],
        expected_answer="B",
        explanation=(
            "A built-in dishwasher that is permanently installed becomes a fixture "
            "and is considered real property. The key tests are method of "
            "attachment, adaptation to the property, and intent of the parties."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="I. Real Property Characteristics, A. Fixtures and personal property",
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-002",
        domain=Domain.LICENSING,
        subdomain="real_property_characteristics",
        question="A metes and bounds legal description begins at which point?",
        choices=[
            "A. The geographic center of the parcel",
            "B. The point of beginning (POB)",
            "C. The nearest government survey monument",
            "D. The street address of the property",
        ],
        expected_answer="B",
        explanation=(
            "A metes and bounds description always starts and returns to the point "
            "of beginning (POB). Metes are measurements of distance and bounds are "
            "directions."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="I. Real Property Characteristics, B. Legal descriptions",
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-003",
        domain=Domain.LICENSING,
        subdomain="real_property_characteristics",
        question="Riparian rights apply to properties that:",
        choices=[
            "A. Are adjacent to navigable oceans",
            "B. Border flowing water such as rivers and streams",
            "C. Contain underground aquifers",
            "D. Are located in flood zones",
        ],
        expected_answer="B",
        explanation=(
            "Riparian rights belong to owners of land that borders flowing water "
            "such as rivers, streams, and creeks. Littoral rights apply to "
            "properties bordering standing bodies of water like lakes and oceans."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="I. Real Property Characteristics, C. Property use and rights",
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-004",
        domain=Domain.LICENSING,
        subdomain="real_property_characteristics",
        question=(
            "A homeowner installs a custom built-in bookshelf unit in their living "
            "room, anchored to the wall studs. When they sell the property, the "
            "buyer expects the bookshelf to remain. The seller wants to take it. "
            "Under standard fixture analysis, who prevails?"
        ),
        choices=[
            "A. The seller, because personal property always remains with the owner",
            "B. The buyer, because the bookshelf is likely a fixture",
            "C. Neither party, because this must be decided in court",
            "D. The seller, because built-in items are always personal property",
        ],
        expected_answer="B",
        explanation=(
            "Applying the fixture tests (method of attachment -- anchored to studs; "
            "adaptation -- custom fit to the space; intent -- permanent "
            "installation), the bookshelf is likely a fixture that conveys with the "
            "property."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="I. Real Property Characteristics, A. Fixtures and personal property",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-005",
        domain=Domain.LICENSING,
        subdomain="real_property_characteristics",
        question=(
            "A property is described as the NE 1/4 of the SW 1/4 of Section 12. How "
            "many acres does this parcel contain?"
        ),
        choices=[
            "A. 10 acres",
            "B. 20 acres",
            "C. 40 acres",
            "D. 160 acres",
        ],
        expected_answer="C",
        explanation=(
            "A section contains 640 acres. The SW 1/4 = 160 acres. The NE 1/4 of "
            "that = 160 / 4 = 40 acres."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="I. Real Property Characteristics, B. Legal descriptions",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-006",
        domain=Domain.LICENSING,
        subdomain="real_property_characteristics",
        question=(
            "A property owner grants a conservation easement to a land trust,"
            "permanently restricting development on 50 acres. What type of easement "
            "is this?"
        ),
        choices=[
            "A. Easement appurtenant",
            "B. Easement by necessity",
            "C. Easement in gross",
            "D. Prescriptive easement",
        ],
        expected_answer="C",
        explanation=(
            "A conservation easement held by a land trust is an easement in gross "
            "because it benefits the land trust as an entity rather than an "
            "adjacent property."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="I. Real Property Characteristics, C. Property use and rights",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-007",
        domain=Domain.LICENSING,
        subdomain="real_property_characteristics",
        question=(
            "A commercial tenant installs a custom hydraulic car lift in a leased "
            "auto repair shop, bolting it to the concrete floor. The lease is "
            "silent on trade fixtures. At lease end, can the tenant remove it?"
        ),
        choices=[
            "A. No, because it is permanently attached to the building",
            "B. Yes, because trade fixtures remain the tenant's personal property",
            "C. No, because all improvements belong to the landlord",
            "D. Yes, but only if the landlord consents in writing",
        ],
        expected_answer="B",
        explanation=(
            "Trade fixtures are an exception to the general fixture rule. Items "
            "installed by a tenant for business purposes may be removed before or "
            "at lease end, provided the tenant repairs any damage."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="I. Real Property Characteristics, A. Fixtures and personal property",
        difficulty="hard",
    ),
    Instance(
        instance_id="licensing-national-008",
        domain=Domain.LICENSING,
        subdomain="real_property_characteristics",
        question=(
            "A property owner discovers that a neighbor's fence encroaches 2 feet "
            "onto their land. The fence has been there for 25 years, exceeding the "
            "state's statutory period for adverse possession. The neighbor claims "
            "no hostile intent. A broker advising the owner should explain that:"
        ),
        choices=[
            "A. The neighbor automatically owns the 2-foot strip through adverse possession",
            (
                "B. Adverse possession requires hostile use regardless"
                " of the neighbor's subjective intent"
            ),
            "C. The encroachment is irrelevant because fences are always on property lines",
            "D. Only a court can determine property boundaries, so the broker cannot advise",
        ],
        expected_answer="B",
        explanation=(
            "Most jurisdictions apply an objective standard for hostile use in "
            "adverse possession -- the claimant need not have subjective hostile "
            "intent, only that the use was without permission and inconsistent with "
            "the true owner's rights."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="I. Real Property Characteristics, C. Property use and rights",
        difficulty="hard",
    ),
]

# ---------------------------------------------------------------------------
# Topic II: Forms of Ownership, Transfer & Recording of Title
# ---------------------------------------------------------------------------
_TOPIC_II: list[Instance] = [
    Instance(
        instance_id="licensing-national-009",
        domain=Domain.LICENSING,
        subdomain="ownership_and_title",
        question="In a joint tenancy, what happens to a deceased tenant's interest?",
        choices=[
            "A. It passes to the deceased's heirs through probate",
            "B. It passes to the surviving joint tenant(s) by right of survivorship",
            "C. It reverts to the state through escheat",
            "D. It is divided equally among all living relatives",
        ],
        expected_answer="B",
        explanation=(
            "The defining feature of joint tenancy is the right of survivorship. "
            "When one joint tenant dies, their interest automatically passes to the "
            "surviving joint tenant(s) without going through probate."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="II. Forms of Ownership, A. Joint tenancy",
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-010",
        domain=Domain.LICENSING,
        subdomain="ownership_and_title",
        question="Which type of deed provides the GREATEST protection to the grantee?",
        choices=[
            "A. Quitclaim deed",
            "B. Bargain and sale deed",
            "C. General warranty deed",
            "D. Special warranty deed",
        ],
        expected_answer="C",
        explanation=(
            "A general warranty deed provides the most protection because the "
            "grantor warrants title against all defects, including those arising "
            "before the grantor's ownership."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="II. Forms of Ownership, B. Transfer of title",
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-011",
        domain=Domain.LICENSING,
        subdomain="ownership_and_title",
        question="Title insurance protects the insured against:",
        choices=[
            "A. Future liens placed on the property after closing",
            "B. Physical damage to the property",
            "C. Defects in title that existed before the policy date but were not discovered",
            "D. Depreciation in property value",
        ],
        expected_answer="C",
        explanation=(
            "Title insurance protects against losses arising from defects in title "
            "that existed at or before the policy date but were not discovered "
            "during the title search."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="II. Forms of Ownership, C. Recording of title",
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-012",
        domain=Domain.LICENSING,
        subdomain="ownership_and_title",
        question=(
            "Three friends purchase a property as joint tenants. One friend later "
            "sells their interest to a fourth party without the others' knowledge. "
            "What form of ownership exists after the sale?"
        ),
        choices=[
            "A. The three remaining owners hold as joint tenants",
            "B. All three owners hold as tenants in common",
            (
                "C. The two original owners remain joint tenants"
                " with each other, and the new owner is a tenant in common"
            ),
            "D. The sale is void because it was done without the other owners' consent",
        ],
        expected_answer="C",
        explanation=(
            "When one joint tenant conveys their interest, it severs the joint "
            "tenancy only as to that share. The two original owners retain joint "
            "tenancy between themselves, while the new buyer holds their 1/3 as a "
            "tenant in common."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="II. Forms of Ownership, A. Joint tenancy",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-013",
        domain=Domain.LICENSING,
        subdomain="ownership_and_title",
        question=(
            "A developer creates a condominium by recording a declaration and plat "
            "map. Each unit owner receives:"
        ),
        choices=[
            "A. A leasehold interest in their unit",
            "B. Fee simple ownership of their unit and an undivided interest in common elements",
            "C. A life estate in their unit",
            "D. A tenancy in common interest in the entire building",
        ],
        expected_answer="B",
        explanation=(
            "In a condominium, each owner holds fee simple title to their "
            "individual unit and an undivided percentage interest in the common "
            "elements (lobby, hallways, grounds, etc.)."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="II. Forms of Ownership, B. Condominium ownership",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-014",
        domain=Domain.LICENSING,
        subdomain="ownership_and_title",
        question=(
            "Buyer A records their deed on Monday. Buyer B, who purchased the same "
            "property from the same seller, records on Tuesday. In a race-notice "
            "recording state, who has priority?"
        ),
        choices=[
            "A. Buyer A, because they recorded first",
            "B. Buyer B, if they purchased without notice of Buyer A's interest",
            (
                "C. Buyer A, only if they purchased without notice"
                " of Buyer B's interest and recorded first"
            ),
            "D. The seller, because they committed fraud",
        ],
        expected_answer="C",
        explanation=(
            "In a race-notice state, a subsequent purchaser prevails only if they "
            "(1) purchased without notice of the prior interest AND (2) recorded "
            "first. Here, Buyer A recorded first and must also have been a bona "
            "fide purchaser without notice to have priority."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="II. Forms of Ownership, C. Recording of title",
        difficulty="hard",
    ),
    Instance(
        instance_id="licensing-national-015",
        domain=Domain.LICENSING,
        subdomain="ownership_and_title",
        question=(
            "A married couple owns property as tenants by the entirety. The husband "
            "files for bankruptcy individually. What happens to the property?"
        ),
        choices=[
            "A. The entire property can be seized to satisfy the husband's debts",
            "B. The husband's half-interest can be seized, converting to tenancy in common",
            "C. The property is generally protected from the husband's individual creditors",
            "D. The property must be sold and proceeds split equally",
        ],
        expected_answer="C",
        explanation=(
            "Tenancy by the entirety provides protection from individual creditors "
            "of one spouse. Neither spouse can unilaterally convey or encumber the "
            "property. Only joint creditors of both spouses can typically reach the "
            "property."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="II. Forms of Ownership, A. Tenancy by the entirety",
        difficulty="hard",
    ),
]

# ---------------------------------------------------------------------------
# Topic III: Property Value & Appraisal
# ---------------------------------------------------------------------------
_TOPIC_III: list[Instance] = [
    Instance(
        instance_id="licensing-national-016",
        domain=Domain.LICENSING,
        subdomain="property_value_and_appraisal",
        question="The principle of substitution states that:",
        choices=[
            (
                "A. A property's value is determined by the cost to acquire an equally desirable "
                "substitute"
            ),
            "B. Properties in the same neighborhood always have the same value",
            "C. The value of a property increases when nearby properties are improved",
            "D. All properties eventually return to their original value",
        ],
        expected_answer="A",
        explanation=(
            "The principle of substitution is foundational to all three appraisal "
            "approaches. It states that a rational buyer will pay no more for a "
            "property than the cost of acquiring an equally desirable substitute."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="III. Property Value and Appraisal, A. Principles of value",
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-017",
        domain=Domain.LICENSING,
        subdomain="property_value_and_appraisal",
        question=(
            "A broker is preparing a competitive market analysis (CMA) for a "
            "listing presentation. Which of the following is TRUE about a CMA "
            "versus a formal appraisal?"
        ),
        choices=[
            "A. A CMA and an appraisal are interchangeable for lending purposes",
            (
                "B. A CMA is an opinion of value prepared by a licensed agent, not a certified "
                "appraiser"
            ),
            "C. A CMA must comply with USPAP standards",
            "D. A CMA carries the same legal weight as a formal appraisal",
        ],
        expected_answer="B",
        explanation=(
            "A CMA is a market analysis prepared by a real estate licensee to help "
            "determine a listing or offer price. It is NOT a formal appraisal and "
            "does not need to comply with USPAP."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.BROKER,
        source_outline="III. Property Value and Appraisal, E. Broker price opinions",
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-018",
        domain=Domain.LICENSING,
        subdomain="property_value_and_appraisal",
        question=(
            "Which economic principle explains why adding a swimming pool worth"
            "$50,000 to a modest home in a declining neighborhood may only increase "
            "the home's value by $10,000?"
        ),
        choices=[
            "A. Principle of contribution",
            "B. Principle of conformity",
            "C. Principle of highest and best use",
            "D. Principle of anticipation",
        ],
        expected_answer="A",
        explanation=(
            "The principle of contribution states that the value of an improvement "
            "is measured by what it adds to the property's total value, not by its "
            "cost."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="III. Property Value and Appraisal, A. Principles of value",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-019",
        domain=Domain.LICENSING,
        subdomain="property_value_and_appraisal",
        question=(
            "An appraiser identifies three comparable sales: $310,000, $325,000,"
            "and $340,000. Comparable 1 has a smaller lot and needs a +$15,000 "
            "adjustment. Comparable 2 needs no adjustments. Comparable 3 has an "
            "extra bathroom requiring a -$10,000 adjustment. What is the indicated "
            "value using the sales comparison approach?"
        ),
        choices=[
            "A. $310,000",
            "B. $325,000",
            "C. $330,000",
            "D. $340,000",
        ],
        expected_answer="B",
        explanation=(
            "Adjusted values: Comp 1 = $310,000 + $15,000 = $325,000. Comp 2 = "
            "$325,000 (no adjustment). Comp 3 = $340,000 - $10,000 = $330,000. Comp "
            "2 requires no adjustment and is the most reliable indicator at "
            "$325,000."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="III. Property Value and Appraisal, B. Appraisal process",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-020",
        domain=Domain.LICENSING,
        subdomain="property_value_and_appraisal",
        question=(
            "A commercial property generates $120,000 in net operating income"
            "(NOI). The capitalization rate for similar properties is 8%. What is "
            "the property's value using the income approach?"
        ),
        choices=[
            "A. $960,000",
            "B. $1,200,000",
            "C. $1,500,000",
            "D. $1,800,000",
        ],
        expected_answer="C",
        explanation="Value = NOI / Cap Rate = $120,000 / 0.08 = $1,500,000.",
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="III. Property Value and Appraisal, C. Income approach",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-021",
        domain=Domain.LICENSING,
        subdomain="property_value_and_appraisal",
        question="Functional obsolescence in a property can be caused by:",
        choices=[
            "A. A busy highway built next to the property",
            "B. Normal wear and tear over time",
            "C. An outdated floor plan with insufficient bathrooms for the number of bedrooms",
            "D. A declining neighborhood",
        ],
        expected_answer="C",
        explanation=(
            "Functional obsolescence is a loss in value due to deficiencies in the "
            "design or features of the property itself. A busy highway and "
            "declining neighborhood are external obsolescence. Normal wear is "
            "physical deterioration."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="III. Property Value and Appraisal, D. Cost approach",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-022",
        domain=Domain.LICENSING,
        subdomain="property_value_and_appraisal",
        question=(
            "Which appraisal approach is most appropriate for valuing a unique,"
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
            "The cost approach is most appropriate when the property is unique and "
            "there are few or no comparable sales. It estimates value by "
            "calculating the cost to reproduce or replace the improvements, minus "
            "depreciation, plus land value."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="III. Property Value and Appraisal, B. Appraisal process",
        difficulty="hard",
    ),
    Instance(
        instance_id="licensing-national-023",
        domain=Domain.LICENSING,
        subdomain="property_value_and_appraisal",
        question=(
            "An appraiser is valuing a 20-year-old office building. The replacement "
            "cost new is $2,000,000. Physical deterioration is estimated at 15%,"
            "functional obsolescence at 5%, and external obsolescence at 3%. The "
            "land value is $500,000. What is the indicated value?"
        ),
        choices=[
            "A. $1,540,000",
            "B. $2,040,000",
            "C. $2,500,000",
            "D. $2,270,000",
        ],
        expected_answer="B",
        explanation=(
            "Total depreciation = 15% + 5% + 3% = 23%. Depreciated improvement "
            "value = $2,000,000 x (1 - 0.23) = $1,540,000. Total value = $1,540,000 "
            "+ $500,000 land = $2,040,000."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="III. Property Value and Appraisal, D. Cost approach",
        difficulty="hard",
    ),
]

# ---------------------------------------------------------------------------
# Topic IV: Real Estate Contracts & Agency
# ---------------------------------------------------------------------------
_TOPIC_IV: list[Instance] = [
    Instance(
        instance_id="licensing-national-024",
        domain=Domain.LICENSING,
        subdomain="contracts_and_agency",
        question="What are the essential elements required for a valid real estate contract?",
        choices=[
            "A. Offer, acceptance, and a notarized signature",
            (
                "B. Competent parties, offer and acceptance, consideration, legal purpose, and in "
                "writing"
            ),
            "C. An attorney's approval, earnest money, and two witnesses",
            "D. A licensed broker, written agreement, and government approval",
        ],
        expected_answer="B",
        explanation=(
            "A valid real estate contract requires competent parties, mutual assent "
            "(offer and acceptance), consideration, lawful purpose, and under the "
            "Statute of Frauds must be in writing to be enforceable."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="IV. Real Estate Contracts and Agency, A. Contract elements",
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-025",
        domain=Domain.LICENSING,
        subdomain="contracts_and_agency",
        question="A buyer's agent owes all of the following fiduciary duties to the buyer EXCEPT:",
        choices=[
            "A. Loyalty",
            "B. Obedience",
            "C. Disclosure of the buyer's maximum price to the seller",
            "D. Accounting",
        ],
        expected_answer="C",
        explanation=(
            "A buyer's agent owes OLDCAR duties: Obedience, Loyalty, Disclosure, "
            "Confidentiality, Accounting, and Reasonable care. Disclosing the "
            "buyer's maximum price would violate confidentiality and loyalty."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="IV. Real Estate Contracts and Agency, B. Agency relationships",
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-026",
        domain=Domain.LICENSING,
        subdomain="contracts_and_agency",
        question="In an exclusive right-to-sell listing agreement, the broker earns a commission:",
        choices=[
            "A. Only if the broker personally finds the buyer",
            "B. Regardless of who finds the buyer, including the seller",
            "C. Only if the property sells above the listing price",
            "D. Only if the buyer uses their own financing",
        ],
        expected_answer="B",
        explanation=(
            "An exclusive right-to-sell listing entitles the broker to a commission "
            "regardless of who procures the buyer -- even if the seller finds the "
            "buyer independently."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="IV. Real Estate Contracts and Agency, E. Listing agreements",
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-027",
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
            "conditions are discovered."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="IV. Real Estate Contracts and Agency, D. Sales contract",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-028",
        domain=Domain.LICENSING,
        subdomain="contracts_and_agency",
        question=(
            "A seller lists their home at $450,000. A buyer submits an offer at"
            "$420,000. The seller responds with a counter-offer at $440,000. Which "
            "statement is TRUE?"
        ),
        choices=[
            "A. The original offer of $420,000 is still binding on the buyer",
            "B. The counter-offer terminates the original offer",
            "C. Both the original offer and counter-offer are binding",
            "D. The seller must accept the original offer if the buyer rejects the counter",
        ],
        expected_answer="B",
        explanation=(
            "A counter-offer terminates the original offer. Once the seller makes a "
            "counter-offer, the buyer's original offer of $420,000 is extinguished."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="IV. Real Estate Contracts and Agency, C. Offer and acceptance",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-029",
        domain=Domain.LICENSING,
        subdomain="contracts_and_agency",
        question=(
            "A buyer submits an offer with an earnest money deposit of $10,000. The "
            "offer is accepted, but the buyer later defaults without a legal "
            "excuse. Under a liquidated damages clause, the seller:"
        ),
        choices=[
            "A. Must return the earnest money to the buyer",
            "B. May retain the earnest money as liquidated damages",
            "C. Can sue for the full purchase price plus the earnest money",
            "D. Must split the earnest money with the listing broker",
        ],
        expected_answer="B",
        explanation=(
            "A liquidated damages clause specifies the earnest money deposit as the "
            "agreed-upon damages in case of buyer default. The seller retains the "
            "deposit as their sole remedy."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="IV. Real Estate Contracts and Agency, D. Sales contract",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-030",
        domain=Domain.LICENSING,
        subdomain="contracts_and_agency",
        question=(
            "The Statute of Frauds requires that certain contracts be in writing to "
            "be enforceable. Which of the following is NOT required to be in "
            "writing under the Statute of Frauds?"
        ),
        choices=[
            "A. A lease for 13 months",
            "B. A contract for the sale of real property",
            "C. A listing agreement authorizing a broker to sell property",
            "D. An oral agreement to share a real estate commission between brokers",
        ],
        expected_answer="D",
        explanation=(
            "The Statute of Frauds requires written contracts for the sale of real "
            "property, leases exceeding one year, and listing agreements. "
            "Commission-sharing agreements between brokers are generally not "
            "specifically required by the Statute of Frauds."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="IV. Real Estate Contracts and Agency, A. Contract elements",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-031",
        domain=Domain.LICENSING,
        subdomain="contracts_and_agency",
        question=(
            "A listing agent receives an offer on their listing and simultaneously "
            "has a buyer client who wants to make an offer on the same property. "
            "The broker must:"
        ),
        choices=[
            "A. Reject the outside offer to protect their buyer client",
            "B. Present all offers to the seller and disclose the dual agency situation",
            "C. Only present the higher offer to the seller",
            "D. Withdraw from representing the buyer to avoid any conflict",
        ],
        expected_answer="B",
        explanation=(
            "Agents must present all offers to the seller. Additionally, the "
            "potential for dual agency must be disclosed. The broker cannot "
            "suppress offers or favor one client over another."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="IV. Real Estate Contracts and Agency, B. Agency relationships",
        difficulty="hard",
    ),
    Instance(
        instance_id="licensing-national-032",
        domain=Domain.LICENSING,
        subdomain="contracts_and_agency",
        question=(
            "A buyer's agent discovers that the property they are showing has a "
            "material defect that the seller has not disclosed. The listing agent "
            "has assured the buyer's agent everything is fine. The buyer's agent "
            "should:"
        ),
        choices=[
            "A. Trust the listing agent's assurance and say nothing",
            "B. Disclose the known defect to their buyer client immediately",
            "C. Wait until after closing to mention the defect",
            "D. Contact the seller directly to demand repairs",
        ],
        expected_answer="B",
        explanation=(
            "A buyer's agent owes fiduciary duties to the buyer, including "
            "disclosure of all material facts. The duty to disclose overrides any "
            "informal assurances from the listing agent."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="IV. Real Estate Contracts and Agency, B. Agency relationships",
        difficulty="hard",
    ),
    Instance(
        instance_id="licensing-national-033",
        domain=Domain.LICENSING,
        subdomain="contracts_and_agency",
        question=(
            "A property is under contract. The buyer discovers a previously unknown "
            "easement that was not disclosed and that significantly limits their "
            "planned use. The seller claims the contract is 'as-is.' Which analysis "
            "is MOST accurate?"
        ),
        choices=[
            "A. The 'as-is' clause protects the seller from all claims",
            (
                "B. The undisclosed easement may constitute a failure"
                " of marketable title, allowing the buyer to rescind"
            ),
            "C. The buyer must close and then sue the seller for damages",
            "D. Easements never affect property value so the buyer has no claim",
        ],
        expected_answer="B",
        explanation=(
            "An undisclosed easement that materially affects use may constitute a "
            "title defect. An 'as-is' clause typically applies to physical "
            "condition, not title defects. The buyer likely has grounds to rescind."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="IV. Real Estate Contracts and Agency, D. Sales contract",
        difficulty="hard",
    ),
]

# ---------------------------------------------------------------------------
# Topic V: Real Estate Practice (incl. Fair Housing & Risk Management)
# ---------------------------------------------------------------------------
_TOPIC_V: list[Instance] = [
    Instance(
        instance_id="licensing-national-034",
        domain=Domain.LICENSING,
        subdomain="real_estate_practice",
        question="Under the Fair Housing Act, which of the following is a protected class?",
        choices=[
            "A. Marital status",
            "B. Sexual orientation",
            "C. Familial status",
            "D. Source of income",
        ],
        expected_answer="C",
        explanation=(
            "The federal Fair Housing Act protects seven classes: race, color, "
            "religion, national origin, sex, familial status, and disability."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="V. Real Estate Practice, A. Fair Housing laws",
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-035",
        domain=Domain.LICENSING,
        subdomain="real_estate_practice",
        question="Steering in real estate refers to:",
        choices=[
            "A. Directing buyers away from certain neighborhoods based on protected class",
            "B. A negotiation technique where brokers guide price discussions",
            "C. The practice of requiring buyers to use a specific lender",
            "D. Marketing properties only through exclusive channels",
        ],
        expected_answer="A",
        explanation=(
            "Steering is the illegal practice of directing buyers toward or away "
            "from certain areas based on race, color, religion, national origin, "
            "sex, familial status, or disability."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="V. Real Estate Practice, A. Fair Housing laws",
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-036",
        domain=Domain.LICENSING,
        subdomain="real_estate_practice",
        question="The Americans with Disabilities Act (ADA) requires:",
        choices=[
            "A. All residential properties to be wheelchair accessible",
            (
                "B. Public accommodations and commercial facilities"
                " to be accessible to persons with disabilities"
            ),
            "C. Only government buildings to meet accessibility standards",
            "D. Landlords to allow pets in all rental units",
        ],
        expected_answer="B",
        explanation=(
            "The ADA requires public accommodations and commercial facilities to be "
            "accessible to persons with disabilities. It does not apply to private "
            "residential properties."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="V. Real Estate Practice, A. Fair Housing laws",
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-037",
        domain=Domain.LICENSING,
        subdomain="real_estate_practice",
        question="A broker's trust account must be:",
        choices=[
            "A. A personal savings account at any financial institution",
            "B. A separate, designated account at a recognized depository",
            "C. Combined with the broker's operating account for convenience",
            "D. An investment account to maximize returns for clients",
        ],
        expected_answer="B",
        explanation=(
            "A broker's trust (or escrow) account must be a separate, designated "
            "account at a recognized depository institution. Commingling trust "
            "funds with personal or operating funds is a serious violation."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.BROKER,
        source_outline="V. Real Estate Practice, B. Trust accounts",
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-038",
        domain=Domain.LICENSING,
        subdomain="real_estate_practice",
        question=(
            "A landlord refuses to rent to a family with children, stating the "
            "property is for 'adults only.' The property is a 10-unit apartment "
            "building. Is this a Fair Housing violation?"
        ),
        choices=[
            "A. No, landlords can set any tenant criteria they choose",
            "B. Yes, unless the property qualifies as housing for older persons",
            "C. No, because families with children are not a protected class",
            "D. Yes, but only if the family files a complaint within 30 days",
        ],
        expected_answer="B",
        explanation=(
            "Familial status is a protected class under the Fair Housing Act. "
            "Refusing to rent to families with children is illegal unless the "
            "property qualifies as 'housing for older persons' (55+ or 62+ "
            "communities)."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="V. Real Estate Practice, A. Fair Housing laws",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-039",
        domain=Domain.LICENSING,
        subdomain="real_estate_practice",
        question=(
            "An agent writes an advertisement for a property in a predominantly "
            "Spanish-speaking neighborhood stating: 'Perfect for English-speaking "
            "professionals.' This ad is:"
        ),
        choices=[
            "A. Legal, because language preference is not a protected class",
            "B. A potential Fair Housing violation based on national origin discrimination",
            "C. Acceptable if the agent is merely describing the neighborhood",
            "D. Required by local advertising standards",
        ],
        expected_answer="B",
        explanation=(
            "Using 'English-speaking' as a qualifier in advertising can constitute "
            "national origin discrimination under the Fair Housing Act. HUD has "
            "found that language-based restrictions can be a proxy for national "
            "origin discrimination."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="V. Real Estate Practice, A. Fair Housing laws",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-040",
        domain=Domain.LICENSING,
        subdomain="real_estate_practice",
        question=(
            "A licensed salesperson moves from Broker A to Broker B. The "
            "salesperson has active listings under Broker A. What happens to those "
            "listings?"
        ),
        choices=[
            "A. The listings automatically transfer to Broker B",
            (
                "B. The listings remain with Broker A since the listing agreement is between the "
                "seller and the broker"
            ),
            "C. The listings are automatically canceled",
            "D. The salesperson can take the listings to Broker B without seller consent",
        ],
        expected_answer="B",
        explanation=(
            "Listing agreements are between the seller and the brokerage firm, not "
            "between the seller and the individual agent."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="V. Real Estate Practice, D. Brokerage operations",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-041",
        domain=Domain.LICENSING,
        subdomain="real_estate_practice",
        question=(
            "A broker receives multiple offers on a listing. One offer includes an "
            "escalation clause. The broker should:"
        ),
        choices=[
            "A. Disclose the escalation clause to all competing buyers",
            "B. Present all offers to the seller including the escalation clause terms",
            "C. Remove the escalation clause to create a level playing field",
            "D. Only present the escalation clause offer to the seller",
        ],
        expected_answer="B",
        explanation=(
            "The broker has a duty to present ALL offers to the seller. The broker "
            "must NOT disclose terms of one offer to competing buyers, and must NOT "
            "modify or remove offer terms."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="V. Real Estate Practice, C. Broker supervision and risk management",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-042",
        domain=Domain.LICENSING,
        subdomain="real_estate_practice",
        question=(
            "A managing broker discovers that a newly licensed agent under their "
            "supervision has been conducting open houses without disclosing their "
            "agency relationship to visitors. The managing broker:"
        ),
        choices=[
            "A. Has no liability because the agent is independently responsible",
            "B. May be held vicariously liable for the agent's failure to disclose",
            "C. Is only liable if a formal complaint is filed",
            "D. Can avoid liability by terminating the agent immediately",
        ],
        expected_answer="B",
        explanation=(
            "Managing brokers have supervisory responsibility for their agents. "
            "Under respondeat superior the managing broker can be held vicariously "
            "liable for the acts of agents under their supervision."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="V. Real Estate Practice, C. Broker supervision and risk management",
        difficulty="hard",
    ),
    Instance(
        instance_id="licensing-national-043",
        domain=Domain.LICENSING,
        subdomain="real_estate_practice",
        question=(
            "A property owner wants to sell their single-family home without using "
            "a broker. They place a 'For Sale' sign that reads 'No Children.' Under "
            "the Fair Housing Act:"
        ),
        choices=[
            "A. This is legal because the owner is not using a broker",
            "B. The Mrs. Murphy exemption applies, so this is legal",
            "C. This is illegal because discriminatory advertising is never exempt",
            "D. This is legal because single-family home sales are always exempt",
        ],
        expected_answer="C",
        explanation=(
            "While the Fair Housing Act has exemptions for certain private sales, "
            "discriminatory advertising is NEVER exempt. The sign 'No Children' "
            "violates the Act's advertising provisions regardless of any sale "
            "exemption."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="V. Real Estate Practice, A. Fair Housing laws",
        difficulty="hard",
    ),
    Instance(
        instance_id="licensing-national-044",
        domain=Domain.LICENSING,
        subdomain="real_estate_practice",
        question=(
            "A broker discovers that an agent in the office has been commingling "
            "client trust funds with personal funds. The broker's FIRST step should "
            "be:"
        ),
        choices=[
            "A. Terminate the agent immediately and report to the state regulatory agency",
            (
                "B. Conduct an immediate audit of the trust account to determine the extent of the "
                "issue"
            ),
            "C. Wait until the monthly reconciliation to address the issue",
            "D. Ask the agent to reimburse the trust account and keep it confidential",
        ],
        expected_answer="B",
        explanation=(
            "The broker's first priority is to protect client funds. An immediate "
            "audit determines the extent of the commingling and ensures all client "
            "funds are accounted for."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="V. Real Estate Practice, B. Trust accounts",
        difficulty="hard",
    ),
]

# ---------------------------------------------------------------------------
# Topic VI: Property Disclosures & Environmental Issues
# ---------------------------------------------------------------------------
_TOPIC_VI: list[Instance] = [
    Instance(
        instance_id="licensing-national-045",
        domain=Domain.LICENSING,
        subdomain="disclosures_and_environmental",
        question=(
            "Under federal law, sellers of homes built before which year must "
            "disclose known lead-based paint hazards?"
        ),
        choices=[
            "A. 1960",
            "B. 1970",
            "C. 1978",
            "D. 1990",
        ],
        expected_answer="C",
        explanation=(
            "The Residential Lead-Based Paint Hazard Reduction Act of 1992 requires "
            "disclosure of known lead-based paint hazards for homes built before "
            "1978."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="VI. Property Disclosures and Environmental Issues, A. Lead-based paint",
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-046",
        domain=Domain.LICENSING,
        subdomain="disclosures_and_environmental",
        question="Asbestos is most commonly found in homes built before which decade?",
        choices=[
            "A. 1950s",
            "B. 1960s",
            "C. 1980s",
            "D. 1990s",
        ],
        expected_answer="C",
        explanation=(
            "Asbestos was widely used in building materials through the late 1970s "
            "and into the early 1980s."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline=(
            "VI. Property Disclosures and Environmental Issues, B. Environmental hazards"
        ),
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-047",
        domain=Domain.LICENSING,
        subdomain="disclosures_and_environmental",
        question="Radon is:",
        choices=[
            "A. A visible gas produced by decaying organic matter",
            "B. An odorless, radioactive gas produced by the natural decay of uranium in soil",
            "C. A gas only found in commercial buildings",
            "D. A gas that only affects properties built before 1980",
        ],
        expected_answer="B",
        explanation=(
            "Radon is a naturally occurring, odorless, colorless radioactive gas "
            "produced by the decay of uranium in soil and rock."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline=(
            "VI. Property Disclosures and Environmental Issues, B. Environmental hazards"
        ),
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-048",
        domain=Domain.LICENSING,
        subdomain="disclosures_and_environmental",
        question=(
            "CERCLA (Superfund) imposes liability for environmental cleanup on all "
            "of the following EXCEPT:"
        ),
        choices=[
            "A. Current property owners",
            "B. Previous owners who owned the property when contamination occurred",
            (
                "C. A buyer who conducted a Phase I environmental assessment and found no "
                "contamination"
            ),
            "D. Parties who arranged for disposal of hazardous substances at the site",
        ],
        expected_answer="C",
        explanation=(
            "CERCLA provides an 'innocent landowner' defense for purchasers who "
            "conducted appropriate due diligence (such as a Phase I ESA) before "
            "acquiring the property and had no knowledge of contamination."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline=(
            "VI. Property Disclosures and Environmental Issues, B. Environmental hazards"
        ),
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-049",
        domain=Domain.LICENSING,
        subdomain="disclosures_and_environmental",
        question=(
            "A seller knows their basement floods every spring but checks 'No' on "
            "the disclosure form for water intrusion. The buyer discovers the "
            "flooding after closing. The seller is likely liable for:"
        ),
        choices=[
            "A. Nothing, because the buyer should have inspected",
            "B. Fraudulent misrepresentation for knowingly concealing a material defect",
            "C. Only the cost of a sump pump",
            "D. Nothing, because caveat emptor applies after closing",
        ],
        expected_answer="B",
        explanation=(
            "Knowingly misrepresenting or concealing a known material defect on a "
            "disclosure form constitutes fraudulent misrepresentation."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="VI. Property Disclosures and Environmental Issues, C. Seller disclosures",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-050",
        domain=Domain.LICENSING,
        subdomain="disclosures_and_environmental",
        question=(
            "A listing agent learns from a neighbor that the property next door was "
            "formerly a dry cleaning business with potential soil contamination. "
            "The listing agent should:"
        ),
        choices=[
            "A. Ignore the information because it pertains to a neighboring property",
            "B. Disclose the information to prospective buyers as a potential material fact",
            "C. Wait until the buyer asks about environmental issues",
            "D. Tell the seller to handle the disclosure themselves",
        ],
        expected_answer="B",
        explanation=(
            "Agents have a duty to disclose known material facts that could affect "
            "a buyer's decision. Potential soil contamination from an adjacent "
            "property is a material fact requiring disclosure."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="VI. Property Disclosures and Environmental Issues, C. Seller disclosures",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-051",
        domain=Domain.LICENSING,
        subdomain="disclosures_and_environmental",
        question=(
            "A buyer purchasing a property in a known flood zone must obtain flood insurance if:"
        ),
        choices=[
            "A. The property is in any FEMA-designated flood zone",
            (
                "B. The buyer is obtaining a federally backed mortgage and the property is in a "
                "Special Flood Hazard Area"
            ),
            "C. The seller previously had a flood insurance policy",
            "D. The local municipality requires it for all properties",
        ],
        expected_answer="B",
        explanation=(
            "The National Flood Insurance Act requires that borrowers obtaining a "
            "federally backed mortgage on property in a Special Flood Hazard Area "
            "(SFHA) must purchase flood insurance."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="VI. Property Disclosures and Environmental Issues, D. Flood zones",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-052",
        domain=Domain.LICENSING,
        subdomain="disclosures_and_environmental",
        question=(
            "A commercial property is being sold. The buyer's Phase I Environmental "
            "Site Assessment reveals 'recognized environmental conditions' (RECs). "
            "The buyer wants to proceed. As the broker, what should you advise?"
        ),
        choices=[
            "A. Walk away immediately -- any REC makes the property unsellable",
            "B. Proceed to a Phase II ESA to characterize the contamination before closing",
            "C. Ignore the findings because the buyer has already committed",
            "D. Negotiate a lower price and close without further investigation",
        ],
        expected_answer="B",
        explanation=(
            "A Phase I identifies potential contamination (RECs) but does not "
            "confirm or quantify it. The standard next step is a Phase II ESA to "
            "determine if contamination actually exists."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline=(
            "VI. Property Disclosures and Environmental Issues, B. Environmental hazards"
        ),
        difficulty="hard",
    ),
]

# ---------------------------------------------------------------------------
# Topic VII: Financing & Settlement
# ---------------------------------------------------------------------------
_TOPIC_VII: list[Instance] = [
    Instance(
        instance_id="licensing-national-053",
        domain=Domain.LICENSING,
        subdomain="financing_and_settlement",
        question="What is the purpose of RESPA (Real Estate Settlement Procedures Act)?",
        choices=[
            "A. To regulate interest rates on residential mortgages",
            (
                "B. To protect consumers by requiring disclosure of"
                " settlement costs and prohibiting kickbacks"
            ),
            "C. To establish minimum down payment requirements",
            "D. To set maximum loan amounts for residential properties",
        ],
        expected_answer="B",
        explanation=(
            "RESPA protects consumers by requiring lenders and settlement agents to "
            "provide disclosures about settlement costs and by prohibiting "
            "kickbacks and referral fees."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="VII. Financing and Settlement, A. Federal lending regulations",
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-054",
        domain=Domain.LICENSING,
        subdomain="financing_and_settlement",
        question=(
            "A borrower's loan has an interest rate that adjusts annually based on "
            "the 1-year Treasury index plus a 2% margin. This is an example of:"
        ),
        choices=[
            "A. A fixed-rate mortgage",
            "B. An adjustable-rate mortgage (ARM)",
            "C. A balloon mortgage",
            "D. A reverse mortgage",
        ],
        expected_answer="B",
        explanation=(
            "An adjustable-rate mortgage (ARM) has an interest rate that changes "
            "periodically based on an index plus a margin."
        ),
        cognitive_level=CognitiveLevel.KNOWLEDGE,
        exam_type=ExamType.SALESPERSON,
        source_outline="VII. Financing and Settlement, B. Mortgage types",
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-055",
        domain=Domain.LICENSING,
        subdomain="financing_and_settlement",
        question=(
            "A buyer is obtaining a conventional loan with a 90% LTV ratio. The "
            "lender requires PMI. When can the borrower request removal of PMI?"
        ),
        choices=[
            "A. After 1 year of payments regardless of equity",
            "B. When the loan-to-value ratio reaches 80% based on the original value",
            "C. Only when the loan is fully paid off",
            "D. When property values increase in the area",
        ],
        expected_answer="B",
        explanation=(
            "Under the Homeowners Protection Act, borrowers can request PMI "
            "cancellation when the LTV reaches 80% of the original value. Automatic "
            "termination occurs at 78% LTV."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="VII. Financing and Settlement, C. Private mortgage insurance",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-056",
        domain=Domain.LICENSING,
        subdomain="financing_and_settlement",
        question=(
            "At closing, the buyer's settlement statement shows a credit for "
            "property taxes. This most likely means:"
        ),
        choices=[
            "A. The buyer prepaid the taxes at contract signing",
            "B. The seller has prepaid taxes beyond the closing date and is being reimbursed",
            "C. The seller owes taxes through the closing date that the buyer will pay later",
            "D. The government is providing a tax credit to the buyer",
        ],
        expected_answer="C",
        explanation=(
            "A credit to the buyer for property taxes typically means the seller "
            "owes taxes for the period up to closing but has not yet paid them."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="VII. Financing and Settlement, D. Settlement procedures",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-057",
        domain=Domain.LICENSING,
        subdomain="financing_and_settlement",
        question=(
            "The Equal Credit Opportunity Act (ECOA) prohibits lenders from "
            "discriminating based on all of the following EXCEPT:"
        ),
        choices=[
            "A. Race or color",
            "B. Receipt of public assistance income",
            "C. Credit history and debt-to-income ratio",
            "D. Marital status",
        ],
        expected_answer="C",
        explanation=(
            "ECOA prohibits discrimination based on race, color, religion, national "
            "origin, sex, marital status, age, and receipt of public assistance. "
            "Lenders MAY consider legitimate credit factors."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.BROKER,
        source_outline="VII. Financing and Settlement, A. Federal lending regulations",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-058",
        domain=Domain.LICENSING,
        subdomain="financing_and_settlement",
        question=(
            "A borrower has a TILA-disclosed APR of 6.75% on a loan with a 6.25%"
            "note rate. The difference is MOST likely due to:"
        ),
        choices=[
            "A. Borrower's poor credit score",
            (
                "B. Prepaid finance charges (points, origination fees, PMI) included in the APR "
                "calculation"
            ),
            "C. An error in the lender's disclosure",
            "D. The adjustable-rate feature of the loan",
        ],
        expected_answer="B",
        explanation=(
            "The APR under TILA includes the note rate plus prepaid finance charges "
            "such as origination fees, discount points, and PMI premiums."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="VII. Financing and Settlement, A. Federal lending regulations",
        difficulty="hard",
    ),
    Instance(
        instance_id="licensing-national-059",
        domain=Domain.LICENSING,
        subdomain="financing_and_settlement",
        question=(
            "A settlement agent discovers an unreleased mortgage lien from a "
            "previous owner. The current seller claims they paid off the prior "
            "owner's loan. The broker should advise:"
        ),
        choices=[
            "A. Proceed to closing since the seller says it was paid off",
            "B. Require the seller to obtain a lien release or payoff statement before closing",
            "C. Ask the buyer to waive the title issue",
            "D. Close the transaction and deal with the lien later",
        ],
        expected_answer="B",
        explanation=(
            "An unreleased mortgage lien is a cloud on title that must be resolved "
            "before closing. The lien must be formally released of record."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="VII. Financing and Settlement, D. Settlement procedures",
        difficulty="hard",
    ),
    Instance(
        instance_id="licensing-national-060",
        domain=Domain.LICENSING,
        subdomain="financing_and_settlement",
        question=(
            "Under the Dodd-Frank Act, a Qualified Mortgage (QM) must meet all of "
            "the following criteria EXCEPT:"
        ),
        choices=[
            "A. The borrower's total debt-to-income ratio does not exceed 43%",
            "B. The loan term does not exceed 30 years",
            "C. The loan must have a fixed interest rate for the entire term",
            "D. Points and fees do not exceed 3% of the loan amount",
        ],
        expected_answer="C",
        explanation=(
            "QM rules do not require a fixed rate. ARMs can be QMs if they meet "
            "other criteria: DTI at or below 43%, term at or below 30 years, no "
            "negative amortization, and points/fees at or below 3%."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="VII. Financing and Settlement, A. Federal lending regulations",
        difficulty="hard",
    ),
]

# ---------------------------------------------------------------------------
# Topic VIII: Real Estate Math Calculations
# ---------------------------------------------------------------------------
_TOPIC_VIII: list[Instance] = [
    Instance(
        instance_id="licensing-national-061",
        domain=Domain.LICENSING,
        subdomain="real_estate_math",
        question=(
            "A property sold for $425,000. The buyer obtained an 80% LTV loan at "
            "6.5% annual interest. What is the buyer's monthly interest payment for "
            "the first month?"
        ),
        choices=[
            "A. $1,841.67",
            "B. $2,302.08",
            "C. $2,760.42",
            "D. $1,472.92",
        ],
        expected_answer="A",
        explanation=(
            "Loan amount = $425,000 x 0.80 = $340,000. Annual interest = $340,000 x "
            "0.065 = $22,100. Monthly interest = $22,100 / 12 = $1,841.67."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="VIII. Real Estate Math Calculations",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-062",
        domain=Domain.LICENSING,
        subdomain="real_estate_math",
        question=(
            "A broker sells a property for $375,000. The listing agreement calls "
            "for a 6% commission split 50/50 with the selling broker. The listing "
            "agent receives 60% of their broker's share. How much does the listing "
            "agent receive?"
        ),
        choices=[
            "A. $6,750",
            "B. $11,250",
            "C. $22,500",
            "D. $13,500",
        ],
        expected_answer="A",
        explanation=(
            "Total commission = $375,000 x 0.06 = $22,500. Listing broker's share = "
            "$22,500 x 0.50 = $11,250. Listing agent's share = $11,250 x 0.60 = "
            "$6,750."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="VIII. Real Estate Math Calculations",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-063",
        domain=Domain.LICENSING,
        subdomain="real_estate_math",
        question=(
            "A property's market value is $350,000. The assessment ratio is 85%. "
            "The tax rate is 32 mills. What is the annual property tax?"
        ),
        choices=[
            "A. $9,520",
            "B. $11,200",
            "C. $8,400",
            "D. $10,150",
        ],
        expected_answer="A",
        explanation=(
            "Assessed value = $350,000 x 0.85 = $297,500. Tax = $297,500 x 32/1000 "
            "= $297,500 x 0.032 = $9,520."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="VIII. Real Estate Math Calculations",
        difficulty="medium",
    ),
    Instance(
        instance_id="licensing-national-064",
        domain=Domain.LICENSING,
        subdomain="real_estate_math",
        question=(
            "A rectangular lot measures 150 feet by 200 feet. How many acres does "
            "it contain? (1 acre = 43,560 square feet)"
        ),
        choices=[
            "A. 0.56 acres",
            "B. 0.69 acres",
            "C. 0.75 acres",
            "D. 1.00 acre",
        ],
        expected_answer="B",
        explanation=(
            "Area = 150 x 200 = 30,000 sq ft. Acres = 30,000 / 43,560 = 0.689 "
            "acres, rounded to 0.69 acres."
        ),
        cognitive_level=CognitiveLevel.APPLICATION,
        exam_type=ExamType.SALESPERSON,
        source_outline="VIII. Real Estate Math Calculations",
        difficulty="easy",
    ),
    Instance(
        instance_id="licensing-national-065",
        domain=Domain.LICENSING,
        subdomain="real_estate_math",
        question=(
            "A rental property has 8 units, each renting for $1,200/month. The "
            "vacancy rate is 5%. Annual operating expenses are $48,000. What is the "
            "net operating income (NOI)?"
        ),
        choices=[
            "A. $61,440",
            "B. $67,200",
            "C. $109,440",
            "D. $115,200",
        ],
        expected_answer="A",
        explanation=(
            "Gross potential income = 8 x $1,200 x 12 = $115,200. Vacancy loss = "
            "$115,200 x 0.05 = $5,760. Effective gross income = $115,200 - $5,760 = "
            "$109,440. NOI = $109,440 - $48,000 = $61,440."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="VIII. Real Estate Math Calculations",
        difficulty="hard",
    ),
    Instance(
        instance_id="licensing-national-066",
        domain=Domain.LICENSING,
        subdomain="real_estate_math",
        question=(
            "A borrower qualifies for a maximum housing expense ratio of 28% and a "
            "total debt ratio of 36%. Their gross monthly income is $8,500 with "
            "existing monthly debt of $650. What is the maximum monthly PITI they "
            "qualify for?"
        ),
        choices=[
            "A. $2,380",
            "B. $2,410",
            "C. $3,060",
            "D. $2,730",
        ],
        expected_answer="A",
        explanation=(
            "Front-end ratio: $8,500 x 0.28 = $2,380. Back-end ratio: $8,500 x 0.36 "
            "= $3,060. Back-end less existing debt: $3,060 - $650 = $2,410. Maximum "
            "PITI = LESSER of $2,380 and $2,410 = $2,380."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="VIII. Real Estate Math Calculations",
        difficulty="hard",
    ),
    Instance(
        instance_id="licensing-national-067",
        domain=Domain.LICENSING,
        subdomain="real_estate_math",
        question=(
            "An investor purchases a property for $500,000 and sells it 3 years "
            "later for $580,000, after spending $25,000 on improvements. Closing "
            "costs on the sale are $12,000. What is the capital gain?"
        ),
        choices=[
            "A. $43,000",
            "B. $55,000",
            "C. $68,000",
            "D. $80,000",
        ],
        expected_answer="A",
        explanation=(
            "Adjusted basis = $500,000 + $25,000 = $525,000. Net sale price = "
            "$580,000 - $12,000 = $568,000. Capital gain = $568,000 - $525,000 = "
            "$43,000."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="VIII. Real Estate Math Calculations",
        difficulty="hard",
    ),
    Instance(
        instance_id="licensing-national-068",
        domain=Domain.LICENSING,
        subdomain="real_estate_math",
        question=(
            "A property generates $180,000 annual gross income with a 10% vacancy "
            "rate. Operating expenses are 45% of effective gross income. If the cap "
            "rate is 9%, what is the property's value?"
        ),
        choices=[
            "A. $891,000",
            "B. $990,000",
            "C. $1,100,000",
            "D. $1,800,000",
        ],
        expected_answer="B",
        explanation=(
            "Effective gross income = $180,000 x (1 - 0.10) = $162,000. Operating "
            "expenses = $162,000 x 0.45 = $72,900. NOI = $162,000 - $72,900 = "
            "$89,100. Value = NOI / cap rate = $89,100 / 0.09 = $990,000."
        ),
        cognitive_level=CognitiveLevel.ANALYSIS,
        exam_type=ExamType.BROKER,
        source_outline="VIII. Real Estate Math Calculations",
        difficulty="hard",
    ),
]

# ---------------------------------------------------------------------------
# Aggregate all instances
# ---------------------------------------------------------------------------
ALL_LICENSING_INSTANCES: list[Instance] = (
    _TOPIC_I + _TOPIC_II + _TOPIC_III + _TOPIC_IV + _TOPIC_V + _TOPIC_VI + _TOPIC_VII + _TOPIC_VIII
)


def get_sample_instances() -> list[Instance]:
    """Return sample licensing exam instances for testing.

    Returns:
        List of sample Instance objects (first 3 instances).
    """
    return [instance.model_copy(deep=True) for instance in ALL_LICENSING_INSTANCES[:3]]


def get_all_instances() -> list[Instance]:
    """Return all licensing exam instances.

    Returns:
        List of all Instance objects for the licensing domain.
    """
    return [instance.model_copy(deep=True) for instance in ALL_LICENSING_INSTANCES]


def get_national_instances() -> list[Instance]:
    """Return all national exam instances.

    Returns:
        List of national-level Instance objects.
    """
    return [instance.model_copy(deep=True) for instance in ALL_LICENSING_INSTANCES]
