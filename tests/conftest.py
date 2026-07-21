"""Offline test doubles — no API key, no network."""

from __future__ import annotations

import pytest

from adr_advisor.config import Settings
from adr_advisor.models import Advice


class FakeClient:
    """Returns a scripted Advice, so the advisor's validation/normalisation is exercisable offline."""

    def __init__(self, advice: Advice) -> None:
        self._advice = advice
        self.calls = 0

    def structured(self, *, schema, system, user, model=None):
        self.calls += 1
        return self._advice


@pytest.fixture
def settings() -> Settings:
    return Settings(anthropic_api_key="test-key")
