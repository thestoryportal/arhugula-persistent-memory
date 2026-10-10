# Codex brief — D-C10r-seal: review, then implement, the loop sealing + fence v13

**Hard limits.** The GPU is busy with step 1 (`c10s_sharedz_*` processes): run NOTHING that loads the model or uses MPS/torch on the GPU — no `check_equivalence.py`, no `prepare.py --score`, no `edit.py`, no `launch.sh`. Do not touch `experiments/track_c/c10s_sharedz_*`, `docs/C10S_SHARED_Z_PREREG.md`, `memit_dry_run/`, or `experiments/track_c/c10e_bandknob.py`. Do not delete the old sandbox `/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10`. Do not commit; the program session commits. Use `/usr/bin/git`. Disposable `claude --safe-mode … -p` probe sessions are allowed (they use no GPU).

## Read first
`docs/C10R_LOOP_SEALING_V13.md` (the design), `results/autoresearch_c10_sealing_exposure_2026-10-06.md` (exposures 1–7), `results/autoresearch_c10_heldout_mirroring_2026-10-06.md`, and the current loop machinery in `experiments/track_c/autoresearch_c10/` (`sandbox_settings.py`, `launch.sh`, `prepare.py`, `program.md`, `kill_run.sh`, the fence wrappers, `check_equivalence.py`, `README`/docs), plus `docs/AUTORESEARCH.md` and `results/autoresearch_c10_sandbox_probe.md` for the probe pattern.

## Step A — design review (write first)
Write **`results/c10r_seal_codex_design_review.md`**: header (reviewer, model, effort, date), **Verdict: PROCEED or FIX-FIRST**, numbered items (file:line, BLOCKING/ADVISORY, exact fix). Test each design decision against the real code: can the Claude sandbox and the Seatbelt profile express decision 1's two allow-lists and decision 5a's deny-all-but-own-folder? Does the 3-gram rule reject the experiment 3–9 prompts and accept the cleaned base? What did the design miss (another path to the templates, an equivalence consequence, a launch-gate change)?

## Step B — implement (only if Step A has no BLOCKING item; otherwise stop after Step A and say DONE)
Implement decisions 1–5 in the worktree's `experiments/track_c/autoresearch_c10/` and the fence-generation code; build the new sandbox seed (`/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10_sealed`, fresh history, base = `73f78ce` with the mirrored `PROMPTS` removed and a 3-gram-clean `DEV_PROMPT`, cleaned `results.tsv` with the banner, updated `program.md`). Run every verification in design §2 that needs no GPU (items 1–3): offline tests, the direct Seatbelt test, the probe agent. Record each in **`results/c10r_seal_v13_probe.md`**, with the exact commands and outputs. Leave §2 items 4–5 (equivalence re-run, baseline score) for the program session.

Write a short implementation report at **`results/c10r_seal_codex_impl.md`**: files changed, decisions taken where the design was silent, anything deferred. Then say DONE.
