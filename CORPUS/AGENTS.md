# AGENTS.md — CORPUS/ (the locked evidence ledger)

This is the single source of truth for what was tested and what it showed. Every headline claim must resolve to a raw artifact cited here. Treat it as **append-only**.

## Rules
- **A new finding = the next number** (`NN_SLUG.md`; currently through `20`). Do NOT renumber or rewrite past entries.
- **Corrections are recorded, not erased.** If a later result overturns an earlier one, the earlier `NN` stays; note "CORRECTED-FROM / SCOPED-BY `<later NN>`" in `03_STATUS_LEDGER.md` and in the new finding. Honesty about reversals is a feature here (see `03`).
- **Caveats are kept flush** with the result — honest, not minimized. Distinguish EVIDENCE-SHOWS from I-INFER. Cite exact artifact paths (`experiments/...`, `results/...`, `logs/...`) + exact numbers, or flag UNVERIFIABLE.
- Artifacts are cited by basename in older docs; resolve via `docs/EXPERIMENT_REGISTRY.md` or `find . -name <name>`. New entries should cite full `experiments/`/`results/` paths.

## Writeup template (follow `14`–`20`)
```
# NN — TITLE (subtitle)
_Result DATE. context + pre-registration ref. Artifacts: <scripts>, <result json>, <logs>. Engine UNMODIFIED; LAW#5 <status>. Decision: D-<TRACK><n>._
## The question            (why this is mandatory, falsification framing)
## Design                  (advisor/independent-review-vetted before the verdict)
## VERDICT — PASS|PARTIAL|FAIL  (+ data table)
## What this resolves, and what it does NOT
## Caveats (kept flush)
## Decision  (D-<TRACK><n>: verdict + consequence for next work)
## FORK     (PASS→/PARTIAL→/FAIL→ next experiment ID)
```

## When you add a finding (the §0.4 close-out, do all of these)
1. Write `CORPUS/NN_*.md`.
2. Append its row/block to `00_MASTER_EVIDENCE.md` and `03_STATUS_LEDGER.md`.
3. Update `../EXPERIMENT_RUNBOOK.md` §0.3 (what's next) + §12 dashboard + §13 changelog, and `../SESSION_CHECKPOINT.md` (new top block), and `../EVIDENCE_INDEX.md`, and `docs/EXPERIMENT_REGISTRY.md`.
4. Add a `D-<TRACK><n>` to the runbook §5 decisions ledger.
5. Add any durable learning to `../memory_mirror/` (one fact per file) and update `MEMORY.md`.
- Use shell/python to write the big canonical docs and **re-read to confirm** — the network FS has shown silent in-place-edit reverts.

## Index
`00` master evidence · `01` provenance manifest · `02` V&V chain · `03` status ledger (reversals) · `04` env/deps · `05`–`06` spec contracts/bridge · `07`–`12` CP1–G3 governance · `13` G6.1 (first falsifier) · `14`–`16` A1/A2/A2b · `17` B3 quant · `18` E1 deploy · `19` B1 size · `20` C2 keying. `README.md` = read order; `COUNCIL_PROTOCOL.md` = review rules.
