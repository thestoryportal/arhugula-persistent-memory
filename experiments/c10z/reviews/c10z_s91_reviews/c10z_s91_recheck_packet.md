# Re-check: C10Z (ASTRA) amendment §9 → proposed §9.1 revision + Codex build brief v2

You reviewed prereg §9 (docs/C10Z_ASTRA_PREREG.md :449–478, SHA e2d7fa10…) earlier. Your prior reviews:
- Astra: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10z_amend_review_astra.md (FIX-FIRST, 5 BLOCKING)
- Advisor: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10z_amend_review_advisor.md (PROCEED-WITH-CHANGES, B1–B4, A1–A7)

The program drafted a fold. Files to check:
1. /Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10z_s91_draft.md — §9.1 text to be APPENDED (append-only) to the prereg after §9.
2. /Users/robertrhu/.claude/jobs/8ac4cacf/tmp/codex_c10z_build_brief_v2.md — the revised Codex build brief (test-first; model-free while a GPU run, C10W P2, is live).
3. /Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10z_fold_map.md — item → resolution map, including a "Disputed or corrected" section (D1–D5) where the fold disagrees with or corrects reviewer points. Please rule explicitly on each of D1–D5: accept the correction, or say why the original point stands.

Program-lead rulings on the four open items (fold map, last section):
1. Inertness check (h′3) keeps all A7 probe forwards × 3 passes (≈17–85 GPU-min), and runs only if telemetry-on is wanted; the first attempt is telemetry-off.
2. Drift-forced benchmark re-runs (b′4) are not §9(c) refusals, but at most one is made on the program's own call; a second returns to the operator (D-C10z-driftcap, now in the draft).
3. Telemetry-on attempts are allowed only after an INERT record; a timing-gated label (HALTED-BUDGET, EXCEEDS-TTL, HALTED-V11) from a telemetry-on attempt is described as not an identical-reading run and is not cost evidence (h′2).
4. Build is CPU-only until P2 frees the GPU.

Question: does §9.1 + brief v2 precisely resolve each of your BLOCKING items, without introducing a new contradiction with §1–§9 or with the operator's D-C10z-budget bounds (EXPERIMENT_RUNBOOK.md :365)? Cite file:line. Verdict first line: PROCEED / PROCEED-WITH-CHANGES / FIX-FIRST; then remaining BLOCKING items with exact replacement text; then D1–D5 rulings; then non-blocking notes.
