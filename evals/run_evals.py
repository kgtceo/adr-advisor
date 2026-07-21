"""Run the adr-advisor eval suite.

Gates:
  • VALID-RECOMMENDATION — the recommendation is always one of the supplied options (never invented).
  • COMPLETE — every supplied option is analysed; trade-offs cover the axes.
  • AVOIDS-BAD-OPTION — it doesn't recommend an option that's clearly wrong given the constraints.
  • JUDGE — opus scores analysis quality / soundness / pragmatism.

    python evals/run_evals.py [--no-judge]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from anthropic import Anthropic

from adr_advisor.advisor import Advisor
from adr_advisor.client import LLMClient
from adr_advisor.config import Settings

from metrics import (  # noqa: E402
    all_options_analysed,
    avoided_bad_option,
    recommendation_is_valid,
    trade_offs_cover_axes,
)

DATASET = Path(__file__).parent / "dataset" / "cases.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-judge", action="store_true")
    args = ap.parse_args()

    settings = Settings.from_env()
    anthropic = Anthropic(api_key=settings.anthropic_api_key)
    client = LLMClient(settings, anthropic)
    advisor = Advisor(client)
    cases = json.loads(DATASET.read_text())

    failures: list[str] = []
    grades = []
    for case in cases:
        result = advisor.advise(case["decision"], case["options"])
        rec = result.advice.recommendation.option
        print(f"\n=== {case['name']} ===")
        print(f"  recommended={rec!r} valid={result.recommendation_valid}")

        if not recommendation_is_valid(result):
            failures.append(f"{case['name']}: recommended an option not in the list ({rec!r})")
        if not all_options_analysed(result):
            failures.append(f"{case['name']}: didn't analyse every option")
        if not trade_offs_cover_axes(result):
            failures.append(f"{case['name']}: trade-offs don't cover enough axes")
        if not avoided_bad_option(result, case.get("must_not_recommend", [])):
            failures.append(f"{case['name']}: recommended a clearly-wrong option ({rec!r})")

        if not args.no_judge:
            from judge import grade  # noqa: E402

            g = grade(result, settings, client)
            grades.append(g)
            print(f"  JUDGE: analysis={g.analysis_quality} sound={g.recommendation_sound} pragmatism={g.pragmatism} overall={g.overall}")

    if grades:
        n = len(grades)
        print(f"\n=== Judge avg === overall={sum(g.overall for g in grades)/n:.2f} "
              f"sound={sum(g.recommendation_sound for g in grades)/n:.2f}")

    print("\n" + "=" * 40)
    if failures:
        print(f"FAILED ({len(failures)}):")
        for f in failures:
            print(f"  ✗ {f}")
        return 1
    print("ALL GATES PASSED ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
