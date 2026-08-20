"""Sub-agent factory: a create_agent-based researcher with RAG + web tools.

Each parallel branch (see graph.py::route_to_researchers) invokes this
node with its own ResearcherTask. A fresh `create_agent` instance is
built per call so the system prompt can be specialized to that
subtopic's role/objective; the underlying tool set is shared and passed
in from graph.py.
"""
from __future__ import annotations

from typing import List

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool

from research_agent.config import settings
from research_agent.state import ResearcherTask, SubAgentFindings

_RESEARCHER_SYSTEM_PROMPT = """You are a {role} research specialist working \
as part of a larger research team.

Your objective for this sub-task: {objective}

Use the available tools (internal knowledge base + live web search) to \
gather evidence. Prefer the knowledge base first, then the web. Be \
skeptical of single-source claims and note disagreement between sources \
when it exists. Cite the URL or doc id for every finding. Stop once you \
have enough evidence to answer the objective — do not over-research."""


def build_researcher_node(tools: List[BaseTool]):
    """Factory for the `researcher` graph node.

    `tools` (e.g. [rag_tool, web_search_tool]) is shared across every
    parallel researcher branch. TODO: give different roles different
    toolsets (e.g. only 'academic-literature' gets an arXiv tool) by
    branching on `subtopic.role` here instead of using one shared list.
    """

    def researcher_node(task: ResearcherTask) -> dict:
        subtopic = task["subtopic"]

        agent = create_agent(
            model=settings.researcher_model,
            tools=tools,
            system_prompt=_RESEARCHER_SYSTEM_PROMPT.format(
                role=subtopic.role, objective=subtopic.objective
            ),
            response_format=SubAgentFindings,
            name=f"researcher-{subtopic.id}",
        )

        result = agent.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=(
                            f"Overall research question: {task['query']}\n"
                            f"Your subtopic: {subtopic.title}"
                        )
                    )
                ]
            }
        )

        findings: SubAgentFindings = result["structured_response"]
        findings.subtopic_id = subtopic.id  # guard against model drift
        return {"research_results": [findings]}

    return researcher_node
