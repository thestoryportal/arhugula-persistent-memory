---
name: llm-as-database-program-overview
description: What the arhugula-persistent-memory repo is (LLM-as-Database F1 readiness program) and the reading order; live state is runbook §0.3, not this note
metadata:
  type: project
---

Repo https://github.com/thestoryportal/arhugula-persistent-memory is a falsification-first research program testing whether facts can be stored in, read from, governed in, and served from an LLM's weights (MEMIT/AlphaEdit edits to `down_proj`), toward an "F1 spec-implementation-readiness determination" for the spec at `research_and_specs/llm-as-database-v1_2-integrated-spec.md`. Primary model line: Qwen2.5-3B (band layers 4-8), transformers pinned 4.51.0; editing engine = the kmeng01/memit fork vendored and git-tracked at `memit_dry_run/memit` (gate: `tools/engine_fingerprint.py`).

**Why:** Everything in the repo serves F1; CLAUDE.md/DISCIPLINE.md say to re-ground from living docs, never from memory.

**How to apply:** Read in order CLAUDE.md (and AGENTS.md for Codex) -> README -> DISCIPLINE.md -> docs/SPEC_E2E_GROUND_TRUTH.md -> EXPERIMENT_RUNBOOK.md §0.3 (generated from docs/program_state.json via `tools/render_state.py --write`) -> SESSION_CHECKPOINT.md top block -> CORPUS/. `docs/EXPERIMENT_REGISTRY.md` maps every experiment ID to its script/config/result/CORPUS doc. Close-out gate is `LLMDB_ROOT=$PWD python3 tools/closeout_check.py <D-ID>`; prereg + advisor before build and before verdict. Current status (F1 verdict, the open C10 blocker, next actions) lives in runbook §0.3 and CORPUS — do not restate it here. See [[local-only-no-rented-compute]].
