"""Core offline tests — recommendation validation + normalisation to a supplied option."""

from __future__ import annotations

from conftest import FakeClient

from adr_advisor.advisor import Advisor
from adr_advisor.models import Advice, OptionAnalysis, Recommendation, TradeOff


def _advice(rec_option: str) -> Advice:
    return Advice(
        context_summary="ctx",
        option_analyses=[OptionAnalysis(option="SQS FIFO", pros=["ordering"], cons=[], notable_for="ordering")],
        trade_offs=[TradeOff(axis="cost", favoured_option="SQS FIFO", note="cheap")],
        recommendation=Recommendation(option=rec_option, rationale="r", key_risks=["k"], revisit_when="w"),
    )


def test_valid_recommendation_from_options():
    result = Advisor(FakeClient(_advice("SQS FIFO"))).advise("d", ["SQS FIFO", "Kinesis"])
    assert result.recommendation_valid is True
    assert result.advice.recommendation.option == "SQS FIFO"


def test_invented_option_flagged_invalid():
    result = Advisor(FakeClient(_advice("RabbitMQ"))).advise("d", ["SQS FIFO", "Kinesis"])
    assert result.recommendation_valid is False


def test_loose_name_is_normalised_to_supplied():
    # model returns "SQS" but the supplied option is "SQS FIFO" → normalise to the supplied name.
    result = Advisor(FakeClient(_advice("SQS"))).advise("d", ["SQS FIFO", "Kinesis"])
    assert result.recommendation_valid is True
    assert result.advice.recommendation.option == "SQS FIFO"


def test_case_insensitive_match():
    result = Advisor(FakeClient(_advice("kinesis"))).advise("d", ["SQS FIFO", "Kinesis"])
    assert result.recommendation_valid is True
    assert result.advice.recommendation.option == "Kinesis"
