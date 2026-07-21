"""decision + options -> structured trade-off analysis + a recommendation from the given options.

Safety guarantee: the recommendation is validated against the supplied options (case-insensitive).
If the model recommends something not offered, `recommendation_valid` is False and the option is
normalised to the closest supplied name where possible — so a recommendation is always one of the
options the user actually asked about.
"""

from __future__ import annotations

from . import prompts
from .client import LLMClient
from .models import AdrResult, Advice


def _match(option: str, options: list[str]) -> str | None:
    o = option.strip().lower()
    for opt in options:
        if opt.strip().lower() == o:
            return opt
    # loose containment (e.g. "SQS FIFO" vs "SQS (FIFO)")
    for opt in options:
        if o and (o in opt.lower() or opt.lower() in o):
            return opt
    return None


class Advisor:
    def __init__(self, client: LLMClient) -> None:
        self._client = client

    def advise(self, decision: str, options: list[str]) -> AdrResult:
        advice = self._client.structured(
            schema=Advice,
            system=prompts.ADVISOR_SYSTEM,
            user=prompts.advisor_user(decision, options),
        )
        matched = _match(advice.recommendation.option, options)
        valid = matched is not None
        if matched:  # normalise to the exact supplied option name
            advice = advice.model_copy(
                update={"recommendation": advice.recommendation.model_copy(update={"option": matched})}
            )
        return AdrResult(decision=decision, options=options, advice=advice, recommendation_valid=valid)
