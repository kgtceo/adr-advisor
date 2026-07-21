"""Typed contracts for adr-advisor.

Given a decision context and a set of candidate OPTIONS, the advisor analyses each option,
builds a trade-off view across the axes a Staff Engineer weighs, and recommends ONE of the
given options. Safety guarantee (enforced in advisor.py): the recommendation must be one of
the options the user supplied — the model can't invent a new one.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

AXES = ["scalability", "reliability", "cost", "operability", "maintainability"]


class OptionAnalysis(BaseModel):
    option: str = Field(description="The option name, exactly as given.")
    pros: list[str] = Field(default_factory=list)
    cons: list[str] = Field(default_factory=list)
    notable_for: str = Field(description="One line: what this option is strongest at.")


class TradeOff(BaseModel):
    axis: str = Field(description="scalability | reliability | cost | operability | maintainability")
    favoured_option: str = Field(description="Which option is strongest on this axis (one of the given).")
    note: str = Field(description="Why — the trade-off in one line.")


class Recommendation(BaseModel):
    option: str = Field(description="The recommended option — MUST be one of the given options.")
    rationale: str = Field(description="Why this one, given the context and constraints.")
    key_risks: list[str] = Field(default_factory=list, description="The trade-offs you're accepting.")
    revisit_when: str = Field(description="The signal that should make you reconsider this decision.")


class Advice(BaseModel):
    """The advisor's structured output (the tool schema handed to Claude)."""

    context_summary: str = Field(description="1–2 sentences restating the decision and key constraints.")
    option_analyses: list[OptionAnalysis] = Field(default_factory=list)
    trade_offs: list[TradeOff] = Field(default_factory=list)
    recommendation: Recommendation


class AdrResult(BaseModel):
    """Everything returned for one decision — the advice plus a validity flag on the recommendation."""

    decision: str
    options: list[str]
    advice: Advice
    recommendation_valid: bool = Field(
        description="True iff the recommended option is one of the supplied options (never invented)."
    )
