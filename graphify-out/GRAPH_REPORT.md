# Graph Report - research_agent  (2026-08-20)

## Corpus Check
- 30 files · ~14,044 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 146 nodes · 178 edges · 24 communities (18 shown, 6 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e29bbb2a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- graph.py
- What You Must Do When Invoked
- build_vectorstore
- config.py
- /graphify
- opencode.json
- graphify reference: extra exports and benchmark
- graphify.js
- research-agent
- Research Agent (LangGraph + LangChain `create_agent`)
- graphify reference: query, path, explain
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- AGENTS.md
- extraction-spec.md
- state.py

## God Nodes (most connected - your core abstractions)
1. `build_graph()` - 12 edges
2. `What You Must Do When Invoked` - 12 edges
3. `ResearchState` - 10 edges
4. `/graphify` - 10 edges
5. `call_with_model_rotation()` - 9 edges
6. `build_researcher_node()` - 8 edges
7. `graphify reference: extra exports and benchmark` - 8 edges
8. `build_vectorstore()` - 7 edges
9. `ResearcherTask` - 7 edges
10. `build_planner()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `build_planner()` --uses--> `ResearchState`  [INFERRED]
  src/research_agent/agents/planner.py → src/research_agent/state.py
- `build_researcher_node()` --uses--> `SubAgentFindings`  [INFERRED]
  src/research_agent/agents/researcher.py → src/research_agent/state.py
- `build_researcher_node()` --calls--> `call_with_model_rotation()`  [EXTRACTED]
  src/research_agent/agents/researcher.py → src/research_agent/agents/_retry.py
- `build_planner()` --uses--> `ResearchPlan`  [INFERRED]
  src/research_agent/agents/planner.py → src/research_agent/state.py
- `build_graph()` --calls--> `build_planner()`  [EXTRACTED]
  src/research_agent/graph.py → src/research_agent/agents/planner.py

## Import Cycles
- None detected.

## Communities (24 total, 6 thin omitted)

### Community 0 - "graph.py"
Cohesion: 0.16
Nodes (18): Send, build_researcher_node(), BaseTool, Factory for the `researcher` graph node. `tools` (e.g. [rag_tool,…, build_summarizer(), Summarizer node: synthesizes all sub-agent findings into one report., build_graph(), Wires planner -> parallel researchers -> summarizer into a LangGraph graph. (+10 more)

### Community 1 - "What You Must Do When Invoked"
Cohesion: 0.13
Nodes (15): Part A - Structural extraction for code files, Part B - Semantic extraction (parallel subagents), Part C - Merge AST + semantic into final extraction, Step 0 - GitHub repos and multi-path merge (only if a URL or several paths), Step 1 - Ensure graphify is installed, Step 2.5 - Video and audio (only if video files detected), Step 2 - Detect files, Step 3 - Extract entities and relationships (+7 more)

### Community 2 - "build_vectorstore"
Cohesion: 0.28
Nodes (8): Document, Path, build_vectorstore(), load_source_documents(), InMemoryVectorStore, Document ingestion pipeline for the RAG knowledge base. This scaffold ingests a…, TODO: replace with real loaders (PyPDFLoader, WebBaseLoader, GoogleDriveLoader,…, Build (or rebuild) the RAG index. Pass `source_dir=None` to start with an empty…

### Community 3 - "config.py"
Cohesion: 0.17
Nodes (9): Central configuration for models, providers, and runtime knobs. All values are…, Settings, build_rag_tool(), BaseTool, InMemoryVectorStore, Wraps the RAG vector store as a LangChain tool the sub-agents can call., build_web_search_tool(), Live web search tool for sub-agents. Requires TAVILY_API_KEY in the… (+1 more)

### Community 4 - "/graphify"
Cohesion: 0.20
Nodes (9): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Usage (+1 more)

### Community 5 - "opencode.json"
Cohesion: 0.50
Nodes (3): plugin, $schema, .opencode/plugins/graphify.js

### Community 6 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 13 - "Research Agent (LangGraph + LangChain `create_agent`)"
Cohesion: 0.29
Nodes (6): Architecture, Extension points (see `TODO`s in code), How the parallelism works, Layout, Research Agent (LangGraph + LangChain `create_agent`), Run

### Community 14 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 15 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 16 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 17 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 22 - "state.py"
Cohesion: 0.15
Nodes (18): BaseModel, Exception, build_planner(), Planner node: turns the user query into a ResearchPlan (3-4 subtopics).…, Sub-agent factory: a create_agent-based researcher with RAG + web tools. Each…, call_with_model_rotation(), is_daily_quota(), is_rate_limit() (+10 more)

## Knowledge Gaps
- **51 isolated node(s):** `$schema`, `.opencode/plugins/graphify.js`, `research-agent`, `Settings`, `Usage` (+46 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_graph()` connect `graph.py` to `build_vectorstore`, `config.py`, `state.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `build_vectorstore()` connect `build_vectorstore` to `graph.py`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `call_with_model_rotation()` connect `state.py` to `graph.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `build_graph()` (e.g. with `route_to_researchers()` and `ResearchState`) actually correct?**
  _`build_graph()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `ResearchState` (e.g. with `build_planner()` and `build_summarizer()`) actually correct?**
  _`ResearchState` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `.opencode/plugins/graphify.js`, `research-agent` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `What You Must Do When Invoked` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._