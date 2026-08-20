"""Wires planner -> parallel researchers -> summarizer into a LangGraph graph."""
from __future__ import annotations

from typing import List, Optional, Union

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from research_agent.agents.planner import build_planner
from research_agent.agents.researcher import build_researcher_node
from research_agent.agents.summarizer import build_summarizer
from research_agent.rag.ingest import build_vectorstore
from research_agent.rag.retriever_tool import build_rag_tool
from research_agent.state import ResearcherTask, ResearchState
from research_agent.tools.web_search import build_web_search_tool


def route_to_researchers(state: ResearchState) -> List[Send]:
    """Fan-out: dynamically dispatch one `researcher` branch per subtopic.

    Returning a list[Send] instead of a plain node name tells LangGraph
    to run the `researcher` node once per Send, concurrently (same
    superstep), each with its own slice of state (a ResearcherTask)
    instead of the full graph state.
    """
    plan = state["plan"]
    return [
        Send("researcher", ResearcherTask(query=state["query"], subtopic=sub))
        for sub in plan.subtopics
    ]


def build_graph(
    *,
    rag_source_dir: Optional[str] = None,
    checkpointer: Optional[object] = None,
):
    """Build and compile the research graph.

    rag_source_dir: optional folder to seed the RAG index from (see
        rag/ingest.py). Pass None to run with an empty knowledge base
        (researchers will then lean on web_search).
    checkpointer: pass InMemorySaver()/PostgresSaver()/etc. for
        persistence + resumability. Defaults to InMemorySaver() — swap
        for a durable backend before production use.
    """
    vectorstore = build_vectorstore(rag_source_dir)
    shared_tools = [build_rag_tool(vectorstore), build_web_search_tool()]

    builder = StateGraph(ResearchState)
    builder.add_node("planner", build_planner())
    builder.add_node("researcher", build_researcher_node(shared_tools))
    builder.add_node("summarizer", build_summarizer())

    builder.add_edge(START, "planner")
    builder.add_conditional_edges("planner", route_to_researchers, ["researcher"])
    builder.add_edge("researcher", "summarizer")
    builder.add_edge("summarizer", END)

    return builder.compile(checkpointer=checkpointer or InMemorySaver())
