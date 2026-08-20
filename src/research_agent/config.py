"""Central configuration for models, providers, and runtime knobs.

All values are env-overridable so the same code runs in dev/prod without
edits. See .env.example for the full list.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load .env here, not in the CLI entrypoint: config.py is imported by
# research_agent.graph (and everything else), and import order must not decide
# whether PLANNER_MODEL/API keys take effect. override=True makes .env
# authoritative over any leftover session/global env var.
load_dotenv(override=True)


@dataclass(frozen=True)
class Settings:
    # "provider:model" strings — anything init_chat_model()/create_agent()
    # accepts. Split by role so you can e.g. run a cheaper model for
    # researchers and a stronger one for planning/summarizing.
    # groq = GROQ_API_KEY, google_genai = GOOGLE_API_KEY.
    # Limit: Groq models cannot combine tools+structured output and are flaky
    # at JSON-schema output, so Google handles planner/researcher; Groq does
    # the (tool-free, unstructured) summarizer. Avoid groq qwen* models — they
    # dump their chain-of-thought into 'content'.
    planner_model: str = os.getenv("PLANNER_MODEL", "google_genai:gemini-3.6-flash")
    researcher_model: str = os.getenv("RESEARCHER_MODEL", "google_genai:gemini-3.6-flash")
    summarizer_model: str = os.getenv("SUMMARIZER_MODEL", "groq:openai/gpt-oss-120b")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "google_genai:gemini-embedding-2")

    # Researcher branches fan out in parallel. Google free tier caps each model
    # at ~5 req/min and ~20 req/day, so branches rotate across these models to
    # spread the load. Comma-separated; first entry is the primary default.
    # (gemini-2.5-flash-lite was removed from Google's lineup — don't list it.)
    researcher_models: tuple[str, ...] = tuple(
        os.getenv(
            "RESEARCHER_MODELS",
            "google_genai:gemini-3.6-flash,google_genai:gemini-3.5-flash,"
            "google_genai:gemini-3.5-flash-lite,google_genai:gemini-3.1-flash-lite",
        ).split(",")
    )

    # Planner rotation: same idea, but ends with a Groq fallback (the planner
    # is tool-free, and Groq's json_schema structured output works even though
    # its function-calling is unreliable).
    planner_models: tuple[str, ...] = tuple(
        os.getenv(
            "PLANNER_MODELS",
            "google_genai:gemini-3.6-flash,google_genai:gemini-3.5-flash,"
            "google_genai:gemini-3.5-flash-lite,google_genai:gemini-3.1-flash-lite,"
            "google_genai:gemini-3.7-flash,groq:openai/gpt-oss-120b",
        ).split(",")
    )

    # Planner is instructed to produce between min and max subtopics.
    min_subagents: int = int(os.getenv("MIN_SUBAGENTS", 3))
    max_subagents: int = int(os.getenv("MAX_SUBAGENTS", 4))

    rag_top_k: int = int(os.getenv("RAG_TOP_K", 5))
    tavily_max_results: int = int(os.getenv("TAVILY_MAX_RESULTS", 5))


settings = Settings()
