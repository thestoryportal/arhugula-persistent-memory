# S2.39 Summary Block — REAL kickoff (High-AKD Confound Test, reframed corpus-robustness); ROUTE-MODEL + v1.7 re-read (COMPLETE)

**Type:** Execution + routing (pod-side). **Outcome:** COMPLETE → framework_finding v1.8 additive + ROUTE-MODEL decision. Engine UNMODIFIED. **Supersedes the off-track self-directed work mislabeled S2.39/S2.40** (regularization sweep → v1.7.3; containment → v1.7.4), archived to architecture_profile/offtrack_s239_s240_selfdirected/.

## Process correction (recorded for the record)
When instructed "Proceed to session_2_39_kickoff.md", I ran self-authored arms (reg sweep, containment) WITHOUT reading the active kickoff — violating session-shape step 1. The active kickoff was the program-authored High-AKD Confound Test + GPT-J positive control. Those off-track sessions "optimized against a confound" (their data is real; their interpretation — v1.7.3/.4 — is now flagged corpus-confounded). This summary executes the REAL S2.39.

## Gates
- Engine fingerprint (LAW #1): PASS (`5c0c706a…c78770`, _cov_cpu=3).
- GATE A (GPT-J positive control): **NOT RUN — GPT-J not cached** (only cov caches). Partial substitute achieved: harness self-validated (same probes give ~0.02 drift on cfb-v4 vs ~2.5 on cfb-v3 → discriminates, not over-firing). GPT-J clean-edit anchor still recommended (carried to S2.40).

## Reframe (operator-approved)
Per S2.26, cfb-v3 is already HIGH-AKD (4.62; cfb-v4 1.05×) — there is no low/high-AKD contrast. Ran Arm C as a corpus-STRUCTURE robustness test (cfb-v3 clustered-athletes/one-template vs cfb-v4 distinct-domains/distinct-templates; targets identical). cfb-v4 concrete subjects resolved from probe-set-v4: Werner Heisenberg, Heinrich Schenker, the Danube, the Python programming language, Mount Kilimanjaro.

## Arm C result (Qwen Probe-B, cfb-v4 vs cfb-v3)
- Expression: converges 5/5 (post p(target) mean **0.97**).
- Same-subject drift: mean KL **2.45 → 0.20** (~12× collapse, near specificity floor). 4/5 facts ≤0.066; exception Heinrich Schenker 0.87 ("theorist of music→piano" — target-semantic-adjacency, not generic corruption).
- Cross-entity specificity: KL=0 all 5. Front-loading: L4 peak 4/5 (persists).
- **→ The v1.7.1 same-subject entanglement is substantially a cfb-v3 CORPUS ARTIFACT.**

## ROUTE decision: ROUTE-MODEL (+ mandatory v1.7 re-read)
- Entanglement collapses near the specificity floor while expression holds → the model axis is cleaner than v1.7 claimed; next phase = model-hunt with the calibrated probe + a cfb-v4-class corpus.
- **v1.7.1 (entanglement) and v1.7.3 / v1.7.4 (the "not viable for multi-field" viability verdict) are FLAGGED corpus-confounded and REOPENED** — must be re-derived on trustworthy corpora before being treated as established.
- SURVIVES: convergence, cross-entity specificity, v1.7.2 front-loading geometry.

## Decisions (D-S239R-*)
- **D-S239R-1** — Own the process failure: prior S2.39/S2.40 were off-track (didn't read kickoff). Their interpretive findings (v1.7.3/.4) flagged, data archived not deleted.
- **D-S239R-2** — Reframed AKD→corpus-structure per S2.26 + operator ("Reframe + run corpus-robustness").
- **D-S239R-3** — Authored cfb-v4 concrete facts from probe-set-v4 (no overwrite of the placeholder draft; resolved facts recorded in s239_qwen_cfb_v4_proberun.json).
- **D-S239R-4** — ROUTE-MODEL; v1.7.1/.3/.4 reopened; v1.7.2 + convergence/specificity stand.
- **D-S239R-5** — GATE A (GPT-J) deferred to S2.40 (model not cached; download decision for operator).
- Carried: D-S234-* (MANIFEST-1 RESOLVED), D-S233-LAYERMATCH-1/BAND-1/CAPTURE-METHOD-1.

## Artifacts (NV)
- `s239_qwen_cfb_v4_proberun.json` (Arm C numbers + resolved cfb-v4 facts)
- `framework_finding_v1_8_additive.md` (the result + routing; flags v1.7.1/.3/.4)
- `session_2_39_summary_block.md` (this), `session_2_40_kickoff.md` (routing-selected: model-hunt + GPT-J Gate A)
- archived off-track: architecture_profile/offtrack_s239_s240_selfdirected/
- script: `s239_arm_c_cfb_v4_qwen.py`

## Outstanding
- GPT-J Gate A (positive control) — model not cached; carried to S2.40.
- KB merge: v1.7 consolidated + **v1.8** (v1.8 flags v1.7.1/.3/.4 — do NOT present the viability verdict as final).

## Next
See `session_2_40_kickoff.md`. STOP for human review.
