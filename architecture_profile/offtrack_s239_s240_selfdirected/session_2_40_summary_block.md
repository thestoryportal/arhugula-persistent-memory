# S2.40 Summary Block — containment feasibility; FINAL Qwen-as-Database viability verdict (COMPLETE)

**Type:** Execution/analysis (pod-side). **Outcome:** COMPLETE → v1.7.4 additive + cumulative final viability verdict. Engine UNMODIFIED. Manifest canonical.

## Gate
- Engine fingerprint (LAW #1): PASS (`5c0c706a…c78770`, _cov_cpu=3). No science-path change (apply+restore + auxiliary probes only).

## Arm run — containment-layer feasibility (write→verify→rollback)
5 Qwen edits; verification battery = locked generalization probes; held-out = S2.40 auxiliary biographical attributes (sport/team/era/role), disjoint from battery. Flag = top1-flip or KL>0.5.
- **detection rate 1.0** (battery flags every edit), **held-out corruption 1.0** (an unprobed attribute corrupted every edit), **leak 0.0** (battery never missed), **accept rate 0.0** (all edits rejected).
- Corruption hits core identity: Tiger golf→tennis, Deion football→baseball, Vonn skiing→"what".
- **Verdict:** containment is a reliable tripwire but rejects 100% of multi-field writes — detects, does not salvage.

## FINAL Qwen-as-Database viability (cumulative v1.7→v1.7.4)
Writable (only model that is) ✅ | cross-record isolation ✅ | intra-record field isolation ❌ | not regularization-tunable ❌ | not containable-into-usefulness ❌.
→ **Viable ONLY for single-attribute-per-entity / key→value stores (or whole-entity overwrite); NOT for multi-field relational records under MEMIT-class editing.** A viable multi-field Qwen-DB needs a different attribute-local write engine.

## Decisions (D-S240-*)
- **D-S240-1** — Ran containment arm A (most decision-relevant). Confirms the viability verdict; closes the last proposed escape route.
- **D-S240-2** — Held-out auxiliary biographical probes authored for this test only; explicitly NOT added to LOCKED probe-set-v3 (used as diagnostics, not for any verdict).
- Carried: D-S239-1/2; D-S238-1/2; D-S237-*; D-S236-*; D-S235-*; D-S234-* (MANIFEST-1 RESOLVED); D-S233-LAYERMATCH-1/BAND-1/CAPTURE-METHOD-1.

## Artifacts (NV)
- `s240_qwen_containment.json`
- `framework_finding_v1_7_4_additive.md` (final viability; for human KB merge)
- `session_2_40_summary_block.md` (this), `session_2_41_kickoff.md`
- script: `s240_qwen_containment.py`

## Outstanding human-gated item (carried)
- **KB merge:** v1.7 FINAL + v1.7.1 + v1.7.2 + v1.7.3 + **v1.7.4** into project-knowledge. Append v1.7.3 + v1.7.4 to `framework_finding_v1_7_consolidated.md`. Pod cannot write KB.

## Next
See `session_2_41_kickoff.md`. The core Qwen-as-DB viability question is now answered; S2.41 is consolidation/optional breadth. STOP for human review.
