"""Summarizer node: synthesizes all sub-agent findings into one report."""
from __future__ import annotations

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

from research_agent.config import settings
from research_agent.state import ResearchState

_SUMMARIZER_SYSTEM_PROMPT = """You are the lead researcher producing the \
final deliverable for a research request.

You will be given the original question, the research plan, and the \
findings gathered by each specialist sub-agent. Your job:

1. Resolve conflicts/contradictions between sub-agents explicitly.
2. Extract only the relevant, non-redundant, well-evidenced findings.
3. Organize the answer by theme, not by which sub-agent found it.
4. Include an inline citation (source URL/doc id) for every claim.
5. End with a short 'Open questions / gaps' section if evidence was thin \
anywhere.

Write in clear markdown."""


def build_summarizer():
    model = init_chat_model(settings.summarizer_model)

    def summarizer_node(state: ResearchState) -> dict:
        plan = state["plan"]
        role_by_id = {sub.id: sub.role for sub in plan.subtopics}

        findings_blob = "\n\n".join(
            f"### {f.title} (role: {role_by_id.get(f.subtopic_id, 'n/a')})\n"
            f"Confidence: {f.confidence}\n"
            + "\n".join(f"- {point}" for point in f.key_findings)
            + "\nSources: " + ", ".join(f.sources)
            for f in state["research_results"]
        )

        response = model.invoke(
            [
                SystemMessage(content=_SUMMARIZER_SYSTEM_PROMPT),
                HumanMessage(
                    content=(
                        f"Original question: {state['query']}\n\n"
                        f"Restated goal: {plan.restated_goal}\n\n"
                        f"Sub-agent findings:\n\n{findings_blob}"
                    )
                ),
            ]
        )

        return {"final_report": response.content}

    return summarizer_node
