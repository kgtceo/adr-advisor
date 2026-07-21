"""Deterministic eval metrics over an AdrResult."""

from __future__ import annotations

from adr_advisor.models import AXES, AdrResult


def recommendation_is_valid(result: AdrResult) -> bool:
    """The recommended option is one of the supplied options (never invented) — core guarantee."""
    return result.recommendation_valid


def all_options_analysed(result: AdrResult) -> bool:
    """Every supplied option got an analysis (case-insensitive match)."""
    analysed = {a.option.strip().lower() for a in result.advice.option_analyses}
    given = {o.strip().lower() for o in result.options}
    return given.issubset(analysed)


def trade_offs_cover_axes(result: AdrResult, min_axes: int = 3) -> bool:
    """The trade-off view touches at least `min_axes` of the standard axes."""
    axes = {t.axis.strip().lower() for t in result.advice.trade_offs}
    return len(axes & set(AXES)) >= min_axes


def avoided_bad_option(result: AdrResult, must_not: list[str]) -> bool:
    """The recommendation is NOT one of the options that are clearly wrong given the constraints."""
    rec = result.advice.recommendation.option.strip().lower()
    return rec not in {m.strip().lower() for m in must_not}
