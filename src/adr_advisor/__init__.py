"""adr-advisor — an architecture-decision trade-off advisor.

Give it a decision (with constraints) and a set of candidate options; it analyses each option
across scalability, reliability, cost, operability and maintainability, and recommends one of the
given options — never an invented one — with the trade-off it's accepting and when to revisit."""

from .advisor import Advisor
from .client import LLMClient
from .config import Settings
from .models import AdrResult, Advice, OptionAnalysis, Recommendation, TradeOff

__all__ = [
    "Advisor",
    "LLMClient",
    "Settings",
    "AdrResult",
    "Advice",
    "OptionAnalysis",
    "Recommendation",
    "TradeOff",
]
