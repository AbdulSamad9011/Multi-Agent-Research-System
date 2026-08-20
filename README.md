# Research Agent (LangGraph + LangChain `create_agent`)

Planner -> N parallel specialist sub-agents (RAG + web search) -> Summarizer.

## Architecture

```
              START
                │
             planner              structured ResearchPlan (3-4 SubTopics)
                │
      Send() fan-out (dynamic — one per subtopic)
                │
   ┌────────┬───┴────┬────────┐
researcher researcher researcher researcher     parallel, create_agent + [RAG tool, web_search]
   └────────┴───┬────┴────────┘
                │   fan-in via operator.add reducer on research_results
           summarizer                            synthesizes final markdown report
                │
               END
```

## Layout

- `state.py` — `ResearchState` (graph-wide state) + `ResearcherTask` (per-branch `Send` payload) + pydantic schemas: `ResearchPlan`, `SubTopic`, `SubAgentFindings`
- `agents/planner.py` — structured-output planner node (`with_structured_output(ResearchPlan)`)
- `agents/researcher.py` — `create_agent(...)`-based sub-agent factory, returns structured `SubAgentFindings`
- `agents/summarizer.py` — reconciles + synthesizes all sub-agent findings into one report
- `rag/ingest.py` — document loader + `InMemoryVectorStore` builder (swap for Chroma/FAISS/PGVector/Pinecone)
- `rag/retriever_tool.py` — wraps the vector store as a tool via `create_retriever_tool`
- `tools/web_search.py` — Tavily live web search tool
- `graph.py` — `StateGraph` wiring, dynamic parallel fan-out via `Send`
- `main.py` — CLI entrypoint

## Run

```bash
pip install -e .
cp .env.example .env      # fill in API keys
python -m research_agent.main "your research question here"
```

## How the parallelism works

`planner` produces a `ResearchPlan` with 3-4 `SubTopic`s. `route_to_researchers`
(a conditional-edge router in `graph.py`) turns that into a list of `Send`
objects — one per subtopic — so LangGraph schedules all `researcher`
branches concurrently in the same superstep, each with only its own
`ResearcherTask` as input (not the full graph state). Every branch returns
`{"research_results": [finding]}`; because `research_results` is typed
`Annotated[List[SubAgentFindings], operator.add]`, LangGraph merges all
branch outputs into one list automatically before `summarizer` runs.

## Extension points (see `TODO`s in code)

- `rag/ingest.py::load_source_documents` — plug in real loaders (PDF, web, Drive, Notion, ...) and swap the in-memory store for a persistent one
- `agents/planner.py` — tune the role taxonomy / add domain-specific planning constraints or few-shot examples
- `agents/researcher.py` — give each role a distinct toolset instead of one shared list (e.g. only an `academic` role gets an arXiv/Semantic Scholar tool)
- `graph.py` — add a `critic`/`verifier` node between researchers and summarizer, or a re-plan loop when a sub-agent's confidence is low
- Human-in-the-loop: add `interrupt()` right after `planner` to approve the plan before fan-out
- Swap `InMemorySaver` for `PostgresSaver`/`AsyncPostgresSaver` for production persistence
