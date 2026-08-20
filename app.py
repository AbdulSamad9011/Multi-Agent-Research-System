"""Streamlit frontend for the multi-agent research system.

Run with:  streamlit run app.py

Exposes the pipeline (planner -> parallel researcher sub-agents using RAG +
live web search -> summarizer) as an interactive page, with live node-level
progress, the research plan, per-subagent findings, and the final report.

Design notes for resiliency:
- A failed researcher branch never aborts the run (it returns a "failed"
  findings entry); a planner/summarizer failure is surfaced as an error but
  any partial results already collected are still rendered.
- Results are persisted in `st.session_state["result"]`, so toggling sidebar
  widgets (which trigger script reruns) cannot wipe the last report.
- Runtime knobs in the sidebar override the frozen `Settings` dataclass for
  the current run only (object.__setattr__).
"""
from __future__ import annotations

import time
import uuid

import streamlit as st

st.set_page_config(page_title="Multi-Agent Research Studio", page_icon=":material/science:", layout="wide")

# Trigger .env load (config.py holds the load_dotenv(override=True) logic).
from research_agent.config import settings  # noqa: E402
from research_agent.graph import build_graph  # noqa: E402
from research_agent.state import ResearchPlan, SubAgentFindings  # noqa: E402


def _apply_overrides() -> None:
    """Push sidebar runtime knobs into the frozen Settings for this run."""
    object.__setattr__(settings, "min_subagents", int(st.session_state["min_subagents"]))
    object.__setattr__(settings, "max_subagents", int(st.session_state["max_subagents"]))
    object.__setattr__(settings, "rag_top_k", int(st.session_state["top_k"]))
    object.__setattr__(settings, "tavily_max_results", int(st.session_state["tavily"]))


def _empty_result() -> dict:
    return {
        "log": [],
        "plan": None,
        "role_by_id": {},
        "findings": [],
        "report": None,
        "error": None,
        "elapsed": None,
    }


def _render_plan(plan: ResearchPlan) -> None:
    st.subheader("Research plan")
    st.markdown(f"**Restated goal:** {plan.restated_goal}")
    for sub in plan.subtopics:
        st.markdown(f"- **`{sub.id}`** {sub.title} — *{sub.role}* — {sub.objective}")


def _render_findings(findings: list, role_by_id: dict) -> None:
    if not findings:
        return
    st.subheader("Per-sub-agent findings")
    for f in findings:
        title = f.title or role_by_id.get(f.subtopic_id, "Untitled") or "Untitled"
        role = role_by_id.get(f.subtopic_id, "n/a")
        with st.expander(f"{title} — *{role}*", expanded=False):
            st.markdown(f"Confidence: **{f.confidence:.0%}**")
            st.markdown("**Key findings**")
            for point in f.key_findings:
                st.markdown(f"- {point}")
            if f.sources:
                st.markdown("**Sources:** " + ", ".join(f.sources))
            if f.raw_notes:
                with st.popover("Raw notes"):
                    st.code(f.raw_notes, language="markdown")


def _render_report(report: str) -> None:
    st.subheader("Final report")
    st.markdown(report)


def _run(query: str, rag_dir: str | None) -> dict:
    """Execute the graph, streaming node-level progress. Never raises."""
    result = _empty_result()
    _apply_overrides()

    progress = st.container(border=True)
    status = progress.empty()

    def say(line: str) -> None:
        result["log"].append(line)
        status.markdown("\n".join(result["log"]))

    try:
        graph = build_graph(rag_source_dir=rag_dir)
        started = time.time()
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}

        for update in graph.stream(
            {"query": query, "research_results": []}, config, stream_mode="updates"
        ):
            for node, payload in update.items():
                if node == "planner" and isinstance(payload.get("plan"), ResearchPlan):
                    result["plan"] = payload["plan"]
                    say(f"Planned {len(result['plan'].subtopics)} subtopics")
                elif node == "researcher":
                    for f in payload.get("research_results", []):
                        say(f"Finished researcher - {f.title}")
                        result["findings"].append(f)
                elif node == "summarizer":
                    result["report"] = payload.get("final_report")

        result["elapsed"] = time.time() - started
        if result["plan"]:
            result["role_by_id"] = {s.id: s.role for s in result["plan"].subtopics}
        say(f"Report ready in {result['elapsed']:.0f}s")
    except Exception as exc:  # noqa: BLE001 - record and render partial results
        result["error"] = f"{type(exc).__name__}: {exc}"
        say(f"Failed: {result['error']}")
    return result


def _render_result(result: dict) -> None:
    if result["error"]:
        st.error(f"Run ended with an error: {result['error']}")
    if result["plan"]:
        _render_plan(result["plan"])
    _render_findings(result["findings"], result["role_by_id"])
    if result["report"]:
        _render_report(result["report"])
    elif not result["error"]:
        st.warning("No report was produced (the sub-agents returned nothing usable).")

    with st.expander("Run log"):
        for line in result["log"]:
            st.write(line)


# --- Sidebar -----------------------------------------------------------------
with st.sidebar:
    st.header("Runtime knobs")
    st.text_input(
        "RAG knowledge-base dir",
        key="rag_dir",
        placeholder="e.g. ./kb - leave empty to use web only",
        help="Folder of .txt/.md files seeded into the in-memory vector store.",
    )
    st.number_input("Min sub-agents", 1, 8, int(settings.min_subagents), key="min_subagents")
    st.number_input("Max sub-agents", 1, 8, int(settings.max_subagents), key="max_subagents")
    st.slider("RAG top-k", 1, 20, int(settings.rag_top_k), key="top_k")
    st.slider("Web results per search", 1, 10, int(settings.tavily_max_results), key="tavily")

    st.divider()
    st.caption("Model rotation (researchers)")
    st.code("\n".join(settings.researcher_models), language="text")
    st.caption("Extractor")
    st.code("\n".join(settings.extractor_models), language="text")


# --- Main --------------------------------------------------------------------
st.title("Multi-Agent Research Studio")
st.caption(
    "**planner** to **parallel researcher sub-agents** (knowledge base + live web search) to **summarizer**"
)

query = st.text_area(
    "Research question",
    placeholder="e.g. Summarize one paper on Brain Tumor",
    height=110,
)
run_clicked = st.button(
    "Run research", type="primary", use_container_width=True, disabled=not query.strip()
)

if run_clicked:
    rag_dir = (st.session_state.get("rag_dir") or "").strip() or None
    with st.spinner("Running the research agents..."):
        result = _run(query.strip(), rag_dir)
    st.session_state["result"] = result
    _render_result(result)
elif "result" in st.session_state:
    st.caption("Showing last run. Change the query and hit **Run research** for a new one.")
    _render_result(st.session_state["result"])