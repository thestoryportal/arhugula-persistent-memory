---
name: experiment-runbook-is-canonical
description: EXPERIMENT_RUNBOOK.md is the canonical roadmap; start at §0.3 (generated from docs/program_state.json), decisions in §5, storage in §3.3a
metadata:
  type: project
---

`EXPERIMENT_RUNBOOK.md` at the repo root (created 2026-06-18) is the **living, canonical operating runbook** for the LLM-as-Database program's path to spec implementation-readiness. For ANY experimental work, read it before acting (it's item 0 in `SESSION_BOOTSTRAP.md` §1; CLAUDE.md points at it).

It contains: §0 entry point + **CURRENT POSITION (§0.3 = single source of what's next)**; §1 tools/instruments; §2 operating disciplines; §3 operational hygiene (heading still says "RunPod"; the binding part now is **§3.3a storage & archival policy**); §4 knowledge-base index; §5 Decisions Ledger (scientific reasoning may be revisited; §5.2's operator scope, frozen-criteria and run-authorization rulings remain binding until explicitly amended); §6 dependency/model sourcing catalog; §7 standing scientific context; §8 the Track A–F experiment decision tree; §9 master decision-tree map; §10 readiness checklist; §11 risk register; §12 live status dashboard; §13 changelog.

**§0.3 is generated:** the block between the `GENERATED` markers is rendered from `docs/program_state.json` by `python3 tools/render_state.py --write` — never hand-edit inside the markers; edit the JSON and re-render.

**Discipline:** it is LIVING — on every experiment completion / decision / new dependency / durable learning, update program_state.json (→ §0.3) + §12 + §13 (+ the §5 Decision-ID) and mirror to CORPUS + memory (§0.4); `LLMDB_ROOT=$PWD python3 tools/closeout_check.py <D-ID>` checks it. Related: [[prototype-tautology-trap]], [[standing-auth-forward-requirements]], [[disk-budget-before-dispatch]].
