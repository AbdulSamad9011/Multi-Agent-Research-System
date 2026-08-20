"""Wraps the RAG vector store as a LangChain tool the sub-agents can call."""
from __future__ import annotations

from langchain_core.tools import BaseTool
from langchain_core.tools.retriever import create_retriever_tool
from langchain_core.vectorstores import InMemoryVectorStore

from research_agent.config import settings


def build_rag_tool(vectorstore: InMemoryVectorStore) -> BaseTool:
    retriever = vectorstore.as_retriever(search_kwargs={"k": settings.rag_top_k})
    return create_retriever_tool(
        retriever,
        name="knowledge_base_search",
        description=(
            "Search the internal knowledge base (ingested documents, prior "
            "research notes) for passages relevant to a query. Prefer this "
            "before web_search for anything that might already be in the "
            "corpus — it's cheaper and more trustworthy than the open web."
        ),
    )
