# S2.40 Kickoff — viability containment test OR remaining escape routes (LLM-as-Database, Qwen)

Session type: Execution/analysis. v1.7.3 falsified the "surgical knob" escape route for Qwen attribute-entanglement. S2.40 addresses the two remaining viability questions: (A) does a write→verify→rollback containment layer work, and/or (B) breadth confirmation of the no-separation result.

## Read order
- session_2_39_summary_block.md + framework_finding_v1_7_3_additive.md
- framework_finding_v1_7_consolidated.md (FINAL+1.7.1+1.7.2; append 1.7.3)
- s239_qwen_reg_sweep.json, s237_qwen_singlelayer.json, s236_qwen_multifact.json
- reproducibility_manifest.json (canonical, merged union)

## First actions at entry
1. Engine fingerprint gate: `5c0c706a…c78770`, `_cov_cpu==3`. Engine UNMODIFIED; lookup canonical.
2. Kernel hygiene; target `" "+object`.

## Candidate arms (pick per budget; A is most decision-relevant)
- **A — Containment-layer feasibility (write→verify-biography→rollback):** the remaining viable path for Qwen-as-DB. Operationalize: after each edit, probe a fixed same-subject biographical battery; flag drift above a threshold; roll back (restore from weights_copy). Measure detection rate (does the biographical battery reliably catch the corruption?) and the cost (how many edits would be rejected). Tests whether entanglement is at least *detectable/containable* even if not preventable. Apply+restore harness already proven.
- **B — No-separation breadth:** repeat the regularization sweep on 1–2 more facts (e.g. Hakeem, largest drift; Tiger Woods) + add a clamp_norm_factor sweep, to confirm the coupling (flat drift/expression, invariant flip-fraction) is not Bo-Jackson-specific.
- **C — Ceiling-side breadth (optional):** Llama-3.2-3B profile (third ceiling-class control), low priority.

## Deliverables
- session_2_40_summary_block.md; arm JSON(s); framework_finding v1.7.4 additive (containment verdict and/or no-separation breadth); S2.41 kickoff.

## Carried decisions (stand)
- D-S239-1/2; D-S238-1/2; D-S237-*; D-S236-*; D-S235-*; D-S234-* (MANIFEST-1 RESOLVED); D-S233-LAYERMATCH-1/BAND-1/CAPTURE-METHOD-1.

## Open viability framing (for the record)
The cumulative verdict: Qwen is the only writable model (Llama-lineage + Mistral stall), but its writes are entity-local/attribute-NON-local, the entanglement is converger-specific and front-loaded (L4), and it is NOT separable by solve-regularization. Remaining viability hinges on containment (arm A). If containment also fails (drift undetectable or rejection rate impractical), the spec should treat Qwen as viable ONLY for single-attribute-per-entity stores.

## Specialist routing
memit-specialist (primary), state-consistency-theorist (secondary), framework-spec-writer (KB consolidation).

APPROVE-TO-PROCEED:
