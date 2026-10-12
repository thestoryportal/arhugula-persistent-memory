# MAESTRO66 check of SYNTHESIS.md (2026-10-12 01:28Z)

Builder codexcas replied `CAS SYNTHESIS READY results/context_audit_20261012/SYNTHESIS.md` at 01:28:01Z (46% context left).

## Shape against synthesis_brief.md
- 243 lines (cap 300); sections 1–6 present; 15 findings, each marked VERIFIED with own evidence; 5 operator decisions, recommendation first.
- Only SYNTHESIS.md was created; no guidance file changed (`git status --porcelain` shows only the files already modified at takeover).
- Unit table: 119 rows, every estimate ≤8 min. Nine same-file pairs (C1/D-U4 CLAUDE.md, C2/D-U5 AGENTS.md, C5/D-U6 DISCIPLINE.md, C6/D-U23 GC, C7/D-U24 GA, C8/C10 .codex/config.toml, D-U12a/b/c program_state.json); each pair is serialized by `depends on`, so units that may run in parallel have disjoint edit sets.

## Spot-check of cited evidence (MAESTRO re-read, not the builder's citation)
| Finding | Check | Result |
|---|---|---|
| F01 | master CLAUDE.md:16 names gpt-5.5; :28 pins `e6ac7e18…`; main checkout on `master` | reproduced |
| F02 | W/CLAUDE.md:18 says ≤40% handoff; S2/MEMORY.md:1 says "~20% left" | reproduced |
| F02 | "H/.claude/settings.json finds no enabled Memento plugin" | **NOT REPRODUCED as a conclusion**: Memento is enabled at project-local level, M/.claude/settings.local.json:3 `"memento@promptctl": true`, and installed_plugins.json:1029,1040 lists it. The 40%-vs-20% conflict stands; the "inactive hook" premise does not. Hygiene briefs must not remove reliance on the Memento finalize-session on this basis. |
| F03 | H/.claude/settings.json:78,89 run `graft-hooks.cjs` prompt/session-start | reproduced |
| F04 | experiments/track_b/b3_verdict.py:80-86 opens `results/b3_quant_survival_result.json` with mode `w`; experiments/AGENTS.md:9 `export LLMDB_ROOT=/workspace` | reproduced |
| F05 | W/.codex/config.toml:9 `model = "gpt-5.5"` | reproduced |
| F09 | memory_mirror/mps-offset-view-conversion-bug.md:3 description recommends "clone() first" | reproduced |

Verdict: accepted as the audit synthesis, with the F02 Memento correction above carried into any hygiene brief that touches context-management text.
