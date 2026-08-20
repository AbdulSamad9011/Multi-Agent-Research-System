"""CLI entrypoint: run a single research request end-to-end.

    python -m research_agent.main "your research question here"
"""
from __future__ import annotations

import sys
import uuid

# config.py already loads .env before any research_agent import; keep this
# here only as a safety net (move ABOVE the research_agent import — dotenv
# must run before config.py reads PLANNER_MODEL / API keys).
from dotenv import load_dotenv

load_dotenv()

from research_agent.config import settings
from research_agent.graph import build_graph


def run(query: str, rag_source_dir: str | None = None) -> str:
    graph = build_graph(rag_source_dir=rag_source_dir or settings.rag_source_dir or None)
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    final_state = graph.invoke({"query": query, "research_results": []}, config)
    return final_state["final_report"]


if __name__ == "__main__":
    user_query = " ".join(sys.argv[1:]) or "What is the state of solid-state EV batteries in 2026?"
    print(run(user_query))
