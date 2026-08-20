"""Shared graph state schema.

`ResearchState` is the top-level state threaded through the whole graph.
`ResearcherTask` is the *per-branch* payload dispatched to each parallel
sub-agent via `Send` — it deliberately carries only what that branch
needs, not the full graph state.
"""
from __future__ import annotations

import operator
from typing import Annotated, List, Optional, TypedDict

from pydantic import BaseModel, Field


class SubTopic(BaseModel):
    """One slice of the research plan, assigned to one sub-agent."""

    id: str = Field(description="Short stable id, e.g. 'sub-1'")
    title: str = Field(description="Short human-readable title")
    role: str = Field(
        description=(
            "Specialist persona for this sub-agent, e.g. 'market-analyst', "
            "'technical', 'competitive-landscape', 'academic-literature', "
            "'regulatory-legal', 'news-current-events'."
        )
    )
    objective: str = Field(description="What this sub-agent must find out")


class ResearchPlan(BaseModel):
    """Structured output of the planner node."""

    restated_goal: str = Field(description="Planner's restatement of the user's research goal")
    subtopics: List[SubTopic]


class SubAgentFindings(BaseModel):
    """Structured output each sub-agent (researcher) must return."""

    subtopic_id: str
    title: str
    key_findings: List[str] = Field(description="Bullet-point findings, each a standalone fact/claim")
    sources: List[str] = Field(default_factory=list, description="URLs / doc ids used as evidence")
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    raw_notes: Optional[str] = Field(
        default=None, description="Free-form notes / agent transcript, useful for debugging"
    )


class ResearcherTask(TypedDict):
    """Input payload for a single parallel researcher branch (via Send)."""

    query: str
    subtopic: SubTopic


class ResearchState(TypedDict):
    """Top-level graph state."""

    query: str
    plan: Optional[ResearchPlan]
    # Each parallel researcher branch returns exactly one item here;
    # operator.add concatenates them as branches complete (fan-in).
    research_results: Annotated[List[SubAgentFindings], operator.add]
    final_report: Optional[str]
