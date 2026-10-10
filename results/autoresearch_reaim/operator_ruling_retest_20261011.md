# D-C10r-rulings-18 — pre-registered re-test of the AutoResearch best recipe + minted-token arm (operator, 2026-10-11 ~00:10Z)

Asked by MAESTRO28 through AskUserQuestion (recommendation first: recipe alone). Operator chose
**"Approve, with minted token"**.

Scope approved (planning only — no GPU run is authorized by this ruling):
- After the NEW-1 one-shot run, draft ONE pre-registration that tests:
  - Arm R: the AutoResearch loop's best recipe, sandbox commit `73f78ce`
    (`/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10`, "write gain 1.25 past the solved
    target; eigh projector"); its loop score 34/72 held-out (score.json run 20261006-193809) is treated as
    INFLATED because write prompts paraphrased the sealed held-out templates
    (`results/autoresearch_c10_heldout_mirroring_2026-10-06.md`).
  - Arm M: the minted-token lead (CORPUS/45_C10L_MINT_TOKEN.md: 39–46/72, five replicates 34–46/72).
- Program gates: write prompts sealed and checked against the held-out templates (no paraphrase overlap);
  G1–G7 guards; size-matched control edits (same ΔW scale) to rule out "bigger edit scores more";
  a second seed; LAW#5 inertness; engine fingerprint.
- Sequence: prereg draft (Codex builder, test-first) → Astra review to freeze → operator go for the run
  (separate authorization, with disk budget) → run → Astra reading.
- Not before NEW-1's run completes; does not displace the Drive backup (C10Y unblock path, D-C10r-rulings-17).
