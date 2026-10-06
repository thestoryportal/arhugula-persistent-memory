# Pre-registration — D-C10r-exp2ctl: zero-preserve replay of the autoresearch loop's experiment 2 (v1 DRAFT, 2026-10-06)

**Status: v1 DRAFT.** Ruled by the operator 2026-10-06 ~16:10 ("yes, add it to the step-1 break"). Reviews pending: implementation by Codex (gpt-6.1-sol, max), then a Claude advisor pass on this document + the driver. Nothing has run.

## 0. Where this sits

The autoresearch loop (docs/AUTORESEARCH.md; sandbox `/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10`, branch `autoresearch/oct6`) kept experiment 2 (`92acd03`): a preserve term adding the MLP inputs at every value-token position (`Kp`) to the least-squares solve with weight 1 (`92acd03:edit.py:33,96-99`). It scored **18/72** held-out full reads against the baseline's **7/72** (`runs/20261006-142644_nocommit/score.json`, `runs/20261006-131156_nocommit/score.json`), all guards passing, `described_as` 90.38 → 92.55, `dw_total` 88.97 → 131.42. Codex's read-only review (`results/autoresearch_c10_exp2_codex_review.md`, gpt-6.1-sol max) labelled it **SOUND-CANDIDATE**: evaluation files byte-identical, no content leakage found, the head/subject collisions it targets exist (8 heads, 16 facts), no change to the random draws before the context templates are sampled; cross-process replication and the causal role of the term are UNVERIFIABLE from the records. Loop wins are register candidates, never evidence; this control is the cheapest test of whether the term carries the win.

**The e2e map:** write layer, compile step (§8.1 D20 solve: the covariance/preserve side of the normal equations). Read, governance and deployment layers untouched. Engine unmodified (d941a9fb); the loop's harness (`prepare.py`, `c10e_bandknob.py`) used as-is.

## 1. Question and hypotheses

- **H-P1 (term carries the win):** with `PRESERVE_WEIGHT = 0.0` and everything else identical to `92acd03`, the held-out count falls back toward the baseline.
- **H-P0 (artifact):** the count stays at or above 18/72 without the term — the gain came from something other than the preserve term.
- Codex's inference (I-INFER, not evidence): weight 0 restores the baseline write equation (the baseline's own key cache was zero-initialised per call and never consumed), so the replay is predicted to land at 7/72 with `dw_total` ≈ 88.97.

## 2. Design (one process pair: the edit process + the fixed scorer it spawns; ≈ 50–60 min GPU)

- **Isolation:** a standalone clone of the sandbox repo at `92acd03` in its own directory (not the loop's checkout, which stays untouched; the loop is paused for the step-1 break anyway, D-C10r-rulings-4 (1)).
- **The only science change:** `PRESERVE_WEIGHT = 1.0` → `0.0` in `edit.py`. The value-key collection, every extra forward pass, the diagnostics, layer order and all other constants stay.
- **Provenance additions (inert, logging only):** the SHA-256 of the executed `edit.py` and of the edit-time context-template list (printed right after `get_context_templates`), written to the run directory. A diff of the replay's `edit.py` against `92acd03:edit.py` is checked before launch: it must show only the weight line and the logging lines.
- **Launch:** from the program session, the loop paused, nothing else on the GPU (`pgrep -fl "edit.py|prepare.py|safe-mode|ollama"` empty), MPS asserted available before the run.
- **Order in the break:** after step 1's stages (D-C10s-sharedz), before the loop's relaunch.

## 3. Pre-registered readings (frozen at v2)

**Validity (any failure → INVALID, HALT, no label):** `law5_ok` true; `scope_ok` true; scorer `gates.templates_sha` = `e8605172dce0` (both recorded runs); A1 and A2 each in [68, 71] (both recorded runs 69/69); the pre-launch diff shows only the permitted lines; the executed-source hash recorded.

**Binding count:** `heldout_full` of the replay, H0, /72.
- **SUPPORTS-PRESERVE** if H0 ≤ 11 (the baseline 7 plus the per-process spread of ≈ 4; the recorded fixed-seed baseline reproduced 7 exactly).
- **PARTIAL-PRESERVE** if 12 ≤ H0 ≤ 17.
- **ARTIFACT-SUSPECT** if H0 ≥ 18 (guards reported beside it; a guard failure does not rescue the term).

**Reported beside the label, not binding:** canon, first_token, all guard values, `dw_total` (does it return to ≈ 88.97?), whether H0 = 7 exactly (a determinism observation), per-fact `para_full_hits` for the 16 collision facts vs the other 8.

## 4. Not claimed, whatever the outcome

No CORPUS label changes. SUPPORTS-PRESERVE makes the preserve term a register candidate with one confirming control; it does not show the gain replicates under another seed or process, and it is not §8.9 closure, a route change or an F1 change. The result is recorded in the hypothesis register, runbook §5.2/§13 and `results/`, not as a CORPUS entry (loop findings are candidates, docs/AUTORESEARCH.md).

## 5. Halt discipline

One speculative fix after a `cat -n` read, then HALT with `architecture_profile/s_exp2ctl_halt_diagnostic.json`. A failed validity check is a HALT, not a label.

## 6. Review log

- v1 (this draft): authored by the program session (Claude Opus 5.5) from the Codex review's falsifier section.
