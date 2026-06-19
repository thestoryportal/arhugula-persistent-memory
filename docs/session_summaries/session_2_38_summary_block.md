# S2.38 Summary Block — Mistral ceiling-class control; converger-specific front-loading (COMPLETE; manifest designation STILL PENDING)

**Type:** Execution/analysis (pod-side). **Outcome:** breadth arm COMPLETE → v1.7.2 additive. Manifest canonical designation STILL PENDING explicit human instruction (not performed). Engine UNMODIFIED.

## Gates
- Engine fingerprint (LAW #1): PASS (`5c0c706a…c78770`, _cov_cpu=3). No science-path patch; Probe-B style only.

## Result — Mistral entanglement profile (ceiling-class control)
Mistral-7B-v0.3 (caa1feb0…), full-band edit Bo Jackson→guitar, mirrors Llama:
- per-layer down_proj upd [L4..L8] = [0.22,0.20,0.22,0.27,0.43] — **back-loaded (peak L8)**, small.
- edit barely expresses: consistency p(guitar) 0.135; biographical drift KL 0.019 (0/3 changed); specificity KL=0.
- lookup idx 3 (` plays`, subject+1; Mistral auto-BOS `<s>`), canonical.

**3-model synthesis (v1.7.2):** front-loading (L4 peak) + entanglement + effective edit occur ONLY in the converging falsifier (Qwen). Both ceiling-class base decoders (Llama, Mistral) show back-loaded (L8), small, ineffective updates with ~0 biographical drift. The architectural-invariant stall extends to the weight-update geometry, not just the z-trajectory. Cross-entity specificity KL=0 universally.

## Decisions (D-S238-*)
- **D-S238-1** — "approved, proceed with S2.38" interpreted as approval to run the breadth arm; NOT explicit manifest-overwrite instruction. Manifest swap again WITHHELD.
- **D-S238-2** — Chose Mistral control (second ceiling-class model) over Qwen multi-fact single-layer extension (higher information: cross-architecture generality of the converger-specific mechanism). Qwen multi-fact single-layer remains an optional future arm.
- Carried: D-S237-1/2/3; D-S236-1/2/3; D-S235-*; D-S234-*; D-S233-LAYERMATCH-1/BAND-1/CAPTURE-METHOD-1; D-S234-MANIFEST-1 (merged; designation pending).

## Artifacts (NV)
- `s238_mistral_profile.json`
- `framework_finding_v1_7_2_additive.md` (3-model synthesis; for human KB merge)
- `session_2_38_summary_block.md` (this), `session_2_39_kickoff.md`
- script: `s238_mistral_profile.py`

## Outstanding human-gated items (carried, unchanged)
1. **Manifest designation:** explicit yes/no to make `reproducibility_manifest_merged_s236.json` canonical + retire sources. No overwrite without explicit instruction.
2. **KB merges:** framework_finding v1.7 FINAL, v1.7.1, v1.7.2 are pod-NV only; human merges into project-knowledge.

## Next
See `session_2_39_kickoff.md`. STOP for human review.
