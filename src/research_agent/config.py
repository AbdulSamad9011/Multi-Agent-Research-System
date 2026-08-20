"""Central configuration for models, providers, and runtime knobs.

All values are env-overridable so the same code runs in dev/prod without
edits. See .env.example for the full list.
"""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    # "provider:model" strings — anything init_chat_model()/create_agent()
    # accepts. Split by role so you can e.g. run a cheaper model for
    # researchers and a stronger one for planning/summarizing.
    planner_model: str = os.getenv("PLANNER_MODEL", "anthropic:claude-sonnet-4-6")
    researcher_model: str = os.getenv("RESEARCHER_MODEL", "anthropic:claude-sonnet-4-6")
    summarizer_model: str = os.getenv("SUMMARIZER_MODEL", "anthropic:claude-sonnet-4-6")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "openai:text-embedding-3-small")

    # Planner is instructed to produce between min and max subtopics.
    min_subagents: int = int(os.getenv("MIN_SUBAGENTS", 3))
    max_subagents: int = int(os.getenv("MAX_SUBAGENTS", 4))

    rag_top_k: int = int(os.getenv("RAG_TOP_K", 5))
    tavily_max_results: int = int(os.getenv("TAVILY_MAX_RESULTS", 5))


settings = Settings()
