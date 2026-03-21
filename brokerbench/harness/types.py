"""Core data types for BrokerBench datasets and predictions."""

from __future__ import annotations

from pydantic import BaseModel, Field

from brokerbench.harness.constants import CognitiveLevel, Domain, ExamType


class Instance(BaseModel):
    """A single benchmark instance (question/task)."""

    instance_id: str = Field(description="Unique identifier, e.g. 'licensing-national-042'")
    domain: Domain = Field(description="Benchmark domain")
    subdomain: str = Field(default="", description="Topic area within the domain")
    question: str = Field(description="The question or task prompt")
    expected_answer: str = Field(description="Gold-label expected answer")

    # Optional fields depending on domain
    choices: list[str] | None = Field(
        default=None, description="Multiple-choice options (licensing domain)"
    )
    explanation: str = Field(default="", description="Gold-label explanation of the correct answer")
    cognitive_level: CognitiveLevel | None = Field(
        default=None, description="Bloom's taxonomy level (licensing domain)"
    )
    exam_type: ExamType | None = Field(
        default=None, description="Salesperson or Broker (licensing domain)"
    )
    source_outline: str = Field(default="", description="Reference to the source content outline")
    difficulty: str = Field(default="medium", description="Estimated difficulty: easy/medium/hard")
    context: str = Field(
        default="", description="Additional context (e.g. contract excerpt, loan file data)"
    )
    metadata: dict[str, str] = Field(
        default_factory=dict, description="Arbitrary key-value metadata"
    )


class Prediction(BaseModel):
    """A model's prediction for a single benchmark instance."""

    instance_id: str = Field(description="Must match an Instance.instance_id")
    model_name_or_path: str = Field(description="Identifier for the model that generated this")
    prediction: str = Field(description="The model's answer")
    reasoning: str = Field(default="", description="Optional chain-of-thought or explanation")
    raw_output: str = Field(default="", description="Full raw model output if different")
    metadata: dict[str, str] = Field(
        default_factory=dict, description="Arbitrary key-value metadata"
    )
