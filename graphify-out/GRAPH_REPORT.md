# Graph Report - research_agent  (2026-08-20)

## Corpus Check
- 32 files · ~19,068 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 192 nodes · 248 edges · 26 communities (20 shown, 6 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `30c91b3a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- build_graph
- What You Must Do When Invoked
- build_vectorstore
- MRI Brain Tumor Detection Using Deep Learning and Machine Learning Approaches
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
- researcher.py
- app.py
- graph.py

## God Nodes (most connected - your core abstractions)
1. `build_graph()` - 13 edges
2. `What You Must Do When Invoked` - 12 edges
3. `call_with_model_rotation()` - 11 edges
4. `ResearchState` - 10 edges
5. `/graphify` - 10 edges
6. `build_researcher_node()` - 9 edges
7. `MRI Brain Tumor Detection Using Deep Learning and Machine Learning Approaches` - 9 edges
8. `SubAgentFindings` - 8 edges
9. `graphify reference: extra exports and benchmark` - 8 edges
10. `build_planner()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `_render_plan()` --uses--> `ResearchPlan`  [INFERRED]
  app.py → src/research_agent/state.py
- `_run()` --uses--> `ResearchPlan`  [INFERRED]
  app.py → src/research_agent/state.py
- `_run()` --calls--> `build_graph()`  [EXTRACTED]
  app.py → src/research_agent/graph.py
- `build_researcher_node()` --uses--> `ResearcherTask`  [INFERRED]
  src/research_agent/agents/researcher.py → src/research_agent/state.py
- `build_graph()` --uses--> `ResearchState`  [INFERRED]
  src/research_agent/graph.py → src/research_agent/state.py

## Import Cycles
- None detected.

## Communities (26 total, 6 thin omitted)

### Community 0 - "build_graph"
Cohesion: 0.14
Nodes (13): Central configuration for models, providers, and runtime knobs. All values are…, Settings, build_graph(), Build and compile the research graph. rag_source_dir: optional folder to seed…, CLI entrypoint: run a single research request end-to-end. python -m…, run(), build_rag_tool(), BaseTool (+5 more)

### Community 1 - "What You Must Do When Invoked"
Cohesion: 0.13
Nodes (15): Part A - Structural extraction for code files, Part B - Semantic extraction (parallel subagents), Part C - Merge AST + semantic into final extraction, Step 0 - GitHub repos and multi-path merge (only if a URL or several paths), Step 1 - Ensure graphify is installed, Step 2.5 - Video and audio (only if video files detected), Step 2 - Detect files, Step 3 - Extract entities and relationships (+7 more)

### Community 2 - "build_vectorstore"
Cohesion: 0.24
Nodes (9): _count_ingestible(), Document, Path, build_vectorstore(), load_source_documents(), InMemoryVectorStore, Document ingestion pipeline for the RAG knowledge base. This scaffold ingests a…, TODO: replace with real loaders (PyPDFLoader, WebBaseLoader, GoogleDriveLoader,… (+1 more)

### Community 3 - "MRI Brain Tumor Detection Using Deep Learning and Machine Learning Approaches"
Cohesion: 0.09
Nodes (21): 1. Introduction, 2.1. Problem Statement, 2. Related Works, 3.1. Dataset Collection, 3.2.1. Adaptive Contrast Enhancement Algorithm (ACEA), 3.2.2. Median Filter, 3.2. Preprocessing, 3.3. Fuzzy C-Means (FCM) Segmentation (+13 more)

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

### Community 22 - "researcher.py"
Cohesion: 0.15
Nodes (21): Exception, build_researcher_node(), _content_to_text(), _extract_findings(), _fallback_findings(), _looks_complete(), BaseTool, Researcher node: manual tool-calling loop + structured extraction pass. Why not… (+13 more)

### Community 25 - "app.py"
Cohesion: 0.22
Nodes (12): _apply_overrides(), _empty_result(), _kb_dir_candidates(), Streamlit frontend for the multi-agent research system. Run with: streamlit run…, Execute the graph, streaming node-level progress. Never raises., Top-level folders (one level deep) that contain ingestible files., Push sidebar runtime knobs into the frozen Settings for this run., _render_findings() (+4 more)

### Community 26 - "graph.py"
Cohesion: 0.14
Nodes (21): BaseModel, Send, build_planner(), Planner node: turns the user query into a ResearchPlan (3-4 subtopics).…, build_summarizer(), Summarizer node: synthesizes all sub-agent findings into one report., build_chat_model(), Instantiate a chat model from a "provider:model" string. `init_chat_model` has… (+13 more)

## Knowledge Gaps
- **65 isolated node(s):** `$schema`, `.opencode/plugins/graphify.js`, `research-agent`, `Settings`, `Usage` (+60 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_graph()` connect `build_graph` to `app.py`, `graph.py`, `build_vectorstore`, `researcher.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `call_with_model_rotation()` connect `researcher.py` to `graph.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `build_vectorstore()` connect `build_vectorstore` to `build_graph`, `graph.py`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `build_graph()` (e.g. with `route_to_researchers()` and `ResearchState`) actually correct?**
  _`build_graph()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `ResearchState` (e.g. with `build_planner()` and `build_summarizer()`) actually correct?**
  _`ResearchState` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `.opencode/plugins/graphify.js`, `research-agent` to the rest of the system?**
  _65 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build_graph` be split into smaller, more focused modules?**
  _Cohesion score 0.13970588235294118 - nodes in this community are weakly interconnected._