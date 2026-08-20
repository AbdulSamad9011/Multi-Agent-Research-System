"""Central configuration for models, providers, and runtime knobs.

All values are env-overridable so the same code runs in dev/prod without
edits. See .env.example for the full list.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load .env here, not in the CLI entrypoint: config.py is imported by
# research_agent.graph (and everything else), and import order must not decide
# whether PLANNER_MODEL/API keys take effect. override=True makes .env
# authoritative over any leftover session/global env var.
load_dotenv(override=True)


@dataclass(frozen=True)
class Settings:
    # "provider:model" strings — anything init_chat_model()/create_agent()
    # accepts. Split by role so you can e.g. run a cheaper model for
    # researchers and a stronger one for planning/summarizing.
    # groq = GROQ_API_KEY, google_genai = GOOGLE_API_KEY.
    # Highlight summary: Google is primary for planner/researcher. The
    # researcher no longer demands "tools + structured output at once" (we run
    # a manual tool loop + separate extraction), so Groq gpt-oss models are a
    # valid researcher fallback and the tool-free summarizer/extractor. Avoid
    # groq qwen* models — they dump their chain-of-thought into 'content'.
    # Rotation skips models that report unsupported/404/gated.
    planner_model: str = os.getenv("PLANNER_MODEL", "google_genai:gemini-3.6-flash")
    researcher_model: str = os.getenv("RESEARCHER_MODEL", "google_genai:gemini-3.6-flash")
    summarizer_model: str = os.getenv("SUMMARIZER_MODEL", "groq:openai/gpt-oss-120b")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "google_genai:gemini-embedding-2")

    # Researcher branches fan out in parallel. Google free tier caps each model
    # at ~5 req/min and ~20 req/day, so branches rotate across these models to
    # spread the load. Comma-separated; first entry is the primary default.
    # Researchers only need tool-calling (the manual loop + separate extraction
    # pass handle structured output), so Groq gpt-oss models serve as the
    # quota fallback once all Gemini models are spent for the day.
    # (gemini-2.5-flash-lite was removed from Google's lineup — don't list it.)
    researcher_models: tuple[str, ...] = tuple(
        os.getenv(
            "RESEARCHER_MODELS",
            "google_genai:gemini-3.6-flash,google_genai:gemini-3.5-flash,"
            "google_genai:gemini-3.5-flash-lite,google_genai:gemini-3.1-flash-lite,"
            "groq:openai/gpt-oss-120b,groq:openai/gpt-oss-20b",
        ).split(",")
    )

    # Planner rotation: google primary, Groq fallback (the planner is tool-free,
    # and Groq's json_schema structured output works even though its forcing
    # of tool calls is unreliable — irrelevant here since we bind no tools).
    planner_models: tuple[str, ...] = tuple(
        os.getenv(
            "PLANNER_MODELS",
            "google_genai:gemini-3.6-flash,google_genai:gemini-3.5-flash,"
            "google_genai:gemini-3.5-flash-lite,google_genai:gemini-3.1-flash-lite,"
            "google_genai:gemini-3.7-flash,groq:openai/gpt-oss-120b,"
            "groq:openai/gpt-oss-20b",
        ).split(",")
    )

    # Planner is instructed to produce between min and max subtopics.
    min_subagents: int = int(os.getenv("MIN_SUBAGENTS", 3))
    max_subagents: int = int(os.getenv("MAX_SUBAGENTS", 4))

    # Researchers return free text; a separate extraction pass converts it to
    # the SubAgentFindings schema. Groq is primary (fast, reliable json_schema,
    # tool-free).
    extractor_model: str = os.getenv("EXTRACTOR_MODEL", "groq:openai/gpt-oss-120b")
    extractor_models: tuple[str, ...] = tuple(
        os.getenv(
            "EXTRACTOR_MODELS",
            "groq:openai/gpt-oss-120b,groq:openai/gpt-oss-20b",
        ).split(",")
    )

    rag_top_k: int = int(os.getenv("RAG_TOP_K", 5))
    tavily_max_results: int = int(os.getenv("TAVILY_MAX_RESULTS", 5))


def build_chat_model(model_str: str):
    """Instantiate a chat model from a "provider:model" string.

    `init_chat_model` has no serverless-endpoint mapping for HuggingFace (its
    "huggingface" provider builds a *local* transformers pipeline), so we
    special-case it: ChatHuggingFace over HuggingFaceEndpoint hits HF's free
    Inference API (api-inference.huggingface.co) using HUGGINGFACEHUB_API_TOKEN.
    Everything else falls through to init_chat_model.
    """
    if model_str.startswith("huggingface:"):
        from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

        repo_id = model_str.split(":", 1)[1]
        endpoint = HuggingFaceEndpoint(
            repo_id=repo_id,
            task="text-generation",
            huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN", ""),
            max_new_tokens=2048,
            timeout=120,
        )
        return ChatHuggingFace(llm=endpoint)

    from langchain.chat_models import init_chat_model

    return init_chat_model(model_str)


settings = Settings()
