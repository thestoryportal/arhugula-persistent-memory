# knowledge/research

**Job:** Holds our research corpus: surveys, notes, tool assessments.
**Read it when:** You frame a method or prior-art question. The research-first rule is in `_system/governance/DISCIPLINE.md`.
**Written by:** `code/research/openresearch_archive.py` (writes the openresearch_archive subfolder). Other files: none found.
**Read by:** `code/research/connected_papers_index.py:28–33` (reads Markdown through `knowledge/**/*.md`; excludes paths that contain `CONNECTED_PAPERS_GRAPH_INDEX`).
**Not here:** Papers: `knowledge/papers/`. Specs: `knowledge/specs/`.
