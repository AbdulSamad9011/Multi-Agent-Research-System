"""Live web search tool for sub-agents.

Requires TAVILY_API_KEY in the environment. Swap for another provider
(Bing, Serper, Exa, ...) if preferred — just keep the factory-function
shape so graph.py doesn't need to change.
"""
from __future__ import annotations

from langchain_tavily import TavilySearch

from research_agent.config import settings


def build_web_search_tool() -> TavilySearch:
    return TavilySearch(max_results=settings.tavily_max_results, topic="general")
