---
name: llm-as-database-program-overview
description: "What the arhugula-persistent-memory repo is (LLM-as-Database F1 readiness program), its workflow, and where its living state lives"
metadata:
  node_type: memory
  type: project
  originSessionId: 4d71207f-24bf-4199-894f-d2f977d9f609
  modified: 2026-10-03T23:24:10.074Z
---

Repo https://github.com/thestoryportal/arhugula-persistent-memory (branch `master`, last commit 2026-06-27) is a falsification-first research program testing whether facts can be stored in, read from, governed in, and served from an LLM's weights (MEMIT/AlphaEdit edits to `down_proj`), toward an "F1 spec-implementation-readiness determination" for the spec at `research_and_specs/llm-as-database-v1_2-integrated-spec.md`. Primary model line: Qwen2.5-3B (band layers 4-8), transformers pinned 4.51.0, editing engine = unmodified kmeng01/memit fork at `memit_dry_run/memit` (gitignored, not in repo).

**Why:** Everything in the repo serves F1; CLAUDE.md/DISCIPLINE.md say to re-ground from living docs, never from memory.

**How to apply:** Read in order README -> DISCIPLINE.md -> docs/SPEC_E2E_GROUND_TRUTH.md -> EXPERIMENT_RUNBOOK.md §0.3 (generated from docs/program_state.json via `tools/render_state.py --write`) -> SESSION_CHECKPOINT.md top block -> CORPUS/. Close-out gate is `tools/closeout_check.py <D-ID>`; prereg + advisor before build and before verdict. Status 2026-06-27: F1 = NOT-READY-WITH-CONDITIONS; C10 (multi-token project-coined values) is the open blocker; next step C10K Stage 0 = source-faithful official AnyEdit run. See [[llm-db-local-migration-gaps]].
