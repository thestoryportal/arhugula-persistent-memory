# S2.38 Kickoff — consolidation & checkpoint (human-gated items + optional cross-model entanglement breadth)

Session type: Execution/analysis (pod-side). S2.37 closed the Qwen layer-locus mechanism (v1.7.1). S2.38 is primarily a checkpoint for the outstanding human-gated items, with an optional breadth arm.

## Read order
- session_2_37_summary_block.md
- framework_finding_v1_7_final.md + framework_finding_v1_7_1_additive.md (KB merge targets)
- reproducibility_manifest_merged_s236.json (designation pending)
- s237_{drift_update_corr,qwen_singlelayer,llama_profile}.json

## First actions at entry
1. Engine fingerprint gate: `5c0c706a…c78770`, `_cov_cpu==3`. Engine UNMODIFIED; lookup canonical.
2. Kernel hygiene; target `" "+object`.

## Human-gated items to resolve at entry (carry until explicitly answered)
- **Manifest designation (D-S237-1):** explicit yes/no — make `reproducibility_manifest_merged_s236.json` canonical and retire sources? Until explicit, no overwrite/delete (storage discipline).
- **KB merges:** framework_finding v1.7 FINAL and v1.7.1 are pod-NV only; human merges into project-knowledge.

## Optional breadth arm (gated on human go; pick per budget)
- **Mistral entanglement profile:** Mistral-7B cleared as base-decoder general (axis 10, S2.29). Run Probe-B per-layer profile + biographical drift on a Mistral edit to test whether front-loading/entanglement is Qwen-unique or appears in another converging arm. Cov caches for Mistral layers 4–8 exist.
- **Qwen multi-fact single-layer:** extend the single-layer ablation beyond Bo Jackson to 002–005 to confirm the L4-most-entangling pattern generalizes.

## Deliverables
- session_2_38_summary_block.md; (if breadth arm) the corresponding JSON + framework_finding v1.7.2 additive; manifest canonical-designation record IF blessed.

## Carried decisions (stand)
- D-S237-1/2/3; D-S236-1/2/3; D-S235-*; D-S234-* ; D-S233-LAYERMATCH-1/BAND-1/CAPTURE-METHOD-1.
- D-S234-MANIFEST-1: merged; canonical designation PENDING explicit human instruction.

## Specialist routing
memit-specialist (primary), state-consistency-theorist (secondary), framework-spec-writer (KB consolidation).

APPROVE-TO-PROCEED:
