"""Researcher: manual tool-calling loop + structured extraction pass.

create_agent(response_format=...) forces tool_choice="any" (langchain agents
factory.py:1419), which Groq doesn't support. So we bind tools plainly, loop
until the model answers, and normalize the final text into SubAgentFindings
with a separate extraction call (Groq json_schema). Rotation happens on every
step; `start_index` staggers parallel branches.
"""
from __future__ import annotations

from typing import List

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import BaseTool

from research_agent.agents._retry import call_with_model_rotation
from research_agent.config import build_chat_model, settings
from research_agent.state import ResearcherTask, SubAgentFindings

_MAX_TOOL_STEPS = 6

_RESEARCHER_SYSTEM_PROMPT = """You are a {role} research specialist working \
as part of a larger research team.

Your objective for this sub-task: {objective}

Use the available tools (internal knowledge base + live web search) to \
gather evidence. Prefer the knowledge base first, then the web. Be \
skeptical of single-source claims and note disagreement between sources \
when it exists. Cite the URL or doc id for every finding.

When you have enough evidence, STOP calling tools and write your final \
findings as plain markdown text: a short title, bullet-point findings, a \
'Sources:' line with every URL/doc id used, and a confidence score 0-1. \
Do not invent sources you did not actually use."""

_EXTRACTOR_SYSTEM_PROMPT = """You are a strict data extractor. Convert the \
researcher's final markdown notes into the requested JSON schema.

- `title`: short human-readable title of the findings.
- `key_findings`: discrete, standalone claims (one fact each).
- `sources`: every URL / doc id the researcher cited. Emit them exactly as \
written. Empty list if the text cites nothing.
- `confidence`: 0-1 estimate of how well-evidenced the findings are.
- `raw_notes`: keep the researcher's text verbatim.

Do not add findings that are not in the text, and do not invent sources."""


def build_researcher_node(tools: List[BaseTool]):
    """Factory for the `researcher` graph node (see module docstring)."""

    tool_by_name = {t.name: t for t in tools}

    def researcher_node(task: ResearcherTask) -> dict:
        """Per-branch entry. Never lets one branch's failure abort the run."""
        subtopic = task["subtopic"]
        try:
            return _run_researcher(task)
        except Exception as exc:  # noqa: BLE001 - degrade instead of aborting fan-in
            msg = f"{type(exc).__name__}: {exc}"
            print(f"[researcher] {subtopic.title} FAILED: {msg}")
            return {
                "research_results": [
                    SubAgentFindings(
                        subtopic_id=subtopic.id,
                        title=f"{subtopic.title} (failed)",
                        key_findings=[f"Researcher sub-agent failed: {msg}"],
                        sources=[],
                        confidence=0.0,
                        raw_notes=None,
                    )
                ]
            }

    def _run_researcher(task: ResearcherTask) -> dict:
        subtopic = task["subtopic"]
        messages: list = [
            SystemMessage(
                content=_RESEARCHER_SYSTEM_PROMPT.format(
                    role=subtopic.role, objective=subtopic.objective
                )
            ),
            HumanMessage(
                content=(
                    f"Overall research question: {task['query']}\n"
                    f"Your subtopic: {subtopic.title}"
                )
            ),
        ]

        def build_step(model_str: str):
            return build_chat_model(model_str).bind_tools(list(tools))

        def run_step(bound_model):
            return bound_model.invoke(messages)

        stagager = (
            hash(subtopic.id) % len(settings.researcher_models)
            if len(settings.researcher_models) > 1
            else 0
        )

        for _ in range(_MAX_TOOL_STEPS):
            response: AIMessage = call_with_model_rotation(
                settings.researcher_models,
                build_step,
                run_step,
                max_attempts=8,
                start_index=stagager,
            )
            messages.append(response)
            if not getattr(response, "tool_calls", None):
                break
            for call in response.tool_calls:
                tool = tool_by_name.get(call["name"])
                try:
                    output = tool.invoke(call["args"]) if tool else f"unknown tool: {call['name']}"
                except Exception as exc:  # noqa: BLE001 - surface to the model
                    output = f"tool error: {exc}"
                messages.append(
                    ToolMessage(content=str(output)[:4000], tool_call_id=call["id"])
                )

        final_text = _content_to_text(messages[-1].content if messages else None)
        if not final_text.strip() or len(final_text.strip()) < 20:
            print(f"[researcher] {subtopic.title}: final answer too short ({len(final_text)} chars); "
                  f"wrapping without extraction")
            findings = _fallback_findings(subtopic, final_text)
        else:
            findings = _extract_findings(subtopic, final_text)
        findings.subtopic_id = subtopic.id  # guard against extraction drift
        return {"research_results": [findings]}

    return researcher_node


def _content_to_text(content) -> str:
    """Normalize a message's `content` (str, list of blocks, or None) to text."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))
                elif block.get("type") == "tool_use":
                    parts.append(f"[tool call: {block.get('name', '')}]")
            elif hasattr(block, "text"):
                parts.append(str(block.text))
        return "\n".join(p for p in parts if p)
    if content is None:
        return ""
    return str(content)


def _extract_findings(subtopic, final_text: str) -> SubAgentFindings:
    """Normalize the researcher's text into SubAgentFindings. Never raises;
    on exhaustion/unsupported models it wraps the raw text instead."""
    try:

        def make_structured(model_str: str):
            return build_chat_model(model_str).with_structured_output(
                SubAgentFindings, method="json_schema"
            )

        def invoke_extract(structured_model):
            return structured_model.invoke(
                [
                    SystemMessage(content=_EXTRACTOR_SYSTEM_PROMPT),
                    HumanMessage(
                        content=(
                            f"Subtopic: {subtopic.title}\n\n"
                            f"Researcher notes:\n\n{final_text}"
                        )
                    ),
                ]
            )

        findings = call_with_model_rotation(
            settings.extractor_models, make_structured, invoke_extract
        )
        if isinstance(findings, SubAgentFindings) and _looks_complete(findings):
            return findings
        print(f"[researcher] extraction for {subtopic.title} came back empty/invalid "
              f"(title={getattr(findings, 'title', '?')!r}); wrapping raw notes")
        return _fallback_findings(subtopic, final_text)
    except Exception as exc:  # noqa: BLE001 - never let extraction fail the run
        print(f"[researcher] extraction failed ({type(exc).__name__}: {exc}); "
              f"wrapping raw notes for {subtopic.title}")
        return _fallback_findings(subtopic, final_text)


def _looks_complete(f: SubAgentFindings) -> bool:
    """Reject extraction outputs that echo junk instead of real findings."""
    title_ok = bool((f.title or "").strip())
    findings_ok = bool(f.key_findings) and any(
        (kf or "").strip() for kf in f.key_findings
    )
    refuse = any(t.lower() in (f.title or "").lower() for t in ("no findings", "not found"))
    return title_ok and findings_ok and not refuse


def _fallback_findings(subtopic, final_text: str) -> SubAgentFindings:
    return SubAgentFindings(
        subtopic_id=subtopic.id,
        title=subtopic.title,
        key_findings=[final_text] if final_text else [f"No findings returned for {subtopic.title}"],
        sources=[],
        confidence=0.5,
        raw_notes=final_text,
    )