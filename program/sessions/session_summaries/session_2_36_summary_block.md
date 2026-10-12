# S2.36 Summary Block — v1.7 generalization (5-fact) + manifest merge (COMPLETE)

**Type:** Execution (pod-side). **Outcome:** COMPLETE — all 3 scope items delivered; v1.7 promoted to FINAL; D-S234-MANIFEST-1 resolved (merged to new path, sources untouched). Engine UNMODIFIED. No HALT.

## Gates
- **Engine fingerprint (LAW #1): PASS** — `5c0c706a…c78770`, `_cov_cpu`=3.
- **Known-baseline reproduction (LAW #3): PASS 5/5** — every Llama fact reproduces its s224 step-0 within 1 OOM before any verdict trusted.
- **Read-source-before-authoring / patch-isolation:** n/a new (engine untouched; harness-level only).

## Results
**Arm 1 — Llama 5-fact z-geometry** (v_loss_layer 31): GATE **5/5 PASS**, **STALL 5/5** (max final avg-prob 1.78e-4; non-monotonic; no convergence). Lookup idx 3/4/4/8/6 (canonical subject_last+1).

**Arm 2 — Qwen 5-fact z-geometry** (v_loss_layer 27): **CONVERGE 5/5** (final avg-prob 0.982–0.997, early-break 7–11 steps). Lookup idx 1/2/2/6/4 (true subject-last; no-BOS).

**Arm 2 — Qwen Probe B 5-fact** (apply+restore each): **entity-local / attribute-NON-local 5/5** — biographical drift present every fact (KL 1.66–3.88; ≥1/3 probes flip; e.g. Nigeria→Norway, Mississippi→Texas, Colorado→Oklahoma) with **zero target leakage**; cross-entity specificity **KL=0.000, 0/3 changed for all 5**; update front-loaded on band layer 4 (4/5). Intended consistency post p(tgt) 0.70–0.97.

**Verdict:** the S2.35 single-fact findings GENERALIZE across cfb-v3 for BOTH the Llama architectural-invariant stall and the Qwen entity-local/attribute-nonlocal entanglement. → framework_finding v1.7 **FINAL**.

## Manifest merge (D-S234-MANIFEST-1 — RESOLVED, load-bearing)
- Two sources confirmed **disjoint** at the session level: `reproducibility_manifest.json` (main lineage 2.5b…2.29 + metadata, newer) vs `architecture_profile/reproducibility_manifest.json` (fork sessions 2.18/2.20/2.22 only, older). No session-key collision.
- Built **union** to NEW path `reproducibility_manifest_merged_s236.json`: deep-copy of the richer manifest + B-only `schema_version` + disjoint-union sessions + appended S2.33–S2.36 entries + `_merge_provenance`.
- **Both source manifests left byte-identical / untouched** (storage discipline: no overwrite in place). **Designation request:** human to bless the merged file as canonical and retire the sources.

## Decisions (D-S236-*)
- **D-S236-1** — v1.7 → FINAL on 5/5 generalization (gate 5/5; Llama STALL 5/5; Qwen CONVERGE 5/5; entanglement 5/5).
- **D-S236-2** — Manifest merge as disjoint union to a NEW path; sources untouched; canonical designation deferred to human (load-bearing, not auto-applied).
- **D-S236-3** — Probe B target-prob proxy = first token for multi-token harp (cfb-v3-004), consistent with probe-set-v3 ALLOWLIST_FIRST_TOKEN_PROXY.
- Carried: D-S234-1/2/3, D-S235-1/2/3, D-S233-LAYERMATCH-1/BAND-1/CAPTURE-METHOD-1.

## Artifacts (NV)
- `s236_llama_multifact.json`, `s236_qwen_multifact.json` (5-fact raw: z-geometry + Probe B)
- `framework_finding_v1_7_final.md` (FINAL; supersedes additive; for human KB merge)
- `reproducibility_manifest_merged_s236.json` (merged union; NOT a source overwrite)
- `session_2_36_summary_block.md` (this), `session_2_37_kickoff.md`
- scripts: `s236_llama_multifact.py`, `s236_qwen_multifact.py`

## Note on execution venue
S2.33–S2.36 ran as standalone `python3` shell processes (background), NOT Jupyter kernels — so nothing appears in the RunPod Notebook UI by design. GPU returns to ~2 MiB idle between/after runs. Engine SHA unchanged throughout.

## Next
See `session_2_37_kickoff.md`. STOP for human review.
