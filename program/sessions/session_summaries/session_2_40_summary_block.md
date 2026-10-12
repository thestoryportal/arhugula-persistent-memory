# S2.40 Summary Block — ROUTE-MODEL kickoff: GPT-J positive control (Gate A) → HALT (harness same-subject-drift axis uncalibrated). v1.9 additive. (COMPLETE-as-HALT)

**Type:** Execution + validation (pod-side). **Outcome:** Gate A run cleanly → **HALT per pre-registered gate** → framework_finding v1.9 additive. Arms M1/M2 NOT run (correctly withheld). Engine UNMODIFIED.
**Replaces** the stale top-level S2.40 summary/kickoff that were off-track v1.7.4 copies (verified byte-identical to the archive retained in `architecture_profile/offtrack_s239_s240_selfdirected/`).

## Gates
- **Engine fingerprint (LAW #1): PASS** — `5c0c706a…c78770`, `_cov_cpu==3`, UNMODIFIED. CPU-solve path (S2.31 VRAM mitigation) is unconditional + numerically inert; GPT-J ran the same isolated path, no science-path change.
- **GPT-J download:** operator-APPROVED (~12GB); weights cached, cov-stats/hparams pre-staged → no covariance recompute (caches loaded from disk; atimes confirm).
- **GATE A (GPT-J positive control): FAIL → HALT.** GPT-J is effective + cross-entity-specific but NOT attribute-local. Trips the kickoff's pre-registered HALT condition exactly.

## Gate A result (GPT-J-6B MEMIT, 5 CounterFact/ROME-canonical edits)
- Efficacy: **5/5** top1, mean post p(target) **0.973** (effective ✓).
- Cross-entity specificity: mean KL **0.0001** (clean ✓ — matches MEMIT-paper neighborhood-specificity).
- **Same-subject other-attribute drift: mean KL 2.48 (range 1.89–3.34), flip-frac 0.67–1.0 — HIGH.** Same regime as Qwen-cfb-v3 (2.45); ~12× above Qwen-cfb-v4 (0.20).
- Drift is genuine ORTHOGONAL corruption: Eiffel city→Rome corrupted designer/material/year; MJ sport→baseball corrupted college/birthplace. Not edit-adjacent generalization.

## Interpretation (→ v1.9 additive)
- **Same-subject attribute drift is MEMIT-GENERAL, not a Qwen pathology.** The MEMIT paper's "locality" = CROSS-ENTITY (other subjects), which GPT-J passes (KL≈0). Same-subject-different-attribute consistency was never measured/controlled by the paper; the canonical clean editor violates it.
- **The same-subject drift metric has no calibrated clean floor** — the only known-clean reference (GPT-J) reads high → it is not a valid ABSOLUTE clean-vs-broken discriminator.
- **v1.8's ROUTE-MODEL premise is UNDERCUT:** "diverse corpus ⇒ low drift" fails to generalize (GPT-J diverse facts → high). The **Qwen-cfb-v4 low drift (0.20) is now the unexplained OUTLIER** vs GPT-J high AND Qwen-cfb-v3 high.
- **SURVIVES:** efficacy/convergence; cross-entity specificity (KL≈0 across all three — now GPT-J-confirmed); v1.7.2 front-loading.

## Why M1/M2 were NOT run (halt discipline; prime directive)
Both depend on the same-subject drift metric Gate A just invalidated as an absolute discriminator. Running M1 (Qwen viability re-derivation) or M2 (model-hunt = "select models by low drift") would promote data past an unmet gate. A halted session with clean diagnostic state is the correct outcome. The M1 harness (`s240_qwen_cfb_v4_viability.py`) was authored and is staged for S2.41 once the metric is calibrated.

## Decisions (D-S240R-*)
- **D-S240R-1** — Approved GPT-J download (operator-gated); ran Gate A FIRST as designed.
- **D-S240R-2** — Gate A FAIL → HALT per pre-registered condition. No M1/M2.
- **D-S240R-3** — Diagnosis: same-subject drift is MEMIT-general (cross-entity specificity is the paper's clean axis and IS calibrated; same-subject attribute axis is NOT). Authored v1.9 additive.
- **D-S240R-4** — v1.8's "corpus-artifact / model-axis-cleaner" resolution REOPENED (joins already-reopened v1.7.1/.3/.4). Qwen-cfb-v4 low drift = unexplained outlier.
- **D-S240R-5** — S2.41 = MODEL×CORPUS cross on IDENTICAL probes (disambiguate H-MODEL vs H-PROBE), gated behind a calibrated-floor (benign/null/true-reassert) measurement. NO model-hunt until the locality metric is calibrated.
- **D-S240R-6** — Incorporated operator-supplied external-literature scan (`s240_literature_scan.md`, 6 sources, load-bearing claims PDF-verified). Findings: (a) our phenomenon is the named "Ripple Effect in the Same Entity" (RippleEdits); (b) arXiv 2601.17343 independently endorses the Probe-B behavioral-deviation metric and confirms standard locality eval is inadequate (certifies the Gate A instrument + HALT); (c) BLUE (2502.03748) converts the v1.7.2 front-loading observation into a testable within-MEMIT fix. Folded into v1.9 §2.5.3 and S2.41 (GATE-CAL protocol upgrade, ARM X4 BLUE, ARM X3 BalancEdit-scope, RippleEdits/MQuAKE benchmarks).
- Carried: D-S239R-1..5; D-S234-* (MANIFEST-1 RESOLVED); D-S233-LAYERMATCH-1/BAND-1/CAPTURE-METHOD-1.

## Artifacts (NV)
- `s240_gptj_positive_control.json` (full per-fact Gate A data) + `s240_gptj_positive_control.py` (harness)
- `framework_finding_v1_9_additive.md` (result + reopened framing)
- `architecture_profile/s240_halt_diagnostic.json` (halt record + decisive-next-experiment spec)
- `s240_qwen_cfb_v4_viability.py` (Arm M1 harness — authored, NOT executed; ready for S2.41 once metric is calibrated)
- `s240_literature_scan.md` (external-literature scan + solution clues; feeds S2.41)
- `session_2_40_summary_block.md` (this), `session_2_41_kickoff.md`

## Outstanding
- Same-subject multi-field locality under MEMIT: UNRESOLVED, generically poor even on canonical GPT-J. Possibly needs a different write mechanism, not a different model.
- KB merge: v1.7 consolidated + v1.8 + **v1.9**. Do NOT present any viability verdict as final; v1.7.1/.3/.4 AND v1.8's resolution are all reopened.

## Next
See `session_2_41_kickoff.md`. STOP for human review.
