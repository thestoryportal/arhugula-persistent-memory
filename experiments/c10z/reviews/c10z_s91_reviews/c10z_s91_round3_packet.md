# Round-3 re-check (narrow): C10Z §9.1 draft + Codex brief v2 after the round-2 fold

HARD CONSTRAINT: run no python of any kind (a live GPU run's stage gate refuses its next stage if any python process exists). Read files with shell tools only.

Round-2 reviews: Astra /private/tmp/claude-501/reviews/c10z_s91_recheck_astra.md (FIX-FIRST, blocking 1–4), Advisor /private/tmp/claude-501/reviews/c10z_s91_recheck_advisor.md (PROCEED-WITH-CHANGES, blocking N1, N2).
Folded files: /Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10z_s91_draft.md (D), /Users/robertrhu/.claude/jobs/8ac4cacf/tmp/codex_c10z_build_brief_v2.md (B); resolution map /Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10z_fold_map.md section "## Round 2" (rows R1–R18, incl. declined non-blocking items with reasons).

One program-lead change beyond the reviews: D (h′3) Cost bullet — the inertness check is now outside D-C10z-budget's approved GPU time and runs only after an operator yes to its stated cost (previously it claimed authorization through D-C10r-rulings-11's "proven inert" path).

Scope: (1) is each of the six round-2 blocking items resolved exactly as you specified, at the right place, with no residual contradiction elsewhere in D or B (grep for the superseded wording)? (2) did any round-2 edit (incl. adopted non-blocking A-2..A-6, the warm-up pass, the benchmark_module() seam, the full stage-3 launch line, the lead's Cost change) introduce a new contradiction with prereg docs/C10Z_ASTRA_PREREG.md §1–§9 (in /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a) or EXPERIMENT_RUNBOOK.md:365? (3) are the declined items' reasons acceptable? Do not re-open settled round-1 points.

Output: first line PROCEED / PROCEED-WITH-CHANGES / FIX-FIRST; then any BLOCKING item with exact replacement text and file:line; then brief notes. Keep it short.
