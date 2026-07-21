"""LLM-as-judge (opus): is the trade-off analysis sound and the recommendation pragmatic?"""

from __future__ import annotations

from pydantic import BaseModel, Field

from adr_advisor.client import LLMClient
from adr_advisor.config import Settings
from adr_advisor.models import AdrResult


class AdviceGrade(BaseModel):
    analysis_quality: int = Field(ge=1, le=5, description="Are the per-option pros/cons accurate and fair?")
    recommendation_sound: int = Field(ge=1, le=5, description="Is the recommendation justified by the constraints?")
    pragmatism: int = Field(ge=1, le=5, description="Does it name real trade-offs (not dogma)?")
    overall: int = Field(ge=1, le=5)
    comment: str = ""


JUDGE_SYSTEM = (
    "You are a Principal Engineer grading an architecture-decision write-up. Given the DECISION, the "
    "OPTIONS and the ADVICE (analysis + recommendation), score analysis_quality, whether the "
    "recommendation is sound given the stated constraints, and pragmatism (names real trade-offs). "
    "Integer scores 1-5."
)


def grade(result: AdrResult, settings: Settings, client: LLMClient | None = None) -> AdviceGrade:
    client = client or LLMClient(settings)
    a = result.advice
    analyses = "\n".join(f"- {o.option}: +{o.pros} / -{o.cons}" for o in a.option_analyses)
    user = (
        f"DECISION: {result.decision}\nOPTIONS: {result.options}\n\n"
        f"ANALYSES:\n{analyses}\n\nRECOMMENDATION: {a.recommendation.option} — {a.recommendation.rationale}"
    )
    return client.structured(schema=AdviceGrade, system=JUDGE_SYSTEM, user=user, model=settings.judge_model)
