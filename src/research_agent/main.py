"""CLI entrypoint: run a single research request end-to-end.

    python -m research_agent.main "your research question here"
"""
from __future__ import annotations

import sys
import uuid

from dotenv import load_dotenv

from research_agent.graph import build_graph

load_dotenv()


def run(query: str, rag_source_dir: str | None = None) -> str:
    graph = build_graph(rag_source_dir=rag_source_dir)
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    final_state = graph.invoke({"query": query, "research_results": []}, config)
    return final_state["final_report"]


if __name__ == "__main__":
    user_query = " ".join(sys.argv[1:]) or "What is the state of solid-state EV batteries in 2026?"
    print(run(user_query))
