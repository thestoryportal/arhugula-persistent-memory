# S2.40 Kickoff — model-hunt scoping (ROUTE-MODEL) + GPT-J positive control (Gate A, carried)

Session type: Execution + validation. Selected by the S2.39 ROUTING GATE = ROUTE-MODEL. S2.39 showed the Qwen attribute-entanglement substantially collapses on a structurally-diverse corpus (cfb-v4): drift 2.45→0.20, expression held, specificity KL=0, front-loading persists. The model axis is cleaner than v1.7 claimed. This session (a) runs the still-missing GPT-J positive control, and (b) scopes the model-hunt on a trustworthy corpus.

## Read order
- session_2_39_summary_block.md + framework_finding_v1_8_additive.md (ROUTE-MODEL; v1.7.1/.3/.4 reopened)
- s239_qwen_cfb_v4_proberun.json (the corpus-robustness numbers + resolved cfb-v4 facts)
- framework_finding_v1_7_consolidated.md (v1.7.2 front-loading + convergence/specificity survive; entanglement/viability flagged)
- session_2_26_summary_block.md (AKD-eliminated; cfb-v3 high-AKD)

## First actions at entry
1. Engine fingerprint gate: `5c0c706a…c78770`, `_cov_cpu==3`. Engine UNMODIFIED.
2. Kernel hygiene; target `" "+object`.

## Arms (in order)
- **GATE A — GPT-J positive control (do FIRST; validation anchor).** GPT-J-6B is NOT cached — Arm requires a ~12GB download (operator-gated: confirm the download). Run MEMIT on GPT-J against 3-5 CounterFact/zsRE facts the paper edits cleanly (or the smoke-test Michael Jordan→baseball lineage). Apply the Probe-B harness on cfb-v4-class biographical/property probes. GATE: GPT-J must register effective + attribute-LOCAL (low drift) + entity-specific edits — the calibrated "clean success" shape. If GPT-J ALSO drifts high → harness mis-calibrated → HALT. If clean → confirms the cfb-v4 low-drift reading and the whole instrument.
- **ARM M1 — re-derive Qwen viability on cfb-v4 (the reopened verdict).** Re-run the v1.7.3-style and v1.7.4-style checks (is residual drift tunable / containable) but on cfb-v4, to REPLACE the corpus-confounded v1.7.3/.4. Determine: on a trustworthy corpus, is Qwen attribute-local ENOUGH for a multi-field DB? (Watch the target-semantic-adjacency residual — Schenker.)
- **ARM M2 (scoping) — model-hunt candidate set.** Enumerate acquirable base decoders with cov-cache/patch feasibility for a converge+attribute-local search (the spec target). Document, do not run.

## Deliverables
- session_2_40_summary_block.md; s240_gptj_positive_control.json (Gate A); s240_qwen_cfb_v4_viability.json (Arm M1 — the re-derived verdict); model-hunt candidate table; framework_finding v1.9 additive (calibrated positive control + re-derived Qwen viability); session_2_41_kickoff.md.

## Carried decisions
- D-S239R-1..5; D-S234-* (MANIFEST-1 RESOLVED); D-S233-LAYERMATCH-1/BAND-1/CAPTURE-METHOD-1.

## Open decision surfaced for entry
GPT-J download (~12GB) is the one operator-gated cost. If declined, Gate A cannot run and the cfb-v4 low-drift reading stays harness-self-validated only (partial). Recommend approving the download — the positive control is the missing validation anchor for the entire program.

APPROVE-TO-PROCEED:
