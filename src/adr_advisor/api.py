"""FastAPI wrapper: submit a decision + options → trade-off analysis + a recommendation."""

from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .advisor import Advisor
from .config import Settings
from .models import AdrResult

app = FastAPI(title="adr-advisor", version="1.0.0")

_env_origins = [o.strip() for o in os.getenv("AD_CORS_ORIGINS", "").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_env_origins,
    allow_origin_regex=r"https://adr-advisor[a-z0-9-]*\.vercel\.app|http://(localhost|127\.0\.0\.1):\d+",
    allow_methods=["*"],
    allow_headers=["*"],
)

_EXAMPLE = {
    "decision": (
        "We need a queue between the order service and the email/notification sender. Constraints: "
        "per-user ordering matters, at-least-once delivery is fine, ~1,000 messages/sec, a small "
        "team with limited ops capacity, and we're already all-in on AWS serverless."
    ),
    "options": ["SQS FIFO", "Kinesis", "EventBridge", "Kafka (MSK)"],
}


class AdviseRequest(BaseModel):
    decision: str = Field(..., min_length=10, max_length=5000)
    options: list[str] = Field(..., min_length=2, max_length=8)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/example")
def example() -> dict:
    return _EXAMPLE


@app.post("/api/advise")
def advise(req: AdviseRequest) -> AdrResult:
    opts = [o.strip() for o in req.options if o.strip()]
    if len(opts) < 2:
        raise HTTPException(status_code=400, detail="Provide at least two options.")
    try:
        settings = Settings.from_env()
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    from .client import LLMClient

    return Advisor(LLMClient(settings)).advise(req.decision, opts)
