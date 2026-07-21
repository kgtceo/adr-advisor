"""`adr-advisor` CLI — weigh an architecture decision across the trade-off axes.

    adr-advisor advise --decision "Queue between order & email svc; need per-user ordering, small team" \
                       --option "SQS FIFO" --option "Kinesis" --option "EventBridge" --option "Kafka (MSK)"
    adr-advisor demo
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .advisor import Advisor
from .client import LLMClient
from .config import Settings

app = typer.Typer(add_completion=False, help="Architecture-decision trade-off advisor (recommends one of your options).")
console = Console()

_DEMO_DECISION = (
    "We need a queue between the order service and the email/notification sender. Constraints: "
    "per-user ordering matters, at-least-once delivery is fine, ~1,000 messages/sec, a small team "
    "with limited ops capacity, and we're already all-in on AWS serverless."
)
_DEMO_OPTIONS = ["SQS FIFO", "Kinesis", "EventBridge", "Kafka (MSK)"]


def _print(result) -> None:
    a = result.advice
    console.print(Panel(a.context_summary, title="Decision", border_style="cyan"))

    t = Table(title="Trade-offs")
    t.add_column("Axis"); t.add_column("Favoured"); t.add_column("Note")
    for to in a.trade_offs:
        t.add_row(to.axis, to.favoured_option, to.note)
    console.print(t)

    for oa in a.option_analyses:
        console.print(f"\n[bold]{oa.option}[/] — [dim]{oa.notable_for}[/]")
        for p in oa.pros:
            console.print(f"  [green]+[/] {p}")
        for c in oa.cons:
            console.print(f"  [red]−[/] {c}")

    rec = a.recommendation
    flag = "" if result.recommendation_valid else " [red](⚠ not one of the given options)[/]"
    console.print(Panel(
        f"[bold]{rec.option}[/]{flag}\n\n{rec.rationale}\n\n"
        f"[dim]Risks:[/] {'; '.join(rec.key_risks) or '—'}\n[dim]Revisit when:[/] {rec.revisit_when}",
        title="Recommendation", border_style="green"))


def _run(decision: str, options: list[str]) -> None:
    settings = Settings.from_env()
    advisor = Advisor(LLMClient(settings))
    with console.status("Weighing the options…"):
        result = advisor.advise(decision, options)
    _print(result)


@app.callback()
def _root() -> None:
    """Architecture-decision trade-off advisor."""


@app.command()
def advise(
    decision: str = typer.Option(..., "--decision", help="The decision + any constraints."),
    option: list[str] = typer.Option(..., "--option", help="A candidate option (repeat for each)."),
) -> None:
    if len(option) < 2:
        console.print("[red]Give at least two --option values to compare.[/]")
        raise typer.Exit(1)
    _run(decision, option)


@app.command()
def demo() -> None:
    """Weigh a baked-in decision (queue choice for a small serverless team)."""
    _run(_DEMO_DECISION, _DEMO_OPTIONS)


if __name__ == "__main__":
    app()
