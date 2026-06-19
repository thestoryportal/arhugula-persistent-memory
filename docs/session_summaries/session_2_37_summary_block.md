# S2.37 Summary Block — Qwen entanglement layer-locus + Llama contrast (COMPLETE; manifest designation PENDING)

**Type:** Execution/analysis (pod-side). **Outcome:** Track 2 COMPLETE; Track 1 (manifest canonical designation) **PENDING explicit human instruction** — NOT performed (storage discipline: manifest overwrite/retire needs explicit instruction; "approved, proceed" is not that). Engine UNMODIFIED.

## Gates
- Engine fingerprint (LAW #1): PASS (`5c0c706a…c78770`, _cov_cpu=3).
- No new science-path patch; harness/Probe-B style only. Llama lookup still canonical idx 3.

## Track 2 results (Qwen entanglement layer-locus)
1. **Drift↔update correlation (n=5, S2.36 data):** pearson r=0.90 (L4 update vs biographical-drift meanKL), r=0.92 (total update vs drift). Update magnitude tracks entanglement.
2. **Single-layer ablation (Bo Jackson, band=[L], L∈4..8):** every layer alone lands the edit (p(guitar) 0.73–0.83) AND drifts biography (KL 1.69–3.65); specificity KL=0. Drift magnitude tracks single-layer update norm; **L4 most entangling** (upd 6.28→drift 3.65), L7 least. Entanglement is a magnitude/early-layer effect, not one discrete layer. (Caveat: z_layer co-varies with L.)
3. **Llama contrast control (full-band edit):** Llama update profile **back-loaded** [0.27,0.28,0.34,0.46,0.77] (peak L8) vs Qwen **front-loaded** (peak L4). Llama edit barely expresses (p(guitar) 0.052; drift KL 0.0008, 0/3) — "no drift" because the edit doesn't take, not clean locality. **Front-loading + entanglement are Qwen-specific.**

→ framework_finding **v1.7.1 additive** (layer-locus), deepening v1.7 §X.2.

## Track 1 — Manifest designation (PENDING, load-bearing)
- `reproducibility_manifest_merged_s236.json` remains a CANDIDATE. Source manifests untouched.
- **Explicit human yes/no still required** to (a) designate the merged file canonical and (b) retire/archive the two sources. Per storage discipline I will not overwrite or delete a manifest without explicit instruction. No manifest writes this session.

## Decisions (D-S237-*)
- **D-S237-1** — "approved, proceed with S2.37" interpreted as approval of the session, NOT explicit manifest-overwrite instruction; manifest swap withheld; designation re-surfaced for explicit blessing.
- **D-S237-2** — Single-layer ablation accepted with z_layer co-variation caveat (engine couples z_layer=layers[-1]; fixed-z isolation would require a science-path change, declined per gate #5).
- **D-S237-3** — Llama drift≈0 attributed to non-expressing edit (p 0.05), not attribute-locality.
- Carried: D-S236-1/2/3; D-S235-*; D-S234-*; D-S233-LAYERMATCH-1/BAND-1/CAPTURE-METHOD-1; D-S234-MANIFEST-1 (merged; designation pending).

## Artifacts (NV)
- `s237_drift_update_corr.json`, `s237_qwen_singlelayer.json`, `s237_llama_profile.json`
- `framework_finding_v1_7_1_additive.md` (for human KB merge)
- `session_2_37_summary_block.md` (this), `session_2_38_kickoff.md`
- scripts: `s237_qwen_singlelayer.py`, `s237_llama_profile.py`

## Next
See `session_2_38_kickoff.md`. STOP for human review. Two human-gated items remain: manifest designation (Track 1) and KB merges of v1.7 FINAL + v1.7.1.
