# S2.37 Kickoff — v1.7 FINAL consolidation review + entanglement-mechanism deepening (layer-4 locus)

Session type: Execution / analysis (pod-side). S2.36 closed v1.7 FINAL with 5-fact generalization. S2.37 has two tracks: (1) a human-blessing checkpoint for the manifest + v1.7 FINAL, and (2) an optional mechanistic deepening of the Qwen layer-4 entanglement locus. Track 2 is gated on Track 1 approval.

## Read order
- session_2_36_summary_block.md (predecessor close)
- framework_finding_v1_7_final.md (the FINAL finding to consolidate into KB)
- reproducibility_manifest_merged_s236.json (the merged union awaiting canonical designation)
- s236_llama_multifact.json + s236_qwen_multifact.json (5-fact evidence)
- z_convergence_trace_llama_vs_qwen.json (S2.35 single-fact primary evidence)
- architecture_profile/s234_halt_diagnostic.json (re-diagnosis lineage)

## First actions at entry
1. Engine fingerprint gate: `5c0c706a…c78770`, `_cov_cpu==3`. Engine remains UNMODIFIED; lookup path canonical (do not touch).
2. Kernel hygiene: HF_HOME=/workspace/hf_cache before HF import; sys.path+chdir ENGINE_ROOT; pad-token per model.
3. Target discipline: `" "+object` (leading space) on every request.

## Track 1 — Human-blessing checkpoint (do FIRST; load-bearing, human-gated)
- **Manifest designation:** confirm whether `reproducibility_manifest_merged_s236.json` becomes the canonical `reproducibility_manifest.json` and the two sources are retired/archived. DO NOT overwrite or delete sources without explicit instruction (storage discipline). Until blessed, continue writing no session entries into the source manifests.
- **v1.7 FINAL → KB:** framework_finding_v1_7_final.md is pod-NV only (KB not writable from pod). Human merges into project-knowledge. Confirm it supersedes the additive.

## Track 2 — Layer-4 entanglement locus (OPTIONAL, gated on Track 1)
S2.36 localized the largest down_proj update to band layer 4 (4/5 facts) and tied entanglement to the early band. Candidate deepenings (pick per budget):
- **Single-layer ablation:** run Qwen edits restricted to each band layer individually ([4] vs [5] vs … vs [8]) and measure whether biographical drift tracks the layer-4 update magnitude — does isolating L4 reproduce the entanglement, and does excluding L4 reduce it?
- **Drift-vs-update correlation:** across the 5 facts, correlate per-fact L4 update norm with per-fact biographical-drift meanKL (n=5; descriptive only).
- **Llama contrast control:** repeat the per-layer update-norm profile for a Llama edit (even though Llama "stalls" at compute_z, the solve still produces deltas) to test whether the front-loading is Qwen-specific or shared.
- Capture method: Probe B style (apply+restore); no engine modification.

## Deliverables at close
- session_2_37_summary_block.md
- (Track 2, if run) qwen_layer4_entanglement_ablation.json + framework_finding v1.7.1 (additive, layer-locus)
- Manifest canonical-designation record (only if human blesses)

## Carried decisions (stand)
- D-S236-1/2/3; D-S235-1/2/3; D-S234-1/2/3; D-S233-LAYERMATCH-1/BAND-1/CAPTURE-METHOD-1.
- D-S234-MANIFEST-1: RESOLVED to merged file; canonical designation pending human (Track 1).

## Specialist routing
memit-specialist (primary), state-consistency-theorist (secondary), framework-spec-writer (KB consolidation).

## Open decision surfaced for entry
If the human does not bless the manifest designation, Track 2 still runs (it does not depend on the manifest), but no canonical manifest swap occurs and the merged file remains a candidate.

APPROVE-TO-PROCEED:
