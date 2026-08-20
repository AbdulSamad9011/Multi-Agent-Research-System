---
description: Open the graphify knowledge-graph visualization in the browser.
agent: build
---

Open the graphify knowledge graph visualization in the user's default browser.

The interactive files live in `graphify-out/`:

- `graphify-out/graph.html` — recommended: clickable force-directed graph with
  search, node filter, and community colors.
- `graphify-out/GRAPH_TREE.html` — collapsible D3 tree view of the same graph.

Steps:

1. If `graphify-out/graph.html` is missing or stale, rebuild it first
   (AST-only, no API cost):
   `graphify update .`
   (If `graphify` is not on PATH, use the full path
   `C:\Users\hp\.local\bin\graphify.exe`.)
2. If `graphify-out/GRAPH_TREE.html` is missing, generate it:
   `graphify tree --output graphify-out\GRAPH_TREE.html`
3. Open the file in the default browser with PowerShell:
   `Start-Process "graphify-out\graph.html"`

Tell the user which file you opened and describe what they can do with it
(click nodes to inspect connections, use the search box, filter by edge type).