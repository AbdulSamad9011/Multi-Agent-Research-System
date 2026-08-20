# Graph Report - research_agent  (2026-08-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 64 nodes · 100 edges · 13 communities (11 shown, 2 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- graph.py
- researcher.py
- build_vectorstore
- config.py
- ResearcherTask
- build_graph
- build_rag_tool
- graphify.js
- research-agent

## God Nodes (most connected - your core abstractions)
1. `build_graph()` - 12 edges
2. `ResearchState` - 10 edges
3. `ResearcherTask` - 7 edges
4. `build_researcher_node()` - 7 edges
5. `build_vectorstore()` - 7 edges
6. `route_to_researchers()` - 6 edges
7. `ResearchPlan` - 5 edges
8. `SubAgentFindings` - 5 edges
9. `build_planner()` - 5 edges
10. `load_source_documents()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `build_graph()` --uses--> `ResearchState`  [INFERRED]
  src/research_agent/graph.py → src/research_agent/state.py
- `route_to_researchers()` --uses--> `ResearchState`  [INFERRED]
  src/research_agent/graph.py → src/research_agent/state.py
- `build_researcher_node()` --uses--> `ResearcherTask`  [INFERRED]
  src/research_agent/agents/researcher.py → src/research_agent/state.py
- `build_planner()` --uses--> `ResearchPlan`  [INFERRED]
  src/research_agent/agents/planner.py → src/research_agent/state.py
- `build_planner()` --uses--> `ResearchState`  [INFERRED]
  src/research_agent/agents/planner.py → src/research_agent/state.py

## Import Cycles
- None detected.

## Communities (13 total, 2 thin omitted)

### Community 0 - "graph.py"
Cohesion: 0.26
Nodes (10): build_planner(), Planner node: turns the user query into a ResearchPlan (3-4 subtopics).…, build_summarizer(), Summarizer node: synthesizes all sub-agent findings into one report., Wires planner -> parallel researchers -> summarizer into a LangGraph graph., Shared graph state schema. `ResearchState` is the top-level state threaded…, Structured output of the planner node., Top-level graph state. (+2 more)

### Community 1 - "researcher.py"
Cohesion: 0.22
Nodes (9): BaseModel, build_researcher_node(), BaseTool, Sub-agent factory: a create_agent-based researcher with RAG + web tools. Each…, Factory for the `researcher` graph node. `tools` (e.g. [rag_tool,…, One slice of the research plan, assigned to one sub-agent., Structured output each sub-agent (researcher) must return., SubAgentFindings (+1 more)

### Community 2 - "build_vectorstore"
Cohesion: 0.28
Nodes (8): Document, Path, build_vectorstore(), load_source_documents(), InMemoryVectorStore, Document ingestion pipeline for the RAG knowledge base. This scaffold ingests a…, TODO: replace with real loaders (PyPDFLoader, WebBaseLoader, GoogleDriveLoader,…, Build (or rebuild) the RAG index. Pass `source_dir=None` to start with an empty…

### Community 3 - "config.py"
Cohesion: 0.29
Nodes (5): Central configuration for models, providers, and runtime knobs. All values are…, Settings, build_web_search_tool(), Live web search tool for sub-agents. Requires TAVILY_API_KEY in the…, TavilySearch

### Community 4 - "ResearcherTask"
Cohesion: 0.33
Nodes (6): Send, Fan-out: dynamically dispatch one `researcher` branch per subtopic. Returning a…, route_to_researchers(), Input payload for a single parallel researcher branch (via Send)., ResearcherTask, TypedDict

### Community 5 - "build_graph"
Cohesion: 0.50
Nodes (4): build_graph(), Build and compile the research graph. rag_source_dir: optional folder to seed…, CLI entrypoint: run a single research request end-to-end. python -m…, run()

### Community 6 - "build_rag_tool"
Cohesion: 0.40
Nodes (4): build_rag_tool(), BaseTool, InMemoryVectorStore, Wraps the RAG vector store as a LangChain tool the sub-agents can call.

## Knowledge Gaps
- **2 isolated node(s):** `Settings`, `research-agent`
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_vectorstore()` connect `build_vectorstore` to `graph.py`, `build_graph`?**
  _High betweenness centrality (0.118) - this node is a cross-community bridge._
- **Why does `build_graph()` connect `build_graph` to `graph.py`, `researcher.py`, `build_vectorstore`, `config.py`, `ResearcherTask`, `build_rag_tool`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Why does `build_researcher_node()` connect `researcher.py` to `graph.py`, `ResearcherTask`, `build_graph`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `build_graph()` (e.g. with `route_to_researchers()` and `ResearchState`) actually correct?**
  _`build_graph()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `ResearchState` (e.g. with `build_planner()` and `build_summarizer()`) actually correct?**
  _`ResearchState` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `build_researcher_node()` (e.g. with `ResearcherTask` and `SubAgentFindings`) actually correct?**
  _`build_researcher_node()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Settings`, `research-agent` to the rest of the system?**
  _2 weakly-connected nodes found - possible documentation gaps or missing edges._