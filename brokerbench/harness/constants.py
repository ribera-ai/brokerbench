"""Constants, enums, and thresholds for BrokerBench evaluation."""

from enum import Enum


class Domain(str, Enum):
    """Benchmark domains."""

    LICENSING = "licensing"
    UNDERWRITING = "underwriting"
    LEGAL = "legal"
    MARKETING = "marketing"
    TRANSACTION_MANAGEMENT = "transaction_management"
    COMPLIANCE = "compliance"
    BROKERAGE_MANAGEMENT = "brokerage_management"
    CLIENT_ADVISORY = "client_advisory"


class CognitiveLevel(str, Enum):
    """Cognitive levels for licensing exam questions (Bloom's taxonomy)."""

    KNOWLEDGE = "knowledge"
    APPLICATION = "application"
    ANALYSIS = "analysis"
    EXPERT = "expert"


class ExamType(str, Enum):
    """Licensing exam variants."""

    SALESPERSON = "salesperson"
    BROKER = "broker"


class ResolutionStatus(str, Enum):
    """Whether a prediction resolved the instance correctly."""

    RESOLVED = "resolved"
    UNRESOLVED = "unresolved"
    ERROR = "error"


# Default scoring thresholds (0-1 scale)
DEFAULT_PASS_THRESHOLD = 0.70

# Domain weight defaults (must sum to 1.0)
DEFAULT_DOMAIN_WEIGHTS: dict[Domain, float] = {
    Domain.LICENSING: 0.15,
    Domain.UNDERWRITING: 0.15,
    Domain.LEGAL: 0.10,
    Domain.MARKETING: 0.08,
    Domain.TRANSACTION_MANAGEMENT: 0.15,
    Domain.COMPLIANCE: 0.12,
    Domain.BROKERAGE_MANAGEMENT: 0.13,
    Domain.CLIENT_ADVISORY: 0.12,
}

# Licensing exam topic areas (Pearson VUE / PSI national content outline)
LICENSING_TOPICS: list[str] = [
    "I. Real Property Characteristics, Legal Descriptions, and Property Use",
    "II. Forms of Ownership, Transfer, and Recording of Title",
    "III. Property Value and Appraisal",
    "IV. Real Estate Contracts and Agency",
    "V. Real Estate Practice and Fair Housing",
    "VI. Property Disclosures and Environmental Issues",
    "VII. Financing and Settlement",
    "VIII. Real Estate Math Calculations",
]
