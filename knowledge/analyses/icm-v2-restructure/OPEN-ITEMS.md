# ICM v2 restructure: open items carried past the merge

None of these items blocks the merge. Astra high ruled each one "does not block" (`astra-g7-verdict.md`, Open items). Each needs its own small change or a program decision later. The c10y precondition has its own file, because a c10y brief must not miss it: `experiments/c10y/design/PRECONDITION_HALT_WRITER_REPOINT.md`.

| # | Item | Next action | Owner |
|---|---|---|---|
| 1 | The `/path` deny rules protect only the session's own worktree. The main checkout has no `Edit` deny by absolute path. | Revisit the settings at phase 5. | MAESTRO, phase 5 |
| 2 | `_system/memory/codex-runs-inline-from-claude-bash.md` still recommends `-c mcp_servers.graft.enabled=false`. That flag fails on Codex 0.162.1. | CLOSED 2026-10-15: flag removed (commit 7d70dfe2); graft removed from the host (lane F `CLOSEOUT.md`). | MAESTRO |
| 3 | `_system/governance/WORKFLOWS_OVERVIEW.md:157-160` keeps pod-era deployment text. | Rewrite or retire the section. | MAESTRO |
| 4 | `_system/governance/STORAGE.md` does not use the D1 vocabulary yet. | Align the terms. | MAESTRO |
| 5 | Nine empty experiment folders exist on disk (`deployment governance infra_scripts scale track_a`-`track_e`). Git does not carry them. | Remove only with operator approval. | Operator |
| 6 | `code/ops/intel/test_memit_intel_copy.py` fails 7 tests when `TMPDIR` is on the memit volume. It passes on internal disk. The cause is not found. | Find the cause. Until then, the suite runner needs `SUITE_TMPDIR` on internal disk. | MAESTRO |
| 7 | The Codex guard's running-process warning counts every non-exempt Python process on the host (it reuses the `c10w_p2_gate` rule). | Accept as a warning, or narrow the rule. | MAESTRO |
| 8 | CI does not run `code/agents/test_codex_hooks.py` (Linux has no MPS). | Run it on the M3 before each merge that touches the hooks: from `code/agents`, `-m unittest test_codex_hooks`. | MAESTRO |
| 9 | `program/STATUS.md` marks halted or closed items "⭐ NEXT". The text comes from `program/program_state.json`. | Decide what is next at the next program session, then fix the JSON. | Program session |
| 10 | `_index/path-map.tsv` rows for the three split monoliths name the pre-split file. `code/state/resolve_path.py` resolves them correctly. | Normalize the raw map when convenient. | MAESTRO |
| 11 | `_system/governance/REPRODUCIBILITY.md:42,61` name output files in ignored legacy roots. This is true: the group-B scripts write there. | No action unless a group-B script is repointed. | — |
| 12 | `build_anchor_map()` reads `git show 3f1a3b95:` and `git show 4e679b15:`. CI uses a shallow checkout, so a CI step that regenerates the anchor map would fail. Today CI runs only `build_index.py --check`, which does not regenerate it. | Add `fetch-depth: 0` before any CI step regenerates the map. | MAESTRO |
| 13 | The old-link resolver (`code/state/resolve_path.py`) proves section identity by CommonMark heading syntax, not by full GitHub rendering. Six classes of live edit can still send an old anchor to another section with exit 0. Each needs a copy of a pinned heading pasted into a history file: (a) a different heading with the same raw slug (`10.1 Purpose` vs `101 Purpose`); (b) an HTML `id=` equal to a pinned fragment; (c) inline markup in a duplicate heading (emphasis, links, padded code, inline HTML); (d) a raw HTML `<h1>`-`<h6>` heading; (e) U+2028 line separators that change block structure; (f) a section moved into a footnote. Sources: `astra-g7-confirm3-verdict.md` section 2, `astra-g7-confirm4-verdict.md` section 2. | First fix: slug the rendered inline text (`renderInline`, strip tags) to close (c). Treat the rest as known limits. | MAESTRO |

## MAESTRO ruling on confirm round 4 (2026-10-12, about 22:20 MDT)

Astra confirm rounds 1-4 (`astra-g7-confirm1..4-*.md`) each returned NO-GO on the old-link resolver. Each round's fix passed, and each round found a deeper class (live heading order → duplicate heading → line scanner → renderer differences). The operator delegated review-bar calls to MAESTRO at about 22:15 ("I am no longer HIL"). MAESTRO ruled: merge, and carry the round-3 and round-4 classes as item 13.

Reasons:
- The remaining classes need GitHub-renderer fidelity. No local parser gives that, so another round would find another edge.
- Every class needs a copy of a pinned heading pasted into a history file. The resolver is a transition tool for pre-restructure links.
- Every non-resolver finding of rounds 1-4 is fixed and confirmed.

Correction: the round-4 packet says the operator accepted the `slug transfer` and `explicit ID` limits. That is false. Astra rated them NON-BLOCKING in round 3; the operator did not rule on them.
