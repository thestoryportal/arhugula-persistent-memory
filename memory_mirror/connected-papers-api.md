---
name: connected-papers-api
description: "Connected Papers: no API key in keychain (2026-10-10) → build graphs on connectedpapers.com via Browser Harness; API helper ready if a key is added"
metadata:
  type: reference
---

Set up 2026-10-06 and tested with the client's test token: the demo paper returned a graph of 41 papers, 10 prior works and 10 derivative works. arXiv-to-Semantic-Scholar id lookup also works, with retry on HTTP 429 because the anonymous Semantic Scholar pool rate-limits bursts. The helper `tools/connected_papers_fetch.py` refuses to run without a key; the test token only reaches the demo paper. A fetched graph stays free to re-fetch for a month, and each new graph costs one usage (`--usages` prints the balance). Current state (2026-10-10): `security find-generic-password -s connectedpapers-api-key` finds no item (exit 44) and `CONNECTED_PAPERS_API_KEY` is unset, so there is no real API key.

**Why:** the operator added Connected Papers as a research instrument for the research pass; the local collection already holds the exported graphs.

**How to apply:** without a key, build graphs on connectedpapers.com through Browser Harness (the operator is signed in with Premium) and export each graph as .bib into the collection INBOX. If a key is later stored in keychain item `connectedpapers-api-key` (or `CONNECTED_PAPERS_API_KEY`), use `uv run --with connectedpapers-py python tools/connected_papers_fetch.py arXiv:<id> DOI:<doi> <sha>` (no install needed); graphs land in the collection's `api/` folder. Fetch only papers that matter, because usages are limited. Treat outputs as leads. See [[notebooklm-via-browser-harness]], [[browser-harness-for-browser-automation]].
