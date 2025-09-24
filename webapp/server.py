"""FastAPI server exposing the Aenon agent as a web application."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from core.aenon import GoalDescriptor
from core.bootstrap import bootstrap_aenon

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"

app = FastAPI(title="Aenon", description="Reflective AGI demonstration", version="1.0.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

aenon = bootstrap_aenon()


class GoalRequest(BaseModel):
    domain: str
    description: str
    constraints: List[str] = Field(default_factory=list)
    success_metrics: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FeedbackRequest(BaseModel):
    message: str
    source: str = "user"


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/api/capabilities")
async def list_capabilities() -> Dict[str, Dict[str, str]]:
    return {"capabilities": aenon.describe_capabilities()}


@app.get("/api/memory")
async def recent_memory(limit: int = 10) -> Dict[str, Any]:
    if not aenon.memory:
        return {"entries": []}
    return {"entries": aenon.memory.recent(limit)}


@app.post("/api/goals")
async def submit_goal(request: GoalRequest) -> Dict[str, Any]:
    try:
        goal = GoalDescriptor(
            domain=request.domain,
            description=request.description,
            constraints=request.constraints,
            success_metrics=request.success_metrics,
            metadata=request.metadata,
        )
    except TypeError as exc:  # pragma: no cover - defensive guard
        raise HTTPException(status_code=400, detail=str(exc))

    report = aenon.execute_goal(goal)
    return report.to_dict()


@app.post("/api/feedback")
async def submit_feedback(request: FeedbackRequest) -> Dict[str, str]:
    capability = aenon.get_capability("human_ai")
    if capability is None:
        raise HTTPException(status_code=404, detail="Human collaboration capability is not available")

    capability.record_feedback(request.message, {"source": request.source})
    return {"status": "recorded"}
