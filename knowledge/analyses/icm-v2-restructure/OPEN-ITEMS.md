# ICM v2 restructure: open items carried past the merge

None of these items blocks the merge. Astra high ruled each one "does not block" (`astra-g7-verdict.md`, Open items). Each needs its own small change or a program decision later. The c10y precondition has its own file, because a c10y brief must not miss it: `experiments/c10y/design/PRECONDITION_HALT_WRITER_REPOINT.md`.

| # | Item | Next action | Owner |
|---|---|---|---|
| 1 | The `/path` deny rules protect only the session's own worktree. The main checkout has no `Edit` deny by absolute path. | Revisit the settings at phase 5. | MAESTRO, phase 5 |
| 2 | `_system/memory/codex-runs-inline-from-claude-bash.md` still recommends `-c mcp_servers.graft.enabled=false`. That flag fails on Codex 0.162.1. | Fix as its own small change (protected path). | MAESTRO |
| 3 | `_system/governance/WORKFLOWS_OVERVIEW.md:157-160` keeps pod-era deployment text. | Rewrite or retire the section. | MAESTRO |
| 4 | `_system/governance/STORAGE.md` does not use the D1 vocabulary yet. | Align the terms. | MAESTRO |
| 5 | Nine empty experiment folders exist on disk (`deployment governance infra_scripts scale track_a`-`track_e`). Git does not carry them. | Remove only with operator approval. | Operator |
| 6 | `code/ops/intel/test_memit_intel_copy.py` fails 7 tests when `TMPDIR` is on the memit volume. It passes on internal disk. The cause is not found. | Find the cause. Until then, the suite runner needs `SUITE_TMPDIR` on internal disk. | MAESTRO |
| 7 | The Codex guard's running-process warning counts every non-exempt Python process on the host (it reuses the `c10w_p2_gate` rule). | Accept as a warning, or narrow the rule. | MAESTRO |
| 8 | CI does not run `code/agents/test_codex_hooks.py` (Linux has no MPS). | Run it on the M3 before each merge that touches the hooks: from `code/agents`, `-m unittest test_codex_hooks`. | MAESTRO |
| 9 | `program/STATUS.md` marks halted or closed items "⭐ NEXT". The text comes from `program/program_state.json`. | Decide what is next at the next program session, then fix the JSON. | Program session |
| 10 | `_index/path-map.tsv` rows for the three split monoliths name the pre-split file. `code/state/resolve_path.py` resolves them correctly. | Normalize the raw map when convenient. | MAESTRO |
| 11 | `_system/governance/REPRODUCIBILITY.md:42,61` name output files in ignored legacy roots. This is true: the group-B scripts write there. | No action unless a group-B script is repointed. | — |
