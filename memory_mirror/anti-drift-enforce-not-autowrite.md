---
name: anti-drift-enforce-not-autowrite
description: "Doc-currency: de-duplicate (one source + D-ID pointers); auto-enforce, not auto-write; correcting a pushed claim means grep-sweeping every tracker"
metadata:
  type: feedback
---

When asked to keep documentation in sync / prevent drift (operator, 2026-06-21: "ALL docs, entire repo, never stale, always auto-updated"), the honest engineering answer (advisor + cross-family review, converged):

- **The literal maximal ask is unsatisfiable.** Nothing can auto-*write* corrected narrative prose — only auto-*detect* + *block*. So the deliverable is **auto-ENFORCED** (no stale commit lands), not **auto-updated**; say so out loud. "Fingerprint every doc" gives the same false-green as a presence-only gate (a fingerprint guards only REGISTERED edges) and degrades readability.
- **The cure is DE-DUPLICATION, not instrumentation.** Drift is manufactured by copying an evolving result into many docs (the k≤2→k≤1 lapse). Full detail in ONE source (`CORPUS/NN` / amendment / `docs/program_state.json`); every other doc carries **D-ID + one-line verdict + pointer**. The right-sized built design (generate structured status, fingerprint narrative, pre-commit hook) is in `tools/ANTI_DRIFT.md`.
- **Anchors and tracers rot worst.** Always-in-context anchors (CLAUDE.md) and tracer docs outside the close-out set (REPRODUCIBILITY.md) drift silently. Any doc that references evolving state must be GENERATED, be in the close-out set, or carry only pointers — never a hand-copy; lead anchors with the CURRENT operating mode.
- **Correcting a PUSHED claim = grep-sweep the fan-out (2026-06-25, C5).** A retracted "spec gap" rode a reused paragraph into ~8 trackers plus `program_state.json` `current_latest`; hand-picking spots missed them. Fix: `grep -rn "<false phrase>"` the whole tree, correct the program_state SOURCE + re-render, verify 0 live occurrences. Never push a gap before reading the governing source end-to-end ([[read-authoritative-source-fully]]).

**Why:** the original arc spent ~15 turns on doc-integrity infra that both reviewers said displaced the F1 science ([[evidence-over-scaffolding]]).

**How to apply:** when an infra/process requirement escalates toward "comprehensive / automatic / all", treat it as an architecture decision: name the science-vs-infra trade-off, run the cross-family review before committing to a design, build the right-sized version, then stop. ([[closeout-gate-before-done]])
