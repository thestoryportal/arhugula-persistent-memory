# S2.41 Kickoff — consolidation of the v1.7 viability arc; optional breadth/robustness

Session type: Checkpoint + optional robustness. The LLM-as-Database / Qwen viability question is ANSWERED (v1.7→v1.7.4): viable only for single-attribute/key-value stores; multi-field editing fails and is neither tunable nor containable-into-usefulness. S2.41 is primarily consolidation; substantive arms are optional robustness checks.

## Read order
- session_2_40_summary_block.md + framework_finding_v1_7_4_additive.md
- framework_finding_v1_7_consolidated.md (append 1.7.3 + 1.7.4)
- s240_qwen_containment.json, s239_qwen_reg_sweep.json, s236/s237 Qwen arms
- reproducibility_manifest.json (canonical)

## First actions at entry
1. Engine fingerprint gate: `5c0c706a…c78770`, `_cov_cpu==3`. Engine UNMODIFIED; lookup canonical.
2. Kernel hygiene; target `" "+object`.

## Optional robustness arms (pick per budget; none required — verdict is established)
- **R1 — single-attribute write confirmation (the positive case):** the verdict says Qwen IS viable for key→value. Demonstrate it: a fact whose entity has no other probed attributes, edit + verify NO collateral on a broad biographical battery. Confirms the narrow viable profile actually holds, not just the negative case.
- **R2 — second-engine check:** if any non-MEMIT attribute-local editor is available on NV (ROME/GRACE dry-run dirs exist), test whether the intra-entity entanglement is MEMIT-specific or editor-general on Qwen.
- **R3 — leakage stress:** shrink the verification battery to 1 probe and broaden held-out, to find the leak rate when corruption is less pervasive (bounds the containment tripwire's reliability claim).

## Deliverables
- session_2_41_summary_block.md; (if arm run) arm JSON + framework_finding v1.7.5 additive; S2.42 kickoff. If purely consolidation: a v1.7 FINAL-CONSOLIDATED note and the manifest cosmetic-status fix (if canonical-write unblocked).

## Carried decisions (stand)
- D-S240-1/2; D-S239-1/2; D-S238-1/2; D-S237-*; D-S236-*; D-S235-*; D-S234-* (MANIFEST-1 RESOLVED); D-S233-LAYERMATCH-1/BAND-1/CAPTURE-METHOD-1.

## Specialist routing
memit-specialist (primary), state-consistency-theorist (secondary), framework-spec-writer (KB consolidation).

APPROVE-TO-PROCEED:
