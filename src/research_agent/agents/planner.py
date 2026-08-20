"""Planner node: turns the user query into a ResearchPlan (3-4 subtopics).

Deliberately a plain structured-output LLM call rather than a tool-calling
agent — planning doesn't need tools, just good decomposition.
"""
from __future__ import annotations

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

from research_agent.config import settings
from research_agent.state import ResearchPlan, ResearchState

_PLANNER_SYSTEM_PROMPT = """You are the lead researcher on a team of specialist \
research agents. Given a user's research question, break it into {min_n}-{max_n} \
independent, non-overlapping subtopics that together cover the question well.

For each subtopic, assign it to the specialist role best suited to it (e.g. \
'market-analyst', 'technical', 'competitive-landscape', 'academic-literature', \
'regulatory-legal', 'news-current-events' — invent roles as needed for the \
question at hand).

Subtopics must be genuinely parallelizable: no subtopic should depend on \
another subtopic's findings to be researched.""".format(
    min_n=settings.min_subagents, max_n=settings.max_subagents
)


def build_planner():
    model = init_chat_model(settings.planner_model)
    structured_model = model.with_structured_output(ResearchPlan)

    def planner_node(state: ResearchState) -> dict:
        plan: ResearchPlan = structured_model.invoke(
            [
                SystemMessage(content=_PLANNER_SYSTEM_PROMPT),
                HumanMessage(content=state["query"]),
            ]
        )
        return {"plan": plan}

    return planner_node
