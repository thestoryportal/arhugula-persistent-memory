---
name: connected-papers-api
description: "Connected Papers API (operator subscription) via the official connectedpapers-py client: tools/connected_papers_fetch.py, run with `uv run --with connectedpapers-py`; key in macOS keychain item 'connectedpapers-api-key' (or CONNECTED_PAPERS_API_KEY); graphs land in connected-papers-knowledge-graphs/api/."
metadata:
  node_type: memory
  type: reference
  originSessionId: 6ffb3bc2-e19e-4357-8a56-33c06cb0cf38
  modified: 2026-10-06T14:42:49.098Z
---

Set up 2026-10-06 and tested with the client's test token: the demo paper returned a graph of 41 papers, 10 prior works and 10 derivative works. arXiv-to-Semantic-Scholar id lookup also works, with retry on HTTP 429 because the anonymous Semantic Scholar pool rate-limits bursts. The helper refuses to run without a key; the test token only reaches the demo paper. A fetched graph stays free to re-fetch for a month, and each new graph costs one usage (`--usages` prints the balance).

**Why:** the operator added Connected Papers as a research instrument for the research pass. The existing collection already holds about 2,177 papers from 117 exported graphs.

**How to apply:** `uv run --with connectedpapers-py python tools/connected_papers_fetch.py arXiv:<id> DOI:<doi> <sha>` (no install needed). Fetch only papers that matter, because usages are limited. Treat outputs as leads, like everything else in the research pass. See [[notebooklm-via-browser-harness]].

**No API key yet (2026-10-06):** build graphs on connectedpapers.com through Browser Harness instead. The operator is signed in there with Premium. Export each graph as .bib into the collection INBOX.
